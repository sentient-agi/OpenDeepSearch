import os
import json
from serpapi import GoogleSearch

search = GoogleSearch({
    "q": "What is elon musk's net worth?", 
    "location": "United Kingdom",
    "api_key": os.getenv("SERPAPI_API_KEY"),
    "num": 10
  })

result = search.get_dict()

# print(json.dumps(result, indent=2))


class SerpApiAdapter:
    def extract_fields(self, items_list, fields_to_extract, field_mapping=None):
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
                source_field = field_mapping.get(target_field, target_field)
                extracted_item[target_field] = item.get(source_field)
            extracted_items.append(extracted_item)
        return extracted_items

    def format_serpapi_response(self, serp_api_data):
        """
        Formats SerpAPI response to the desired internal structure.
        Handles missing keys gracefully by defaulting to empty lists or None.
        """
        if not isinstance(serp_api_data, dict):
            # Handle cases where serp_api_data might not be a dictionary (e.g. error response)
            # You might want to return a default error structure or raise an exception
            print("Warning: serp_api_data is not a dictionary.")
            return { # Return an empty structure matching the target
                'organic': [], 'topStories': [], 'images': [],
                'graph': None, 'answerBox': None,
                'peopleAlsoAsk': [], 'relatedSearches': []
            }

        results = {
            'organic': self.extract_fields(
                serp_api_data.get('organic_results', []),
                ['title', 'link', 'snippet', 'date']
                # Note: 'date' will be None if not present in individual organic_results items.
                # For more advanced date extraction, you might need to inspect item.get('rich_snippet', {})... etc.
            ),
            'topStories': self.extract_fields(
                # SerpAPI might use 'top_stories' or 'news_results'
                serp_api_data.get('top_stories', serp_api_data.get('news_results', [])),
                ['title', 'imageUrl'],
                {'imageUrl': 'thumbnail'} # Map 'thumbnail' from SerpAPI to 'imageUrl'
            ),
            'images': self.extract_fields(
                # SerpAPI might use 'images_results' or 'inline_images'
                (serp_api_data.get('images_results', serp_api_data.get('inline_images', [])))[:6],
                ['title', 'imageUrl'],
                {'imageUrl': 'thumbnail'} # Map 'thumbnail' from SerpAPI to 'imageUrl'
                                          # or use 'original' for full-size image
            ),
            'graph': serp_api_data.get('knowledge_graph'),
            'answerBox': serp_api_data.get('answer_box'),
            'peopleAlsoAsk': serp_api_data.get('people_also_ask', []), # Expects top-level PAA
            'relatedSearches': serp_api_data.get('related_searches', [])
        }
        return results
    

serp_api_adapter = SerpApiAdapter()

print(json.dumps(serp_api_adapter.format_serpapi_response(result), indent=2))