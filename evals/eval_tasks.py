import argparse
import datetime
import json
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
from datasets import Dataset
from dotenv import load_dotenv
from tqdm import tqdm
from opendeepsearch import OpenDeepSearchTool, ListDeepSearchTool, load_config
from opendeepsearch.prompts import MAJORITY_VOTE_PROMPT

from smolagents import (
    AgentError,
    CodeAgent,
    LiteLLMModel,
    HfApiModel,
    PythonInterpreterTool,
    ToolCallingAgent,
)
from smolagents.agents import ActionStep


load_dotenv()

APPEND_ANSWER_LOCK = threading.Lock()


def parse_arguments():
    parser = argparse.ArgumentParser(description="Runs an agent powered by the given model on smolagent benchmark.")
    parser.add_argument(
        "--date",
        type=str,
        default=None,
        help="The date for the evaluation.",
    )
    parser.add_argument(
        "--eval-tasks",
        type=str,
        nargs="+",
        default=["./evals/datasets/frames_test_set.csv", "./evals/datasets/simple_qa_test_set.csv"],
        help="List of evaluation task paths",
    )
    parser.add_argument(
        "--search-model-id",
        type=str,
        default=os.getenv("LITELLM_SEARCH_MODEL_ID", os.getenv("LITELLM_MODEL_ID", "fireworks_ai/accounts/fireworks/models/llama-v3p3-70b-instruct")),
        help="The model ID to use for the search tool (defaults to same as model-id)",
    )
    parser.add_argument(
        "--model-type",
        type=str,
        default="LiteLLMModel",
        choices=["LiteLLMModel", "HfApiModel"],
        help="The model type to use (LiteLLMModel or HfApiModel)",
    )
    parser.add_argument(
        "--model-id",
        type=str,
        default=os.getenv("LITELLM_MODEL_ID", "fireworks_ai/accounts/fireworks/models/llama-v3p3-70b-instruct"),
        help="The model ID to use for the specified model type",
    )
    parser.add_argument(
        "--agent-action-type",
        type=str,
        default="codeact",
        choices=["codeact", "tool-calling", "vanilla"],
        help="The agent action type: 'codeact', 'tool-calling', or 'vanilla' to use the vanilla llm",
    )
    parser.add_argument(
        "--parallel-workers",
        type=int,
        default=8,
        help="The number of processes to run in parallel",
    )
    parser.add_argument(
        "--num-trials",
        type=int,
        default=1,
        help="Number of trials to run for each evaluation",
    )
    return parser.parse_args()


def load_eval_dataset(eval_tasks: list):
    eval_ds = {}
    for task_path in eval_tasks:
        task_name = task_path.split("/")[-1][:-4]
        df = pd.read_csv(task_path)
        dataset = Dataset.from_pandas(df)
        eval_ds[task_name] = dataset
    return eval_ds


def serialize_agent_error(obj):
    if isinstance(obj, AgentError):
        return {"error_type": obj.__class__.__name__, "message": obj.message}
    else:
        return str(obj)


def append_answer(entry: dict, jsonl_file: str) -> None:
    jsonl_file = Path(jsonl_file)
    jsonl_file.parent.mkdir(parents=True, exist_ok=True)
    with APPEND_ANSWER_LOCK, open(jsonl_file, "a", encoding="utf-8") as fp:
        fp.write(json.dumps(entry) + "\n")
    assert os.path.exists(jsonl_file), "File not found!"


def run_with_timeout(func, timeout):
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(func)
        try:
            return future.result(timeout=timeout)
        except TimeoutError:
            return "Timed Out"


