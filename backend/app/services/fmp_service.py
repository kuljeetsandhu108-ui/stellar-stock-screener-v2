import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

FMP_API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/api/v3"
BASE_URL_V4 = "https://financialmodelingprep.com/api/v4"

# --- HIGH-END OPTIMIZATION: PERSISTENT SESSION ---
# Reuses TCP connections to reduce latency/overhead on repeated requests
session = requests.Session()

def _fetch(url: str, params: dict = None):
    """
    Internal helper for high-performance fetching with error handling.
    """
    if not FMP_API_KEY: return None
    
    # Append API key to params
    if params is None: params = {}
    params['apikey'] = FMP_API_KEY
    
    try:
        # 5-second timeout prevents server hangs
        response = session.get(url, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        # Silent fail to keep app running
        # print(f"FMP Fetch Error: {e}") 
        return None

# ==========================================
# 1. SEARCH & CORE (Optimized)
# ==========================================

def search_ticker(query: str, limit: int = 10):
    """
    Primary Search Engine.
    """
    endpoint = f"{BASE_URL}/search"
    # Ensure limit is passed correctly to FMP
    params = {'query': query, 'limit': limit}
    res = _fetch(endpoint, params)
    return res if res else []

def get_company_profile(symbol: str):
    """
    Backup Profile Data (Description, Website, Sector).
    """
    endpoint = f"{BASE_URL}/profile/{symbol}"
    res = _fetch(endpoint)
    return res[0] if res and isinstance(res, list) else {}

# ==========================================
# 2. FINANCIALS (BACKUP ENGINE)
# ==========================================

def get_financial_statements(symbol: str, statement_type: str, period: str = "annual", limit: int = 5):
    """
    Fetches Income/Balance/CashFlow.
    Used if EODHD returns empty data.
    statement_type: 'income-statement', 'balance-sheet-statement', 'cash-flow-statement'
    """
    endpoint = f"{BASE_URL}/{statement_type}/{symbol}"
    params = {'period': period, 'limit': limit}
    res = _fetch(endpoint, params)
    return res if res else []

# ==========================================
# 3. ANALYSTS & NEWS (PRIMARY SOURCE)
# ==========================================

def get_analyst_ratings(symbol: str):
    """
    Fetches Buy/Sell/Hold ratings.
    """
    endpoint = f"{BASE_URL}/rating/{symbol}"
    params = {'limit': 1}
    res = _fetch(endpoint, params)
    return res if res else []

def get_price_target_consensus(symbol: str):
    """
    Fetches High/Low/Avg Price Targets.
    """
    endpoint = f"{BASE_URL}/price-target-consensus/{symbol}"
    res = _fetch(endpoint)
    return res[0] if res and isinstance(res, list) else {}

def get_shareholding_data(symbol: str):
    """
    Fetches Institutional Holders.
    """
    endpoint = f"{BASE_URL}/institutional-holder/{symbol}"
    res = _fetch(endpoint)
    return res if res else []

# ==========================================
# 4. PEERS & METRICS (V4 UPGRADE)
# ==========================================

def get_stock_peers(symbol: str):
    """
    Uses FMP V4 endpoint for better peer matching.
    """
    endpoint = f"{BASE_URL_V4}/stock_peers"
    params = {'symbol': symbol}
    res = _fetch(endpoint, params)
    # V4 returns: [{"symbol": "AAPL", "peersList": [...]}]
    if res and isinstance(res, list) and 'peersList' in res[0]:
        return res[0]['peersList']
    return []

def get_peers_with_metrics(symbols: list):
    """
    BULK FETCH: Gets TTM Metrics for multiple stocks in ONE call.
    Drastically reduces server load for the Peers Tab.
    """
    if not symbols: return []
    symbols_str = ",".join(symbols)
    endpoint = f"{BASE_URL}/key-metrics-ttm/{symbols_str}"
    res = _fetch(endpoint)
    return res if res else []

# ==========================================
# 5. TECHNICAL BACKUP (HYBRID STRATEGY)
# ==========================================

def get_technical_indicator_backup(symbol: str, indicator: str, period: int = 14):
    """
    Direct API fetch for RSI/SMA/EMA.
    Only used if local calculations on EODHD chart data fail.
    """
    # Map common names to FMP types
    # indicators: rsi, sma, ema, wma, dema, tema, williams, adx
    endpoint = f"{BASE_URL}/technical_indicator/1day/{symbol}"
    params = {'type': indicator, 'period': period}
    
    res = _fetch(endpoint, params)
    
    if res and isinstance(res, list) and len(res) > 0:
        # FMP returns list of objects: [{'date':..., 'rsi': 55.4}, ...]
        # We need the most recent value
        return res[0].get(indicator)
    return None