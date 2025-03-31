from smolagents import Tool
import wolframalpha
import json
import os

class WolframAlphaTool(Tool):
    name = "calculate"
    description = """
    Performs computational, mathematical, and factual queries using Wolfram Alpha's computational knowledge engine.
    """
    inputs = {
        "query": {
            "type": "string",
            "description": "The query to send to Wolfram Alpha",
        },
    }
    output_type = "string"
    
    def __init__(self, app_id: str):
        super().__init__()
        self.app_id = app_id
    
    def setup(self):
        # Initialize the Wolfram Alpha client
        self.wolfram_client = wolframalpha.Client(self.app_id)
        
    def forward(self, query: str):
        try:
            # Send the query to Wolfram Alpha
            res = self.wolfram_client.query(query)
            
            # Process the results
            results = []
            for pod in res.pods:
                if pod.title:
                    for subpod in pod.subpods:
                        if subpod.plaintext:
                            results.append({
                                'title': pod.title,
                                'result': subpod.plaintext
                            })
                            
            # Convert results to a JSON-serializable format
            formatted_result = {
                'queryresult': {
                    'success': bool(results),
                    'inputstring': query,
                    'pods': [
                        {
                            'title': result['title'], 
                            'subpods': [{'title': '', 'plaintext': result['result']}]
                        } for result in results
                    ]
                }
            }
            
            # Initialize final_result with a default value
            final_result = "No result found."
            
            # Extract the pods from the query result
            pods = formatted_result.get("queryresult", {}).get("pods", [])
            
            # Loop through pods to find the "Result" title
            for pod in pods:
                if pod.get("title") == "Result":
                    # Extract and return the plaintext from the subpods
                    subpods = pod.get("subpods", [])
                    if subpods:
                        final_result = subpods[0].get("plaintext", "").strip()
                        break
            
            # If no "Result" pod was found, use the first available result
            if final_result == "No result found." and results:
                final_result = results[0]['result']
                
            
            print(f"QUERY: {query}\n\nRESULT: {final_result}")
            return final_result
            
        except Exception as e:
            error_message = f"Error querying Wolfram Alpha: {str(e)}"
            print(error_message)
            return error_message
    