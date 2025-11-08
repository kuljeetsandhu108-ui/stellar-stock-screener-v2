import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file in the `backend` directory
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

def get_company_news(query: str, page_size: int = 20):
    """
    Fetches recent news articles related to a specific company or query
    from the News API. It sorts by the most recently published.
    """
    if not NEWS_API_KEY:
        print("Error: NEWS_API_KEY not found in .env file.")
        return {"error": "News API key not configured."}
    
    # We add quotes around the query for more exact matches
    # e.g., searching for "Apple Inc" instead of just Apple
    params = {
        "q": f'"{query}"',
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        # We extract only the 'articles' list from the response
        return response.json().get("articles", [])
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching company news for '{query}': {e}")
        return []