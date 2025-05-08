from dataclasses import dataclass
import os
from typing import Optional, Dict, Any
import requests

from opendeepsearch.serp_search.serp_search import SearchAPI, SearchResult


class SerpAPIException(Exception):
    """Custom exception for Serp API related errors"""
    pass


@dataclass
class SerpAPIConfig:
    """Configuration for SerpAPI"""
    api_key: str
    default_location: str = 'United Kingdom'
    timeout: int = 10
    num_results: int = 20

    @classmethod
    def from_env(cls) -> 'SerpAPIConfig':
        """Create config from environment variables"""
        api_key = os.getenv("SERPAPI_API_KEY")
        if not api_key:
            raise SerpAPIException("SERPAPI_API_KEY environment variables not set")
        return cls(api_key=api_key)

class SerpAPI(SearchAPI):
    def __init__(self, api_key: Optional[str] = None, config: Optional[SerpAPIConfig] = None):
        """Initialize the SerpAPI class"""
        if not api_key and not config:
            raise SerpAPIException("Either api_key or config must be provided")
        
        try: 
            from serpapi import GoogleSearch
            self.GoogleSearch = GoogleSearch
        except ImportError:
            raise SerpAPIException("serpapi is not installed. Please install it using 'pip install google-search-results'")

        if api_key:
            self.config = SerpAPIConfig(api_key=api_key)
        else:
            self.config = config or SerpAPIConfig.from_env()


    @staticmethod
    def extract_fields(items_list, fields_to_extract, field_mapping=None):
        """
        Extracts specified fields from a list of dictionaries.
        Allows renaming fields using field_mapping.
        :param items_list: List of dictionaries to process.
        :param fields_to_extract: List of target field names.
        :param field_mapping: Dictionary {target_field_name: source_field_name_in_serpapi}
                              e.g., {'imageUrl': 'thumbnail'}
        """
        if field_mapping is None:
            field_mapping = {}

        extracted_items = []
        if not items_list: # Handle empty or None lists gracefully
            return []

        for item in items_list:
            if not isinstance(item, dict): # Ensure item is a dictionary
                # Optionally log a warning or skip
                # print(f"Warning: item is not a dictionary: {item}")
                continue
            
            extracted_item = {}
            for target_field in fields_to_extract:
                # Get the source field name from mapping or use target field name
                source_field = field_mapping.get(target_field, target_field)
                
                # Check if the source field exists in the item
                if source_field in item:
                    extracted_item[target_field] = item.get(source_field)
                else:
                    # Try alternate field names for common fields
                    if source_field == 'link' and 'link' not in item:
                        if 'url' in item:
                            extracted_item[target_field] = item.get('url')
                        elif 'href' in item:
                            extracted_item[target_field] = item.get('href')
                    elif source_field == 'snippet' and 'snippet' not in item:
                        if 'description' in item:
                            extracted_item[target_field] = item.get('description')
                        elif 'content' in item:
                            extracted_item[target_field] = item.get('content')
                    else:
                        # Set None for fields not found
                        extracted_item[target_field] = None
            
            extracted_items.append(extracted_item)
        
        return extracted_items

    def standardize_response(self, serp_api_data):
        """
        Standardizes the SerpAPI response to the desired internal structure.
        Handles missing keys gracefully by defaulting to empty lists or None.
        """
        if not isinstance(serp_api_data, dict):
            # Handle cases where serp_api_data might not be a dictionary (e.g. error response)
            return { # Return an empty structure matching the target
                'organic': [], 'topStories': [], 'images': [],
                'graph': None, 'answerBox': None,
                'peopleAlsoAsk': [], 'relatedSearches': []
            }
         
        # Check for error in the response
        if 'error' in serp_api_data:
            return { # Return an empty structure matching the target
                'organic': [], 'topStories': [], 'images': [],
                'graph': None, 'answerBox': None,
                'peopleAlsoAsk': [], 'relatedSearches': []
            }
        
        # Define proper field mappings for each section
        organic_mapping = {
            'link': 'link',            # SerpAPI uses 'link' for organic results
            'title': 'title',          # Title is usually consistent
            'snippet': 'snippet',      # SerpAPI uses 'snippet' for organic descriptions
            'date': 'date'             # Date might be in various places
        }
        
        image_mapping = {
            'title': 'title',          # Image titles
            'imageUrl': 'thumbnail'    # SerpAPI uses 'thumbnail' for image URLs
        }
        
        news_mapping = {
            'title': 'title',          # News story titles
            'imageUrl': 'thumbnail'    # SerpAPI uses 'thumbnail' for news images
        }

        results = {
            'organic': self.extract_fields(
                serp_api_data.get('organic_results', []),
                ['title', 'link', 'snippet', 'date'],
                organic_mapping
            ),
            'topStories': self.extract_fields(
                # SerpAPI might use 'top_stories' or 'news_results'
                serp_api_data.get('top_stories', serp_api_data.get('news_results', [])),
                ['title', 'imageUrl'],
                news_mapping
            ),
            'images': self.extract_fields(
                # SerpAPI might use 'images_results' or 'inline_images'
                (serp_api_data.get('images_results', serp_api_data.get('inline_images', [])))[:6],
                ['title', 'imageUrl'],
                image_mapping
            ),
            'graph': serp_api_data.get('knowledge_graph'),
            'answerBox': serp_api_data.get('answer_box'),
            'peopleAlsoAsk': serp_api_data.get('people_also_ask', []),
            'relatedSearches': serp_api_data.get('related_searches', [])
        }
                
        return results

    def get_sources(
        self,
        query: str,
        num_results: int = 20,
        stored_location: Optional[str] = None
    ) -> SearchResult[Dict[str, Any]]:
        """
        Fetch search results from SerpAPI.

        Args:
            query: Search query string
            num_results: Number of results to return (default: 20)
            stored_location: Optional location string

        Returns:
            SearchResult containing the search results or error information
        """
        if not query.strip():
            return SearchResult(error="Query cannot be empty")

        try:
            search_location = (stored_location or self.config.default_location).lower()
            
            search = self.GoogleSearch({
                "q": query,
                "location": search_location or self.config.default_location,
                "api_key": self.config.api_key,
                "num": num_results or self.config.num_results
            })
            result = search.get_dict()
            
            # If API returns an error, surface it as our error
            if 'error' in result:
                return SearchResult(error=f"SerpAPI error: {result['error']}")

            return SearchResult(data=self.standardize_response(result))

        except requests.RequestException as e:
            return SearchResult(error=f"API request failed: {str(e)}")
        except Exception as e:
            return SearchResult(error=f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    import rich
    from rich.console import Console
    from rich.pretty import Pretty
    
    # Create console for rich output
    console = Console()
    
    # Get API key from environment
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        console.print("[bold red]Error: SERPAPI_API_KEY environment variable is not set[/bold red]")
        exit(1)
    
    # Initialize API and run search
    serp_api = SerpAPI(api_key=api_key)
    query = "What is elon musk's net worth?"
    console.print(f"Running search for: {query}")
    result = serp_api.get_sources(query)
    
    # Print the result
    console.print(result)
    
    # # Show raw data if successful
    # if result.success and result.data:
    #     console.print("\nData Structure:")
    #     console.print(Pretty(result.data))