from typing import Optional, Literal
from smolagents import Tool
from opendeepsearch.ods_agent import OpenDeepSearchAgent
from opendeepsearch.prompts import LIST_SYSTEM_PROMPT

class ListDeepSearchTool(Tool):
    name = "dataframe_enumeration"
    description = """
    Queries the web and returns unstructured data as a dataframe. Best used instead of traditional web search when you need to extract or rank specific items—e.g., the third king of Spain or the fourth largest country in Asia, or books by Stephen King.
    """
    inputs = {
        "query": {
            "type": "string",
            "description": "The search query to perform",
        },
        "columns": {
            "type": "array",
            "description": "The columns to include in the dataframe (optional).",
            "nullable": True,
        },
    }
    output_type = "object"
    def __init__(
        self,
        model_name: Optional[str] = None,
        reranker: str = "infinity",
        search_provider: Literal["serper", "searxng"] = "serper",
        serper_api_key: Optional[str] = None,
        searxng_instance_url: Optional[str] = None,
        searxng_api_key: Optional[str] = None
    ):
        super().__init__()
        self.search_model_name = model_name  # LiteLLM model name
        self.reranker = reranker
        self.search_provider = search_provider
        self.serper_api_key = serper_api_key
        self.searxng_instance_url = searxng_instance_url
        self.searxng_api_key = searxng_api_key

    def forward(self, query: str, columns = ["Items"]) -> str:
        """Perform a web search and return the results as a dataframe."""
        return self.search_tool.ask_sync(query, max_sources=2, pro_mode=True, columns=columns)

    def setup(self):
        self.search_tool = OpenDeepSearchAgent(
            self.search_model_name,
            reranker=self.reranker,
            search_provider=self.search_provider,
            system_prompt=LIST_SYSTEM_PROMPT,
            serper_api_key=self.serper_api_key,
            searxng_instance_url=self.searxng_instance_url,
            searxng_api_key=self.searxng_api_key,
            chunk=False,  # Disable chunking for the tool
        )
