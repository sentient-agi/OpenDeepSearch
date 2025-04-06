from typing import Optional, Dict, Any, Literal
from opendeepsearch.serp_search.serp_search import create_search_api, SearchAPI
from opendeepsearch.context_building.process_sources_pro import SourceProcessor
from opendeepsearch.context_building.build_context import build_context
from litellm import completion, utils
from dotenv import load_dotenv
import os
from opendeepsearch.prompts import SEARCH_SYSTEM_PROMPT
import asyncio
import nest_asyncio
load_dotenv()

class OpenDeepSearchAgent:
    def __init__(
        self,
        model: Optional[str] = None, #We use LiteLLM to call the model
        system_prompt: Optional[str] = SEARCH_SYSTEM_PROMPT,
        search_provider: Literal["serper", "searxng"] = "serper",
        serper_api_key: Optional[str] = None,
        searxng_instance_url: Optional[str] = None,
        searxng_api_key: Optional[str] = None,
        source_processor_config: Optional[Dict[str, Any]] = None,
        temperature: float = 0.2, # Slight variation while maintaining reliability
        top_p: float = 0.3, # Focus on high-confidence tokens
        reranker: Optional[str] = "None", # Optional reranker identifier
        chunk: bool = False # Whether to chunk the content or not
    ):
        """
        Initialize an OpenDeepSearch agent that combines web search, content processing, and LLM capabilities.

        This agent performs web searches using either SerperAPI or SearXNG, processes the search results to extract
        relevant information, and uses a language model to generate responses based on the gathered context.

        Args:
            model (str): The identifier for the language model to use (compatible with LiteLLM).
            system_prompt (str, optional): Custom system prompt for the language model. If not provided,
                uses a default prompt that instructs the model to answer based on context.
            search_provider (str, optional): The search provider to use ('serper' or 'searxng'). Default is 'serper'.
            serper_api_key (str, optional): API key for SerperAPI. Required if search_provider is 'serper' and
                SERPER_API_KEY environment variable is not set.
            searxng_instance_url (str, optional): URL of the SearXNG instance. Required if search_provider is 'searxng'
                and SEARXNG_INSTANCE_URL environment variable is not set.
            searxng_api_key (str, optional): API key for SearXNG instance. Optional even if search_provider is 'searxng'.
            source_processor_config (Dict[str, Any], optional): Configuration dictionary for the
                SourceProcessor. Supports the following options:
                - strategies (List[str]): Content extraction strategies to use
                - filter_content (bool): Whether to enable content filtering
                - top_results (int): Number of top results to process
            temperature (float, default=0.2): Controls randomness in model outputs. Lower values make
                the output more focused and deterministic.
            top_p (float, default=0.3): Controls nucleus sampling for model outputs. Lower values make
                the output more focused on high-probability tokens.
            reranker (str, optional): Identifier for the reranker to use. If not provided,
                uses the default reranker from SourceProcessor.
            chunk (bool, default=False): Whether to chunk the content or not. If True, the content will be split into smaller segments.
        """
        # Initialize search API based on provider
        self.serp_search = create_search_api(
            search_provider=search_provider,
            serper_api_key=serper_api_key,
            searxng_instance_url=searxng_instance_url,
            searxng_api_key=searxng_api_key
        )

        # Update source_processor_config with reranker if provided
        if source_processor_config is None:
            source_processor_config = {}
        if reranker:
            source_processor_config['reranker'] = reranker

        # Initialize SourceProcessor with provided config or defaults
        self.source_processor = SourceProcessor(**source_processor_config)

        # Initialize LLM settings
        self.model = model if model is not None else os.getenv("LITELLM_SEARCH_MODEL_ID", os.getenv("LITELLM_MODEL_ID", "openrouter/google/gemini-2.0-flash-001"))
        self.temperature = temperature
        self.top_p = top_p
        self.system_prompt = system_prompt
        self.chunk = chunk

        # Configure LiteLLM with OpenAI base URL if provided
        openai_base_url = os.environ.get("OPENAI_BASE_URL")
        if openai_base_url:
            utils.set_provider_config("openai", {"base_url": openai_base_url})
            

    async def search_and_build_context(
        self,
        query: str,
        max_sources: int = 2,
        pro_mode: bool = False
    ) -> str:
        """
        Performs a web search and builds a context from the search results.

        This method executes a search query, processes the returned sources, and builds a
        consolidated context, inspired by FreshPrompt in the FreshLLMs paper, that can be used for answering questions.

        Args:
            query (str): The search query to execute.
            max_sources (int, default=2): Maximum number of sources to process. If pro_mode
                is enabled, this overrides the top_results setting in source_processor_config
                when it's smaller.
            pro_mode (bool, default=False): When enabled, performs a deeper search and more
                thorough content processing.

        Returns:
            str: A formatted context string built from the processed search results.
        """
        # Get sources from SERP
        sources = self.serp_search.get_sources(query)

        # Process sources
        processed_sources = await self.source_processor.process_sources(
            sources,
            max_sources,
            query,
            pro_mode,
            self.chunk
        )

        # Build and return context
        return build_context(processed_sources)

    async def ask(
        self,
        query: str,
        max_sources: int = 2,
        pro_mode: bool = False,
        **kwargs: Optional[Dict[str, Any]]
    ) -> str:
        """
        Searches for information and generates an AI response to the query.

        This method combines web search, context building, and AI completion to provide
        informed answers to questions. It first gathers relevant information through search,
        then uses an LLM to generate a response based on the collected context.

        Args:
            query (str): The question or query to answer.
            max_sources (int, default=2): Maximum number of sources to include in the context.
            pro_mode (bool, default=False): When enabled, performs a more comprehensive search
                and analysis of sources.

        Returns:
            str: An AI-generated response that answers the query based on the gathered context.
        """
        # Get context from search results
        context = await self.search_and_build_context(query, max_sources, pro_mode)
        # Prepare messages for the LLM
        for item in context:
            user_prompt = f"Context:\n{item}\n\nQuestion: {query}"
            for key, value in kwargs.items():
                user_prompt += f"\n{key}: {value}"
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ]
            response = completion(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                top_p=self.top_p
            )
            if "no results" not in response.choices[0].message.content.lower():
                return response.choices[0].message.content
        
        return "No results found."
    
    def ask_sync(
        self,
        query: str,
        max_sources: int = 2,
        pro_mode: bool = False,
        **kwargs: Optional[Dict[str, Any]]
    ) -> str:
        """
        Synchronous version of ask() method.
        """
        try:
            # Try getting the current event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're in a running event loop (e.g., Jupyter), use nest_asyncio
                nest_asyncio.apply()
        except RuntimeError:
            # If there's no event loop, create a new one
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(self.ask(query, max_sources, pro_mode, **kwargs))
