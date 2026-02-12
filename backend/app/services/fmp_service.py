import os
import requests
from datetime import datetime
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
        # 4-second timeout prevents server hangs on slow external API calls
        response = session.get(url, params=params, timeout=4)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        # Silent fail to keep app running
        return None

# ==========================================
# 1. SEARCH & CORE (Optimized)
# ==========================================

def search_ticker(query: str, limit: int = 10):
    """
    Primary Search Engine.
    """
    endpoint = f"{BASE_URL}/search"
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
    if res and isinstance(res, list) and len(res) > 0 and 'peersList' in res[0]:
        return res[0]['peersList']
    return []

def get_peers_with_metrics(symbols: list):
    """
    BULK FETCH: Gets TTM Metrics for multiple stocks in ONE call.
    """
    if not symbols: return []
    
    # FMP format: RELIANCE.NS,TCS.NS
    # Remove any internal suffixes if necessary, but FMP usually handles .NS fine
    query = ",".join(symbols)
    
    # Endpoint: Key Metrics TTM
    endpoint = f"{BASE_URL}/key-metrics-ttm/{query}"
    res = _fetch(endpoint)
    return res if res else []

# ==========================================
# 5. CHARTING ENGINE (HIGH-SPEED PROCESSING)
# ==========================================

def process_fmp_candles(raw_list: list):
    """
    High-Speed Processor:
    1. Slices data (Max 750 candles) for instant loading.
    2. Parses dates safely.
    3. Sorts Oldest -> Newest.
    """
    if not raw_list: return []
    
    # --- SPEED FIX: SLICING ---
    # FMP returns Newest -> Oldest. We only need the recent data.
    # Limiting to 750 candles prevents the loop from running 5000+ times.
    sliced_list = raw_list[:750] 
    
    data = []
    for candle in sliced_list:
        date_str = candle.get('date')
        if not date_str: continue
        
        try:
            # Parse Date
            if ":" in date_str:
                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            else:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
            
            ts = int(dt.timestamp())
            
            # Safe Float Conversion
            o = float(candle.get('open') or 0)
            h = float(candle.get('high') or 0)
            l = float(candle.get('low') or 0)
            c = float(candle.get('close') or 0)
            v = float(candle.get('volume') or 0)
            
            if c > 0: 
                data.append({
                    "time": ts,
                    "open": o, "high": h, "low": l, "close": c, "volume": v
                })
        except: continue
    
    # Sort Oldest -> Newest (Required for Chart)
    data.sort(key=lambda x: x['time'])
    return data

def get_commodity_history(symbol: str, range_type: str = "1d"):
    """
    Fetches Commodity History from FMP (XAUUSD, CLUSD).
    """
    if not FMP_API_KEY: return []
    
    # Map Range to FMP Interval
    interval = "5min"
    if range_type in ["1H", "4H"]: interval = "1hour"
    elif range_type == "15M": interval = "15min"
    
    # API Endpoint
    # e.g. https://financialmodelingprep.com/api/v3/historical-chart/5min/CLUSD
    url = f"{BASE_URL}/historical-chart/{interval}/{symbol}?apikey={FMP_API_KEY}"
    
    # If Daily History, FMP uses a different endpoint structure
    if range_type in ["1W", "1M", "1D"] and interval == "5min":
        url = f"{BASE_URL}/historical-price-full/{symbol}?apikey={FMP_API_KEY}"

    res = _fetch(url)
    
    # Normalize Response: Daily returns { symbol:..., historical: [...] }
    raw_data = []
    if isinstance(res, dict) and 'historical' in res:
        raw_data = res['historical']
    elif isinstance(res, list):
        raw_data = res
    
    # Send to the Slicer for speed
    return process_fmp_candles(raw_data)

def get_crypto_history(symbol: str, range_type: str = "1D"):
    """
    Fetches Crypto Candles (BTCUSD).
    """
    if not FMP_API_KEY: return []
    
    # Intraday Logic
    interval = "5min"
    is_intraday = range_type in ["5M", "15M", "1H", "4H"]
    
    if range_type == "15M": interval = "15min"
    if range_type == "1H": interval = "1hour"
    if range_type == "4H": interval = "4hour"
    
    if is_intraday:
        url = f"{BASE_URL}/historical-chart/{interval}/{symbol}?apikey={FMP_API_KEY}"
    else:
        # Daily/Weekly
        url = f"{BASE_URL}/historical-price-full/{symbol}?apikey={FMP_API_KEY}"

    res = _fetch(url)
    
    raw_data = []
    if isinstance(res, dict) and 'historical' in res:
        raw_data = res['historical']
    elif isinstance(res, list):
        raw_data = res
    
    # Use the Slicer
    return process_fmp_candles(raw_data)
# ==========================================
# 6. REAL-TIME QUOTES (HIGH SPEED)
# ==========================================

def get_quote(symbol: str):
    """
    Fetches Live Price for Commodities/Stocks from FMP.
    Structure matches EODHD quote for seamless frontend integration.
    """
    if not FMP_API_KEY: return {}
    
    endpoint = f"{BASE_URL}/quote/{symbol}"
    res = _fetch(endpoint)
    
    if res and isinstance(res, list) and len(res) > 0:
        data = res[0]
        return {
            "price": data.get('price'),
            "change": data.get('change'),
            "changesPercentage": data.get('changesPercentage'),
            "dayLow": data.get('dayLow'),
            "dayHigh": data.get('dayHigh'),
            "yearHigh": data.get('yearHigh'),
            "yearLow": data.get('yearLow'),
            "volume": data.get('volume'),
            "previousClose": data.get('previousClose'),
            "open": data.get('open'),
            "timestamp": data.get('timestamp')
        }
    return {}

def get_crypto_real_time_bulk(symbols: list):
    """
    Fetches Live Prices for multiple Cryptos in 1 call.
    Used for the Stream Engine.
    """
    if not FMP_API_KEY or not symbols: return []
    
    # FMP format: BTCUSD,ETHUSD
    # Ensure symbols are clean (remove .CC or -USD if passed)
    clean_syms = [s.replace("-USD.CC", "USD").replace("-", "").replace(".CC", "") for s in symbols]
    query = ",".join(clean_syms)
    
    endpoint = f"{BASE_URL}/quote/{query}"
    return _fetch(endpoint) or []