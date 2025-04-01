# 🔍OpenDeepSearch: Democratizing Search with Open-source Reasoning Models and Reasoning Agents 🚀

<!-- markdownlint-disable first-line-h1 -->
<!-- markdownlint-disable html -->
<!-- markdownlint-disable no-duplicate-header -->

<div align="center">
    <img src="./assets/sentient-logo-narrow.png" alt="alt text" width="60%"/>
</div>

<hr>
<div align="center" style="line-height: 1;">
  <a href="https://sentient.xyz/" target="_blank" style="margin: 2px;">
    <img alt="Homepage" src="https://img.shields.io/badge/Sentient-Homepage-%23EAEAEA?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzNDEuMzMzIiBoZWlnaHQ9IjM0MS4zMzMiIHZlcnNpb249IjEuMCIgdmlld0JveD0iMCAwIDI1NiAyNTYiPjxwYXRoIGQ9Ik0xMzIuNSAyOC40Yy0xLjUgMi4yLTEuMiAzLjkgNC45IDI3LjIgMy41IDEzLjcgOC41IDMzIDExLjEgNDIuOSAyLjYgOS45IDUuMyAxOC42IDYgMTkuNCAzLjIgMy4zIDExLjctLjggMTMuMS02LjQuNS0xLjktMTcuMS03Mi0xOS43LTc4LjYtMS4yLTMtNy41LTYuOS0xMS4zLTYuOS0xLjYgMC0zLjEuOS00LjEgMi40ek0xMTAgMzBjLTEuMSAxLjEtMiAzLjEtMiA0LjVzLjkgMy40IDIgNC41IDMuMSAyIDQuNSAyIDMuNC0uOSA0LjUtMiAyLTMuMSAyLTQuNS0uOS0zLjQtMi00LjUtMy4xLTItNC41LTItMy40LjktNC41IDJ6TTgxLjUgNDYuMWMtMi4yIDEuMi00LjYgMi44LTUuMiAzLjctMS44IDIuMy0xLjYgNS42LjUgNy40IDEuMyAxLjIgMzIuMSAxMC4yIDQ1LjQgMTMuMyAzIC44IDYuOC0yLjIgNi44LTUuMyAwLTMuNi0yLjItOS4yLTMuOS0xMC4xQzEyMy41IDU0LjIgODcuMiA0NCA4NiA0NGMtLjMuMS0yLjMgMS00LjUgMi4xek0xNjUgNDZjLTEuMSAxLjEtMiAyLjUtMiAzLjIgMCAyLjggMTEuMyA0NC41IDEyLjYgNDYuNS45IDEuNSAyLjQgMi4zIDQuMiAyLjMgMy44IDAgOS4yLTUuNiA5LjItOS40IDAtMS41LTIuMS0xMC45LTQuNy0yMC44bC00LjctMTguMS00LjUtMi44Yy01LjMtMy40LTcuNC0zLjYtMTAuMS0uOXpNNDguNyA2NS4xYy03LjcgNC4xLTYuOSAxMC43IDEuNSAxMyAyLjQuNiAyMS40IDUuOCA0Mi4yIDExLjYgMjIuOCA2LjIgMzguOSAxMC4yIDQwLjMgOS44IDMuNS0uOCA0LjYtMy44IDMuMi04LjgtMS41LTUuNy0yLjMtNi41LTguMy04LjJDOTQuMiA3My4xIDU2LjYgNjMgNTQuOCA2M2MtMS4zLjEtNCAxLTYuMSAyLjF6TTE5OC4yIDY0LjdjLTMuMSAyLjgtMy41IDUuNi0xLjEgOC42IDQgNS4xIDEwLjkgMi41IDEwLjktNC4xIDAtNS4zLTUuOC03LjktOS44LTQuNXpNMTgxLjggMTEzLjFjLTI3IDI2LjQtMzEuOCAzMS41LTMxLjggMzMuOSAwIDEuNi43IDMuNSAxLjUgNC40IDEuNyAxLjcgNy4xIDMgMTAuMiAyLjQgMi4xLS4zIDU2LjktNTMuNCA1OS01Ny4xIDEuNy0zLjEgMS42LTkuOC0uMy0xMi41LTMuNi01LjEtNC45LTQuMi0zOC42IDI4Ljl6TTM2LjYgODguMWMtNSA0LTIuNCAxMC45IDQuMiAxMC45IDMuMyAwIDYuMi0yLjkgNi4yLTYuMyAwLTIuMS00LjMtNi43LTYuMy02LjctLjggMC0yLjYuOS00LjEgMi4xek02My40IDk0LjVjLTEuNi43LTguOSA3LjMtMTYuMSAxNC43TDM0IDEyMi43djUuNmMwIDYuMyAxLjYgOC43IDUuOSA4LjcgMi4xIDAgNi0zLjQgMTkuOS0xNy4zIDkuNS05LjUgMTcuMi0xOCAxNy4yLTE4LjkgMC00LjctOC40LTguNi0xMy42LTYuM3pNNjIuOSAxMzAuNiAzNCAxNTkuNXY1LjZjMCA2LjIgMS44IDguOSA2IDguOSAzLjIgMCA2Ni02Mi40IDY2LTY1LjYgMC0zLjMtMy41LTUuNi05LjEtNi4ybC01LS41LTI5IDI4Ljl6TTE5Ni4zIDEzNS4yYy05IDktMTYuNiAxNy4zLTE2LjkgMTguNS0xLjMgNS4xIDIuNiA4LjMgMTAgOC4zIDIuOCAwIDUuMi0yIDE3LjktMTQuOCAxNC41LTE0LjcgMTQuNy0xNC45IDE0LjctMTkuMyAwLTUuOC0yLjItOC45LTYuMi04LjktMi42IDAtNS40IDIuMy0xOS41IDE2LjJ6TTk2IDEzNi44Yy0yLjkuOS04IDYuNi04IDkgMCAxLjMgMi45IDEzLjQgNi40IDI3IDMuNiAxMy42IDcuOSAzMC4zIDkuNyAzNy4yIDEuNyA2LjkgMy42IDEzLjMgNC4xIDE0LjIuNSAxIDIuNiAyLjcgNC44IDMuOCA2LjggMy41IDExIDIuMyAxMS0zLjIgMC0zLTIwLjYtODMuMS0yMi4xLTg1LjktLjktMS45LTMuNi0yLjgtNS45LTIuMXpNMTIwLjUgMTU4LjRjLTEuOSAyLjktMS4yIDguNSAxLjQgMTEuNiAxLjEgMS40IDEyLjEgNC45IDM5LjYgMTIuNSAyMC45IDUuOCAzOC44IDEwLjUgMzkuOCAxMC41czMuNi0xIDUuNy0yLjJjOC4xLTQuNyA3LjEtMTAuNi0yLjMtMTMuMi0yOC4yLTguMS03OC41LTIxLjYtODAuMy0yMS42LTEuNCAwLTMgMS0zLjkgMi40ek0yMTAuNyAxNTguOGMtMS44IDEuOS0yLjIgNS45LS45IDcuOCAxLjUgMi4zIDUgMy40IDcuNiAyLjQgNi40LTIuNCA1LjMtMTEuMi0xLjUtMTEuOC0yLjQtLjItNCAuMy01LjIgMS42ek02OS42IDE2MmMtMiAyLjItMy42IDQuMy0zLjYgNC44LjEgMi42IDEwLjEgMzguNiAxMS4xIDM5LjkgMi4yIDIuNiA5IDUuNSAxMS41IDQuOSA1LTEuMyA0LjktMy0xLjUtMjcuNy0zLjMtMTIuNy02LjUtMjMuNy03LjItMjQuNS0yLjItMi43LTYuNC0xLjctMTAuMyAyLjZ6TTQ5LjYgMTgxLjVjLTIuNCAyLjUtMi45IDUuNC0xLjIgOEM1MiAxOTUgNjAgMTkzIDYwIDE4Ni42YzAtMS45LS44LTQtMS44LTQuOS0yLjMtMi4xLTYuNi0yLjItOC42LS4yek0xMjguNSAxODdjLTIuMyAyLjUtMS4zIDEwLjMgMS42IDEyLjggMi4yIDEuOSAzNC44IDExLjIgMzkuNCAxMS4yIDMuNiAwIDEwLjEtNC4xIDExLTcgLjYtMS45LTEuNy03LTMuMS03LS4yIDAtMTAuMy0yLjctMjIuMy02cy0yMi41LTYtMjMuMy02Yy0uOCAwLTIuMy45LTMuMyAyek0xMzYuNyAyMTYuOGMtMy40IDMuOC0xLjUgOS41IDMuNSAxMC43IDMuOSAxIDguMy0zLjQgNy4zLTcuMy0xLjItNS4xLTcuNS03LjEtMTAuOC0zLjR6Ii8%2BPC9zdmc%2B&link=https%3A%2F%2Fhuggingface.co%2FSentientagi" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://github.com/sentient-agi" target="_blank" style="margin: 2px;">
    <img alt="GitHub" src="https://img.shields.io/badge/Github-sentient_agi-181717?logo=github" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://huggingface.co/Sentientagi" target="_blank" style="margin: 2px;">
    <img alt="Hugging Face" src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-SentientAGI-ffc107?color=ffc107&logoColor=white" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>

