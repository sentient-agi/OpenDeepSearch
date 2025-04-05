from typing import List, Dict, Optional
from loguru import logger
from langchain.text_splitter import RecursiveCharacterTextSplitter


def extract_information(organic_results: List[Dict]) -> List[str]:
    """Extract snippets from organic search results in a formatted string."""
    formatted_results = []
    for item in organic_results:
        if 'snippet' in item:
            result_parts = [
                f"title: {item.get('title', 'N/A')}",
                f"date authored: {item.get('date', 'N/A')}",
                f"link: {item.get('link', 'N/A')}",
                f"snippet: {item['snippet']}"
            ]
            
            if 'html' in item:
                result_parts.append(f"additional information: {item['html']}")
            
            formatted_results.append('\n'.join(result_parts))
    
    return formatted_results

def extract_top_stories(top_stories: Optional[List[Dict]]) -> List[str]:
    """Extract titles from top stories."""
    if not top_stories:
        return []
    
    return [
        item['title'] 
        for item in top_stories 
        if 'title' in item
    ]

def extract_answer_box(
    answer_box: Optional[Dict]
) -> List[str]:
    """Extract information from answer box."""
    results = []
    
    if answer_box:
        for key in ['answer', 'snippet']:
            if answer_box.get(key):
                results.append(answer_box[key])
    
    return results

def build_context(
    sources_result: Dict,
) -> str:
    """
    Build context from search results.
    
    Args:
        sources_result: Dictionary containing search results
        
    Returns:
        A formatted string containing all relevant search results
    """
    try:
        # Build context from different components
        organic_results = extract_information(sources_result.get('organic', []))
        top_stories = extract_top_stories(sources_result.get('topStories'))
        answer_box = extract_answer_box(
            sources_result.get('answerBox')
        )
        
        # Combine all results into a single string
        context_parts = []
        
        # Add answer box if available
        if answer_box:
            context_parts.append('\n'.join(answer_box))
        
        # Add organic results
        if organic_results:
            context_parts.append('\n'.join(organic_results))
        
        # Add top stories if available
        if top_stories:
            context_parts.append('\n'.join(top_stories))
        
        return context_parts

    except Exception as e:
        logger.exception(f"An error occurred while building context: {e}")
        return ""  # Return empty string in case of error
