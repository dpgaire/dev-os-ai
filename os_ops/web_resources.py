import requests
from googlesearch import search
from typing import List, Optional

class WebResourceFinder:
    @staticmethod
    def search_web(query: str, num_results: int = 3) -> List[str]:
        try:
            return list(search(query, num_results=num_results))
        except Exception as e:
            return [f"Search error: {str(e)}"]

    @staticmethod
    def get_page_content(url: str) -> Optional[str]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.text[:2000]  # Return first 2000 chars
        except Exception as e:
            return f"Error fetching URL: {str(e)}"