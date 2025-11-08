import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file in the `backend` directory
load_dotenv()

FMP_API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/api/v3"

def get_company_profile(symbol: str):
    """Fetches the company profile (description, industry, etc.) from FMP."""
    if not FMP_API_KEY:
        return {"error": "FMP API key not found."}
    try:
        url = f"{BASE_URL}/profile/{symbol}?apikey={FMP_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching company profile for {symbol}: {e}")
        return []

def get_quote(symbol: str):
    """Fetches the latest quote data (price, change, volume, etc.) from FMP."""
    if not FMP_API_KEY:
        return {"error": "FMP API key not found."}
    try:
        url = f"{BASE_URL}/quote/{symbol}?apikey={FMP_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching quote for {symbol}: {e}")
        return []

def get_financial_statements(symbol: str, statement_type: str, period: str = "annual", limit: int = 5):
    """Fetches financial statements (income-statement, balance-sheet, cash-flow) from FMP."""
    if not FMP_API_KEY:
        return {"error": "FMP API key not found."}
    try:
        url = f"{BASE_URL}/{statement_type}/{symbol}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {statement_type} for {symbol}: {e}")
        return []

def get_key_metrics(symbol: str, period: str = "annual", limit: int = 5):
    """Fetches key metrics (P/E, P/B, Market Cap, ROE, etc.) from FMP."""
    if not FMP_API_KEY:
        return {"error": "FMP API key not found."}
    try:
        url = f"{BASE_URL}/key-metrics/{symbol}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching key metrics for {symbol}: {e}")
        return []

def get_financial_ratios(symbol: str, period: str = "annual", limit: int = 5):
    """Fetches detailed financial ratios (current ratio, debt to equity, etc.) from FMP."""
    if not FMP_API_KEY:
        return {"error": "FMP API key not found."}
    try:
        url = f"{BASE_URL}/ratios/{symbol}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching financial ratios for {symbol}: {e}")
        return []

def get_analyst_ratings(symbol: str, limit: int = 100):
    """Fetches analyst ratings and recommendations from FMP."""
    if not FMP_API_KEY:
        return {"error": "FMP API key not found."}
    try:
        url = f"{BASE_URL}/rating/{symbol}?limit={limit}&apikey={FMP_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching analyst ratings for {symbol}: {e}")
        return []

def get_shareholding_data(symbol: str, limit: int = 100):
    """
    Fetches institutional shareholding data from FMP.
    This will be used to create the shareholding pattern charts.
    """
    if not FMP_API_KEY:
        return {"error": "FMP API key not found."}
    try:
        url = f"{BASE_URL}/institutional-holder/{symbol}?limit={limit}&apikey={FMP_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching shareholding data for {symbol}: {e}")
        return []