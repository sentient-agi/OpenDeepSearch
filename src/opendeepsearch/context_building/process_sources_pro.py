from dataclasses import dataclass
from typing import List, Optional, Tuple
from opendeepsearch.context_scraping.crawl4ai_scraper import WebScraper
from opendeepsearch.ranking_models.infinity_rerank import InfinitySemanticSearcher
from opendeepsearch.ranking_models.jina_reranker import JinaReranker
from opendeepsearch.ranking_models.chunker import Chunker 

@dataclass
class Source:
    link: str
    html: str = ""
    # Add other relevant fields here

class SourceProcessor:
    def __init__(
        self, 
        top_results: int = 5,
        strategies: List[str] = ["no_extraction"],
        filter_content: bool = True,
        reranker: str = "infinity"
    ):
        self.strategies = strategies
        self.filter_content = filter_content
        self.scraper = WebScraper(
            strategies=self.strategies, 
            filter_content=self.filter_content
        )
        self.top_results = top_results
        self.chunker = Chunker(
            chunk_size=1024,  # 1 KB chunks
            chunk_overlap=150,  # 256 characters overlap
        )
        
        # Initialize the appropriate reranker
        if reranker.lower() == "jina":
            self.semantic_searcher = JinaReranker()
            print("Using Jina Reranker")
        else:  # default to infinity
            self.semantic_searcher = InfinitySemanticSearcher()
            print("Using Infinity Reranker")

    async def process_sources(
        self, 
        sources: List[dict], 
        num_elements: int, 
        query: str, 
        pro_mode: bool = False,
        chunk: bool = True
    ) -> List[dict]:
        try:
            valid_sources = self._get_valid_sources(sources, num_elements)
            if not valid_sources:
                return sources

            if not pro_mode:
                # Check if there's a Wikipedia article among valid sources
                wiki_sources = [(i, source) for i, source in valid_sources 
                              if 'wikipedia.org' in source['link']]
                if not wiki_sources:
                    return sources.data
                # If Wikipedia article exists, only process that
                valid_sources = wiki_sources # Take only the first Wikipedia source (why?)

            html_contents = await self._fetch_html_contents([s[1]['link'] for s in valid_sources])
            return self._update_sources_with_content(sources.data, valid_sources, html_contents, query, chunk)
        except Exception as e:
            print(f"Error in process_sources: {e}")
            return sources

    def _get_valid_sources(self, sources: List[dict], num_elements: int) -> List[Tuple[int, dict]]:
        return [(i, source) for i, source in enumerate(sources.data['organic'][:num_elements]) if source]

    async def _fetch_html_contents(self, links: List[str]) -> List[str]:
        raw_contents = await self.scraper.scrape_many(links)
        return [x['no_extraction'].content for x in raw_contents.values()]

    def _process_html_content(self, html: str, query: str, chunk: bool = True) -> str:
        if not html:
            return ""
        try:
            # Split the HTML content into chunks
            if chunk:
                documents = self.chunker.split_text(html)
            
            # Rerank the chunks based on the query
            reranked_content = self.semantic_searcher.get_reranked_documents(
                query,
                documents,
                top_k=self.top_results
            )
            
            return reranked_content
        
        except Exception as e:
            print(f"Error in content processing: {e}")
            return ""

    def _update_sources_with_content(
        self, 
        sources: List[dict],
        valid_sources: List[Tuple[int, dict]], 
        html_contents: List[str],
        query: str,
        chunk: bool = True
    ) -> List[dict]:
        for (i, source), html in zip(valid_sources, html_contents):
            source['html'] = self._process_html_content(html, query, chunk)
            # sources[i] = source
        return sources