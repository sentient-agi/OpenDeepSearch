import pandas as pd
import litellm
import argparse
from evals.grader_prompts import GRADER_TEMPLATE
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from dotenv import load_dotenv
import os
load_dotenv()

def grade_row(row_data):
    idx, row = row_data
    question = row['original_question']
    predicted_answer = row['answer']
    gold_answer = row['true_answer']
    
    input_prompt = GRADER_TEMPLATE.format(
        question=question,
        predicted_answer=predicted_answer,
        target=gold_answer
    )
    model = os.getenv("LITELLM_EVAL_MODEL_ID", os.getenv("LITELLM_MODEL_ID", "openrouter/google/gemini-2.0-flash-001"))
    try:
        output = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": input_prompt}],
            temperature=0.0
        )['choices'][0]['message']['content']
        return idx, output
    except Exception as e:
        print(f"Error processing row {idx}: {e}")
        return idx, "Error"

def autograde_df(df_path, num_cpus=4):
    # Read the dataframe
    df = pd.read_json(df_path, lines=True)
    
    # Prepare data for parallel processing
    row_data = list(df.iterrows())
    
    # Use specified number of CPU cores
    n_processes = max(1, min(num_cpus, cpu_count()))
    print(f"Using {n_processes} processes")
    
    # Create process pool and process rows in parallel
    with Pool(n_processes) as pool:
        # Use tqdm for progress bar
        results = list(tqdm(
            pool.imap(grade_row, row_data),
            total=len(row_data),
            desc="Grading"
        ))
    
    # Sort results by index and extract grades
    results.sort(key=lambda x: x[0])
    final_grades = [grade for _, grade in results]
    
    # Add the grades as a new column
    df['final_grade'] = final_grades
    
    # Save the updated dataframe back to the same file
    df.to_json(df_path, orient='records', lines=True)
    print("Grading completed and results saved!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Auto-grade answers in a DataFrame')
    parser.add_argument('df_path', type=str, help='Path to the DataFrame JSON file')
    parser.add_argument('--num_cpus', type=int, default=4, help='Number of CPU cores to use')
    
    args = parser.parse_args()
    autograde_df(args.df_path, args.num_cpus)