<div align="center" style="line-height: 1;">
  <a href="https://discord.gg/sentientfoundation" target="_blank" style="margin: 2px;">
    <img alt="Discord" src="https://img.shields.io/badge/Discord-SentientAGI-7289da?logo=discord&logoColor=white&color=7289da" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://x.com/SentientAGI" target="_blank" style="margin: 2px;">
    <img alt="Twitter Follow" src="https://img.shields.io/badge/-SentientAGI-grey?logo=x&link=https%3A%2F%2Fx.com%2FSentientAGI%2F" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>

<h4 align="center">
        <a href="https://arxiv.org/pdf/2503.20201"> Paper  </a> 
</h4>

## Description 📝

OpenDeepSearch is a lightweight yet powerful search tool designed for seamless integration with AI agents. It enables deep web search and retrieval, optimized for use with Hugging Face's **[SmolAgents](https://github.com/huggingface/smolagents)** ecosystem.

<div align="center">
    <img src="./assets/evals.png" alt="Evaluation Results" width="80%"/>
</div>

- **Performance**: ODS performs on par with closed source search alternatives on single-hop queries such as [SimpleQA](https://openai.com/index/introducing-simpleqa/) 🔍.
- **Advanced Capabilities**: ODS performs much better than closed source search alternatives on multi-hop queries such as [FRAMES bench](https://huggingface.co/datasets/google/frames-benchmark) 🚀.

## Table of Contents 📑

- [🔍OpenDeepSearch: Democratizing Search with Open-source Reasoning Models and Reasoning Agents 🚀](#opendeepsearch-democratizing-search-with-open-source-reasoning-models-and-reasoning-agents-)
  - [Description 📝](#description-)
  - [Table of Contents 📑](#table-of-contents-)
  - [Features ✨](#features-)
  - [Installation 📚](#installation-)
  - [Setup](#setup)
  - [Usage ️](#usage-️)
    - [Using OpenDeepSearch Standalone 🔍](#using-opendeepsearch-standalone-)
    - [Running the Gradio Demo 🖥️](#running-the-gradio-demo-️)
    - [Integrating with SmolAgents \& LiteLLM 🤖⚙️](#integrating-with-smolagents--litellm-️)
  - [Search Modes 🔄](#search-modes-)
    - [Default Mode ⚡](#default-mode-)
    - [Pro Mode 🔍](#pro-mode-)
  - [Acknowledgments 💡](#acknowledgments-)
  - [License 📝](#license-)
  - [Contributing 🤝](#contributing-)
  - [Contact 📩](#contact-)

## Features ✨

- **Semantic Search** 🧠: Leverages **[Crawl4AI](https://github.com/unclecode/crawl4ai)** and semantic search rerankers (such as [Qwen2-7B-instruct](https://huggingface.co/Alibaba-NLP/gte-Qwen2-7B-instruct/tree/main) and [Jina AI](https://jina.ai/)) to provide in-depth results
- **Two Modes of Operation** ⚡:
  - **Default Mode**: Quick and efficient search with minimal latency.
  - **Pro Mode (Deep Search)**: More in-depth and accurate results at the cost of additional processing time.
- **Optimized for AI Agents** 🤖: Works seamlessly with **SmolAgents** like `CodeAgent`.
- **Fast and Lightweight** ⚡: Designed for speed and efficiency with minimal setup.
- **Extensible** 🔌: Easily configurable to work with different models and APIs.

## Installation 📚

To install OpenDeepSearch, run:

```bash
pip install -e . #you can also use: uv pip install -e .
pip install -r requirements.txt #you can also use: uv pip install -r requirements.txt
```

Note: you must have `torch` installed.
Note: using `uv` instead of regular `pip` makes life much easier!


## Setup

1. **Sign up for Serper.dev**: Get **free 2500 credits** and add your API key.
   - Visit [serper.dev](https://serper.dev) to create an account.
   - Retrieve your API key and store it as an environment variable:
   
   ```bash
   export SERPER_API_KEY='your-api-key-here'
   ```

2. **Choose a Reranking Solution**:
   - **Quick Start with Jina**: Sign up at [Jina AI](https://jina.ai/) to get an API key for immediate use
   - **Self-hosted Option**: Set up [Infinity Embeddings](https://github.com/michaelfeil/infinity) server locally with open source models such as [Qwen2-7B-instruct](https://huggingface.co/Alibaba-NLP/gte-Qwen2-7B-instruct/tree/main)
   - For more details on reranking options, see our [Rerankers Guide](src/opendeepsearch/ranking_models/README.md)

3. **Set up LiteLLM Provider**:
   - Choose a provider from the [supported list](https://docs.litellm.ai/docs/providers/), including:
     - OpenAI
     - Anthropic
     - Google (Gemini)
     - OpenRouter
     - HuggingFace
     - Fireworks
     - And many more!
   - Set your chosen provider's API key as an environment variable:
   ```bash
   export <PROVIDER>_API_KEY='your-api-key-here'  # e.g., OPENAI_API_KEY, ANTHROPIC_API_KEY
   ```
   - When initializing OpenDeepSearch, specify your chosen model using the provider's format:
   ```python
   search_agent = OpenDeepSearchTool(model_name="provider/model-name")  # e.g., "anthropic/claude-3-opus-20240229", 'huggingface/microsoft/codebert-base', 'openrouter/google/gemini-2.0-flash-001'
   ```

## Usage ️

You can use OpenDeepSearch independently or integrate it with **SmolAgents** for enhanced reasoning and code generation capabilities.

### Using OpenDeepSearch Standalone 🔍

```python
from opendeepsearch import OpenDeepSearchTool
import os

# Set environment variables for API keys
os.environ["SERPER_API_KEY"] = "your-serper-api-key-here"
os.environ["OPENROUTER_API_KEY"] = "your-openrouter-api-key-here"
os.environ["JINA_API_KEY"] = "your-jina-api-key-here"

search_agent = OpenDeepSearchTool(model_name="openrouter/google/gemini-2.0-flash-001", reranker="jina")  # Set pro_mode for deep search
# Set reranker to "jina", or "infinity" for self-hosted reranking
query = "Fastest land animal?"
result = search_agent.search(query)
print(result)
```

### Running the Gradio Demo 🖥️

To try out OpenDeepSearch with a user-friendly interface, simply run:

```bash
python gradio_demo.py
```

This will launch a local web interface where you can test different search queries and modes interactively. You can also change the model, reranker, and search mode in `gradio_demo.py`.

### Integrating with SmolAgents & LiteLLM 🤖⚙️

#### 

```python
from opendeepsearch import OpenDeepSearchTool
from smolagents import CodeAgent, LiteLLMModel
import os

# Set environment variables for API keys
os.environ["SERPER_API_KEY"] = "your-serper-api-key-here"
os.environ["OPENROUTER_API_KEY"] = "your-openrouter-api-key-here"
os.environ["JINA_API_KEY"] = "your-jina-api-key-here"

search_agent = OpenDeepSearchTool(model_name="openrouter/google/gemini-2.0-flash-001", reranker="jina") # Set reranker to "jina" or "infinity"
model = LiteLLMModel(
    "openrouter/google/gemini-2.0-flash-001",
    temperature=0.2
)

code_agent = CodeAgent(tools=[search_agent], model=model)
query = "How long would a cheetah at full speed take to run the length of Pont Alexandre III?"
result = code_agent.run(query)

print(result)
```
### ReAct agent with math and search tools 🤖⚙️

#### 
```python
from opendeepsearch import OpenDeepSearchTool 
from opendeepsearch.wolfram_tool import WolframAlphaTool
from opendeepsearch.prompts import REACT_PROMPT
from smolagents import LiteLLMModel, ToolCallingAgent, Tool 
import os

# Set environment variables for API keys
os.environ["SERPER_API_KEY"] = "your-serper-api-key-here"
os.environ["JINA_API_KEY"] = "your-jina-api-key-here"
os.environ["WOLFRAM_ALPHA_APP_ID"] = "your-wolfram-alpha-app-id-here"
os.environ["FIREWORKS_API_KEY"] = "your-fireworks-api-key-here"

model = LiteLLMModel(
    "fireworks_ai/llama-v3p1-70b-instruct",  # Your Fireworks Deepseek model
    temperature=0.7
)
search_agent = OpenDeepSearchTool(model_name="fireworks_ai/llama-v3p1-70b-instruct", reranker="jina") # Set reranker to "jina" or "infinity"

# Initialize the Wolfram Alpha tool
wolfram_tool = WolframAlphaTool(app_id=os.environ["WOLFRAM_ALPHA_APP_ID"])

# Initialize the React Agent with search and wolfram tools 
react_agent = ToolCallingAgent(
    tools=[search_agent, wolfram_tool],
    model=model,
    prompt_templates=REACT_PROMPT # Using REACT_PROMPT as system prompt
)

# Example query for the React Agent
query = "What is the distance, in metres, between the Colosseum in Rome and the Rialto bridge in Venice"
result = react_agent.run(query)

print(result)
```

## Search Modes 🔄

OpenDeepSearch offers two distinct search modes to balance between speed and depth:

### Default Mode ⚡
- Uses SERP-based interaction for quick results
- Minimal processing overhead
- Ideal for single-hop, straightforward queries
- Fast response times
- Perfect for basic information retrieval

### Pro Mode 🔍
- Involves comprehensive web scraping
- Implements semantic reranking of results
- Includes advanced post-processing of data
- Slightly longer processing time
- Excels at:
  - Multi-hop queries
  - Complex search requirements
  - Detailed information gathering
  - Questions requiring cross-reference verification

## Acknowledgments 💡

OpenDeepSearch is built on the shoulders of great open-source projects:

- **[SmolAgents](https://huggingface.co/docs/smolagents/index)** 🤗 – Powers the agent framework and reasoning capabilities.
- **[Crawl4AI](https://github.com/unclecode/crawl4ai)** 🕷️ – Provides data crawling support.
- **[Infinity Embedding API](https://github.com/michaelfeil/infinity)** 🌍 – Powers semantic search capabilities.
- **[LiteLLM](https://www.litellm.ai/)** 🔥 – Used for efficient AI model integration.
- **Various Open-Source Libraries** 📚 – Enhancing search and retrieval functionalities.

## Citation

If you use `OpenDeepSearch` in your works, please cite it using the following BibTex entry:

```
@misc{alzubi2025opendeepsearchdemocratizing,
      title={Open Deep Search: Democratizing Search with Open-source Reasoning Agents}, 
      author={Salaheddin Alzubi and Creston Brooks and Purva Chiniya and Edoardo Contente and Chiara von Gerlach and Lucas Irwin and Yihan Jiang and Arda Kaz and Windsor Nguyen and Sewoong Oh and Himanshu Tyagi and Pramod Viswanath},
      year={2025},
      eprint={2503.20201},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2503.20201}, 
}
```


## Contact 📩

For questions or collaborations, open an issue or reach out to the maintainers.