def answer_single_question(example, model, answers_file, action_type, search_model_id=None, majority_votes=1):
    def init_agent():
        if action_type == "vanilla":
            agent = model
        elif action_type == "codeact":
            agent = CodeAgent(
                tools=[
                    ListDeepSearchTool(model_name=search_model_id or model.model_id), 
                    OpenDeepSearchTool(model_name=search_model_id or model.model_id)],
                model=model,
                additional_authorized_imports=["numpy", "pandas"],
                max_steps=15,
            )
        elif action_type == "tool-calling":
            agent = ToolCallingAgent(
                tools=[
                    ListDeepSearchTool(model_name=search_model_id or model.model_id), 
                    OpenDeepSearchTool(model_name=search_model_id or model.model_id), 
                    PythonInterpreterTool()
                ],
                model=model,
                additional_authorized_imports=["numpy", "pandas"],
                max_steps=15,
            )
        return agent

    augmented_question = example["question"]
    start_time = time.time()
    TIMEOUT_SECONDS = 300  # 5 minutes timeout

    try:
        answers = []
        tokens = 0
        agent = init_agent()
        for _ in range(majority_votes):
            if action_type == "vanilla":
                def get_vanilla_response():
                    response = agent([{"role": "user", "content": augmented_question}])
                    return response.content, agent.last_output_token_count
                
                answer, tokens = run_with_timeout(get_vanilla_response, TIMEOUT_SECONDS)
                intermediate_steps = answer
            else:
                def get_agent_response():
                    response = str(agent.run(augmented_question))
                    token_count = agent.monitor.get_total_token_counts()
                    # Remove memory from logs to make them more compact.
                    for step in agent.memory.steps:
                        if isinstance(step, ActionStep):
                            step.agent_memory = None
                    return response, token_count, str(agent.memory.steps)
                
                answer, tokens, intermediate_steps = run_with_timeout(get_agent_response, TIMEOUT_SECONDS)
            answers.append(answer)
            token_count = tokens
            
        if len(answers) > 1:
            formatted_answers = "\n".join(
                [f"{i}. {a}" for i, a in enumerate(answers, start=1)])

            user_content = f"""Question: {augmented_question}

            Answers:
            {formatted_answers}

            Choose the most frequent and relevant answer. Output it verbatim.
            """
            messages = [{"role": "system", "content": MAJORITY_VOTE_PROMPT}]
            messages.append({"role": "user", "content": user_content})
            answer = model(messages).content

    except Exception as e:
        print("Error on ", augmented_question, e)
        intermediate_steps = []
    end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    annotated_example = {
        "model_id": model.model_id,
        "agent_action_type": action_type,
        "original_question": example["question"],
        "answer": answer,
        "true_answer": example["true_answer"],
        "intermediate_steps": intermediate_steps,
        "start_time": start_time,
        "end_time": end_time,
        "token_counts": token_count,
    }
    append_answer(annotated_example, answers_file)


def answer_questions(
    eval_ds,
    model,
    date,
    action_type: str = "codeact",
    output_dir: str = "output",
    parallel_workers: int = 32,
    search_model_id: str = None,
    num_trials: int = 1,
    majority_votes: int = 1,
):
    date = date or datetime.date.today().isoformat()
    model_id = model.model_id
    
    # Create directory structure: output/model_id/action_type/task
    model_dir = model_id.replace('/', '__')
    
    for task in eval_ds:
        task_dir = os.path.join(output_dir, model_dir, action_type, task)
        os.makedirs(task_dir, exist_ok=True)
        
        for trial in range(num_trials):
            file_name = f"{task_dir}/{model_id.replace('/', '__')}__{action_type}__{task}__trial{trial}.jsonl"
            print(f"Starting processing trial {trial + 1}/{num_trials} and writing output to '{file_name}'")
            answered_questions = []
            if os.path.exists(file_name):
                with open(file_name, "r") as f:
                    for line in f:
                        answered_questions.append(json.loads(line)["original_question"])
            examples_todo = [example for example in eval_ds[task] if example["question"] not in answered_questions]
            print(f"Launching {parallel_workers} parallel workers.")

            with ThreadPoolExecutor(max_workers=parallel_workers) as exe:
                futures = [
                    exe.submit(answer_single_question, example, model, file_name, action_type, search_model_id, majority_votes)
                    for example in examples_todo
                ]
                for f in tqdm(as_completed(futures), total=len(examples_todo), desc="Processing tasks"):
                    f.result()

            print("All tasks processed.")


if __name__ == "__main__":
    args = parse_arguments()
    
    config = load_config('eval')
    eval_ds = load_eval_dataset(args.eval_tasks)

    if args.model_type == "LiteLLMModel":
        model = LiteLLMModel(
            args.model_id,
            max_completion_tokens=config.get("max_tokens", 8192),
            temperature=config.get("temperature", 0.2),
            # api_key=os.getenv("OPENROUTER_API_KEY"),
        )
    else:
        model = HfApiModel(args.model_id, provider="together", max_tokens=config.get("max_tokens", 8192))

    answer_questions(
        eval_ds,
        model,
        args.date,
        action_type=args.agent_action_type,
        parallel_workers=args.parallel_workers,
        search_model_id=args.search_model_id,
        num_trials=args.num_trials,
        majority_votes=config.get("majority_vote", 1),
    )