from typing import Optional, Dict, Any
from opendeepsearch.serp_search.serp_search import SerperAPI, DuckDuckGoAPI
from opendeepsearch.context_building.process_sources_pro import SourceProcessor
from opendeepsearch.context_building.build_context import build_context
from litellm import completion
from dotenv import load_dotenv
import os
from opendeepsearch.prompts import SEARCH_SYSTEM_PROMPT
import asyncio
import nest_asyncio
load_dotenv()

class OpenDeepSearchAgent:
    def __init__(
        self,
        model: str, #We use LiteLLM to call the model
        system_prompt: Optional[str] = SEARCH_SYSTEM_PROMPT,
        serper_api_key: Optional[str] = None,
        source_processor_config: Optional[Dict[str, Any]] = None,
        temperature: float = 0.2, # Slight variation while maintaining reliability
        top_p: float = 0.3, # Focus on high-confidence tokens
        reranker: Optional[str] = "None", # Optional reranker identifier
        search_engine: str = "serper" # Default search engine
    ):
        """
        Initialize an OpenDeepSearch agent that combines web search, content processing, and LLM capabilities.

        This agent performs web searches using SerperAPI, processes the search results to extract relevant
        information, and uses a language model to generate responses based on the gathered context.

        Args:
            model (str): The identifier for the language model to use (compatible with LiteLLM).
            system_prompt (str, optional): Custom system prompt for the language model. If not provided,
                uses a default prompt that instructs the model to answer based on context.
            serper_api_key (str, optional): API key for SerperAPI. If not provided, uses default
                authentication method.
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
            search_engine (str, default="serper"): The search engine to use ("serper" or "duckduckgo").
        """
        # Initialize search engine based on the search_engine parameter
        if search_engine == "duckduckgo":
            self.serp_search = DuckDuckGoAPI(api_key=serper_api_key)
        else:
            self.serp_search = SerperAPI(api_key=serper_api_key) if serper_api_key else SerperAPI()
        
        # Update source_processor_config with reranker if provided
        if source_processor_config is None:
            source_processor_config = {}
        if reranker:
            source_processor_config['reranker'] = reranker
        
        # Initialize SourceProcessor with provided config or defaults
        self.source_processor = SourceProcessor(**source_processor_config)
        
        # Initialize LLM settings
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.system_prompt = system_prompt

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
            pro_mode
        )
        
        # Build and return context
        return build_context(processed_sources)

    async def ask(
        self,
        query: str,
        max_sources: int = 2,
        pro_mode: bool = False,
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
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
        ]
        # Get completion from LLM
        response = completion(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            top_p=self.top_p
        )
        
        return response.choices[0].message.content

    def ask_sync(
        self,
        query: str,
        max_sources: int = 2,
        pro_mode: bool = False,
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
        
        return loop.run_until_complete(self.ask(query, max_sources, pro_mode))
