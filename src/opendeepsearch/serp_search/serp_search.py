import os
from dataclasses import dataclass
from typing import Dict, Any, Optional, List, TypeVar, Generic, Union
from abc import ABC, abstractmethod

from rich.panel import Panel
from rich.tree import Tree
from rich.console import Console
from rich.text import Text

import requests

T = TypeVar('T')

class SearchAPIException(Exception):
    """Custom exception for Search API related errors"""
    pass

class SerperAPIException(SearchAPIException):
    """Custom exception for Serper API related errors"""
    pass

class SearXNGException(SearchAPIException):
    """Custom exception for SearXNG related errors"""
    pass

@dataclass
class SerperConfig:
    """Configuration for Serper API"""
    api_key: str
    api_url: str = "https://google.serper.dev/search"
    default_location: str = 'us'
    timeout: int = 10

    @classmethod
    def from_env(cls) -> 'SerperConfig':
        """Create config from environment variables"""
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            raise SerperAPIException("SERPER_API_KEY environment variable not set")
        return cls(api_key=api_key)

@dataclass
class SearXNGConfig:
    """Configuration for SearXNG instance"""
    instance_url: str
    api_key: Optional[str] = None
    default_location: str = 'all'
    timeout: int = 10

    @classmethod
    def from_env(cls) -> 'SearXNGConfig':
        """Create config from environment variables"""
        instance_url = os.getenv("SEARXNG_INSTANCE_URL")
        if not instance_url:
            raise SearXNGException("SEARXNG_INSTANCE_URL environment variable not set")
        api_key = os.getenv("SEARXNG_API_KEY")  # Optional
        return cls(instance_url=instance_url, api_key=api_key)

class SearchResult(Generic[T]):
    """Container for search results with error handling"""
    def __init__(self, data: Optional[T] = None, error: Optional[str] = None):
        self.data = data
        self.error = error
        self.success = error is None

    @property
    def failed(self) -> bool:
        return not self.success
        
    def __repr__(self) -> str:
        if self.success:
            return f"SearchResult(success={self.success}, data_type={type(self.data).__name__})"
        else:
            return f"SearchResult(success={self.success}, error='{self.error}')"
            
    def __rich__(self) -> str:
        """Rich representation for better formatting in rich-enabled environments"""
        
        if self.success:
            if self.data is None:
                return Panel("[bold green]Success[/bold green]: No data returned", 
                            title="SearchResult", border_style="green", width=100)
                
            if isinstance(self.data, dict):
                # Create tree structure for search results
                tree = Tree("[bold green]Search Results[/bold green]")
                
                # Organic results
                organic_results = self.data.get('organic', [])
                if organic_results:
                    organic_branch = tree.add(f"[yellow]Organic Results[/yellow] ({len(organic_results)})")
                    for i, result in enumerate(organic_results[:5]):  # Show first 3 results
                        title = result.get('title', 'No title')
                        link = result.get('link', 'No link')
                        snippet = result.get('snippet', '')
                        # Truncate snippet if too long
                        if snippet and len(snippet) > 70:
                            snippet = snippet[:67] + "..."
                        
                        result_text = f"[bold cyan]{title}[/bold cyan]\n[blue]{link[:60]}{'...' if len(link) > 60 else ''}[/blue]"
                        if snippet:
                            result_text += f"\n{snippet}"
                        
                        organic_branch.add(result_text)
                    
                    if len(organic_results) > 5:
                        organic_branch.add(f"[dim]... and {len(organic_results) - 5} more results[/dim]")
                
                # Knowledge Graph
                if self.data.get('graph'):
                    graph_branch = tree.add("[yellow]Knowledge Graph[/yellow]")
                    graph_data = self.data['graph']
                    
                    if isinstance(graph_data, dict):
                        title = graph_data.get('title', 'Unknown')
                        description = graph_data.get('description', '')
                        
                        if description and len(description) > 70:
                            description = description[:67] + "..."
                            
                        graph_branch.add(f"[bold cyan]{title}[/bold cyan]")
                        if description:
                            graph_branch.add(description)
                    else:
                        graph_branch.add("[italic]Knowledge graph present[/italic]")
                
                # Answer Box
                if self.data.get('answerBox'):
                    answer_branch = tree.add("[yellow]Answer Box[/yellow]")
                    answer_data = self.data['answerBox']
                    
                    if isinstance(answer_data, dict):
                        title = answer_data.get('title', '')
                        answer = answer_data.get('answer', answer_data.get('snippet', ''))
                        
                        if answer and len(answer) > 100:
                            answer = answer[:97] + "..."
                            
                        if title:
                            answer_branch.add(f"[bold cyan]{title}[/bold cyan]")
                        if answer:
                            answer_branch.add(answer)
                    else:
                        answer_branch.add("[italic]Answer box present[/italic]")
                
                # Other sections as compact summaries
                sections = []
                
                # Top Stories
                top_stories = self.data.get('topStories', [])
                if top_stories:
                    sections.append(f"[yellow]Top Stories[/yellow] ({len(top_stories)})")
                
                # Images
                images = self.data.get('images', [])
                if images:
                    sections.append(f"[yellow]Images[/yellow] ({len(images)})")
                
                # People Also Ask
                paa = self.data.get('peopleAlsoAsk', [])
                if paa:
                    sections.append(f"[yellow]People Also Ask[/yellow] ({len(paa)})")
                
                # Related Searches
                related = self.data.get('relatedSearches', [])
                if related:
                    sections.append(f"[yellow]Related Searches[/yellow] ({len(related)})")
                
                if sections:
                    other_branch = tree.add("[yellow]Other Results[/yellow]")
                    for section in sections:
                        other_branch.add(section)
                
                # Get width of current terminal if possible
                width = 100  # Default width
                try:
                    console = Console()
                    width = min(console.width - 4, 100)  # Subtract some padding and cap at 100
                except:
                    pass
                
                return Panel(tree, title="SearchResult", border_style="green", width=width)
            else:
                return Panel(f"[bold green]Success[/bold green]: {type(self.data).__name__} returned", 
                            title="SearchResult", border_style="green", width=100)
        else:
            return Panel(f"[bold red]Error[/bold red]: {self.error}", 
                        title="SearchResult", border_style="red", width=100)

class SearchAPI(ABC):
    """Abstract base class for search APIs"""
    @abstractmethod
    def get_sources(
        self,
        query: str,
        num_results: int = 8,
        stored_location: Optional[str] = None
    ) -> SearchResult[Dict[str, Any]]:
        """Get search results from the API"""
        pass

class SerperAPI(SearchAPI):
    def __init__(self, api_key: Optional[str] = None, config: Optional[SerperConfig] = None):
        if api_key:
            self.config = SerperConfig(api_key=api_key)
        else:
            self.config = config or SerperConfig.from_env()

        self.headers = {
            'X-API-KEY': self.config.api_key,
            'Content-Type': 'application/json'
        }

    @staticmethod
    def extract_fields(items: List[Dict[str, Any]], fields: List[str]) -> List[Dict[str, Any]]:
        """Extract specified fields from a list of dictionaries"""
        return [{key: item.get(key, "") for key in fields if key in item} for item in items]

    def get_sources(
        self,
        query: str,
        num_results: int = 8,
        stored_location: Optional[str] = None
    ) -> SearchResult[Dict[str, Any]]:
        """
        Fetch search results from Serper API.

        Args:
            query: Search query string
            num_results: Number of results to return (default: 8, max: 10)
            stored_location: Optional location string

        Returns:
            SearchResult containing the search results or error information
        """
        if not query.strip():
            return SearchResult(error="Query cannot be empty")

        try:
            search_location = (stored_location or self.config.default_location).lower()

            payload = {
                "q": query,
                "num": min(max(1, num_results), 10),
                "gl": search_location
            }

            response = requests.post(
                self.config.api_url,
                headers=self.headers,
                json=payload,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            data = response.json()

            results = {
                'organic': self.extract_fields(
                    data.get('organic', []),
                    ['title', 'link', 'snippet', 'date']
                ),
                'topStories': self.extract_fields(
                    data.get('topStories', []),
                    ['title', 'imageUrl']
                ),
                'images': self.extract_fields(
                    data.get('images', [])[:6],
                    ['title', 'imageUrl']
                ),
                'graph': data.get('knowledgeGraph'),
                'answerBox': data.get('answerBox'),
                'peopleAlsoAsk': data.get('peopleAlsoAsk'),
                'relatedSearches': data.get('relatedSearches')
            }

            return SearchResult(data=results)

        except requests.RequestException as e:
            return SearchResult(error=f"API request failed: {str(e)}")
        except Exception as e:
            return SearchResult(error=f"Unexpected error: {str(e)}")


class SearXNGAPI(SearchAPI):
    """API client for SearXNG search engine"""

    def __init__(self, instance_url: Optional[str] = None, api_key: Optional[str] = None, config: Optional[SearXNGConfig] = None):
        if instance_url:
            self.config = SearXNGConfig(instance_url=instance_url, api_key=api_key)
        else:
            self.config = config or SearXNGConfig.from_env()

        self.headers = {'Content-Type': 'application/json'}
        if self.config.api_key:
            self.headers['X-API-Key'] = self.config.api_key

    def get_sources(
        self,
        query: str,
        num_results: int = 8,
        stored_location: Optional[str] = None
    ) -> SearchResult[Dict[str, Any]]:
        """
        Fetch search results from SearXNG instance.

        Args:
            query: Search query string
            num_results: Number of results to return (default: 8)
            stored_location: Optional location string (may not be supported by all instances)

        Returns:
            SearchResult containing the search results or error information
        """
        if not query.strip():
            return SearchResult(error="Query cannot be empty")

        try:
            # Ensure the instance URL ends with /search
            search_url = self.config.instance_url
            if not search_url.endswith('/search'):
                search_url = search_url.rstrip('/') + '/search'

            # Prepare parameters for SearXNG
            params = {
                'q': query,
                'format': 'json',
                'pageno': 1,
                'categories': 'general',
                'language': 'all',
                'time_range': None,
                'safesearch': 0,
                'engines': 'google,bing,duckduckgo',  # Default engines, can be customised
                'max_results': min(max(1, num_results), 20)  # Limit to reasonable range
            }

            # Add location if provided and supported
            if stored_location and stored_location != 'all':
                params['language'] = stored_location

            response = requests.get(
                search_url,
                headers=self.headers,
                params=params,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            data = response.json()

            # Transform SearXNG results to match SerperAPI format
            organic_results = []
            for result in data.get('results', [])[:num_results]:
                organic_results.append({
                    'title': result.get('title', ''),
                    'link': result.get('url', ''),
                    'snippet': result.get('content', ''),
                    'date': result.get('publishedDate', '')
                })

            # Extract image results if available
            image_results = []
            for result in data.get('results', []):
                if result.get('img_src'):
                    image_results.append({
                        'title': result.get('title', ''),
                        'imageUrl': result.get('img_src', '')
                    })
            image_results = image_results[:6]  # Limit to 6 images like SerperAPI

            # Format results to match SerperAPI structure
            results = {
                'organic': organic_results,
                'images': image_results,
                'topStories': [],  # SearXNG might not have direct equivalent
                'graph': None,     # SearXNG doesn't provide knowledge graph
                'answerBox': None, # SearXNG doesn't provide answer box
                'peopleAlsoAsk': None,
                'relatedSearches': data.get('suggestions', [])
            }

            return SearchResult(data=results)

        except requests.RequestException as e:
            return SearchResult(error=f"SearXNG API request failed: {str(e)}")
        except Exception as e:
            return SearchResult(error=f"Unexpected error with SearXNG: {str(e)}")


def create_search_api(
    search_provider: str = "serper",
    serper_api_key: Optional[str] = None,
    searxng_instance_url: Optional[str] = None,
    searxng_api_key: Optional[str] = None
) -> SearchAPI:
    """
    Factory function to create the appropriate search API client.

    Args:
        search_provider: The search provider to use ('serper' or 'searxng')
        serper_api_key: Optional API key for Serper
        searxng_instance_url: Optional SearXNG instance URL
        searxng_api_key: Optional API key for SearXNG instance

    Returns:
        An instance of a SearchAPI implementation

    Raises:
        ValueError: If an invalid search provider is specified
    """
    if search_provider.lower() == "serper":
        return SerperAPI(api_key=serper_api_key)
    elif search_provider.lower() == "searxng":
        return SearXNGAPI(instance_url=searxng_instance_url, api_key=searxng_api_key)
    else:
        raise ValueError(f"Invalid search provider: {search_provider}. Must be 'serper' or 'searxng'")
