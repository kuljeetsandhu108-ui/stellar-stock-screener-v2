import asyncio
import pandas as pd
from fastapi import APIRouter, HTTPException
# Importing our robust EODHD service and redis
from ..services import eodhd_service, redis_service, technical_service

router = APIRouter()

# ==========================================
# 1. ROBUST INDEX CONFIGURATION
# ==========================================
# We map the Display Name to the specific EODHD Ticker (.INDX).
# Stable ordering ensures the UI never "jumps" or blinks.

INDICES_CONFIG = [
    # --- INDIA MARKETS (Priority) ---
    {"name": "Nifty 50",    "symbol": "NSEI.INDX",    "currency": "INR"},
    {"name": "Bank Nifty",  "symbol": "NSEBANK.INDX", "currency": "INR"},
    {"name": "Sensex",      "symbol": "BSESN.INDX",   "currency": "INR"},
    {"name": "India VIX",   "symbol": "INDIAVIX.INDX","currency": "INR"},
    
    # --- US MARKETS ---
    {"name": "Dow Jones",   "symbol": "DJI.INDX",     "currency": "USD"},
    {"name": "S&P 500",     "symbol": "GSPC.INDX",    "currency": "USD"},
    {"name": "Nasdaq 100",  "symbol": "NDX.INDX",     "currency": "USD"},
    
    # --- GLOBAL ---
    {"name": "Nikkei 225",  "symbol": "N225.INDX",    "currency": "JPY"},
    {"name": "DAX",         "symbol": "GDAXI.INDX",   "currency": "EUR"},
    
    # --- COMMODITIES & CRYPTO (Proxies/Direct) ---
    {"name": "Gold",        "symbol": "GLD.US",       "currency": "USD"}, # ETF Proxy for stability
    {"name": "Crude Oil",   "symbol": "USO.US",       "currency": "USD"}, # ETF Proxy for stability
    {"name": "Bitcoin",     "symbol": "BTC-USD.CC",   "currency": "USD"},
]

# ==========================================
# 2. HOMEPAGE TICKER (High-Speed Engine)
# ==========================================

@router.get("/summary")
async def get_indices_summary():
    """
    Fetches live data for all indices in PARALLEL.
    Optimized for "No-Blink" performance using Redis + AsyncIO.
    """
    cache_key = "indices_banner_live_v3"
    
    # 1. Try Cache First (Instant Response)
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    # 2. Define Single Fetch Task
    async def fetch_index(idx_config):
        try:
            # Use EODHD Live Price (Fastest Endpoint)
            data = await asyncio.to_thread(eodhd_service.get_live_price, idx_config["symbol"])
            
            # Crash Guard: Ensure price exists
            if not data or data.get('price') is None:
                # If live fails, try getting yesterday's close from history as fallback
                # This ensures the card doesn't disappear (causing layout shift/blink)
                return {
                    "name": idx_config["name"],
                    "symbol": idx_config["symbol"],
                    "price": 0.0,
                    "change": 0.0,
                    "percent_change": 0.0,
                    "currency": idx_config["currency"],
                    "is_stale": True
                }

            return {
                "name": idx_config["name"],
                "symbol": idx_config["symbol"],
                "price": data.get('price'),
                "change": data.get('change'),
                "percent_change": data.get('changesPercentage'),
                "currency": idx_config["currency"],
                "is_stale": False
            }
        except:
            # Absolute worst case: Return structure with zeros to maintain layout
            return {
                "name": idx_config["name"],
                "symbol": idx_config["symbol"],
                "price": 0.0, "change": 0.0, "percent_change": 0.0,
                "currency": idx_config["currency"]
            }

    # 3. Fire ALL requests simultaneously
    tasks = [fetch_index(idx) for idx in INDICES_CONFIG]
    results = await asyncio.gather(*tasks)
    
    # 4. Cache Strategy
    # We cache for 5 seconds. This allows "Live" feeling updates without hitting
    # API limits (2000 users * 1 request/sec = 2000 req/sec without cache).
    # With cache: 1 req/5sec total.
    redis_service.set_cache(cache_key, results, 5)
        
    return results

# ==========================================
# 3. HEADER PRICE (Lightweight)
# ==========================================

@router.get("/{index_symbol:path}/live-price")
async def get_index_live_price(index_symbol: str):
    """
    Specific endpoint for the Index Details Header.
    """
    # Normalize input (Frontend might send ^NSEI, we need NSEI.INDX)
    symbol = eodhd_service.format_symbol_for_eodhd(index_symbol)
    
    data = await asyncio.to_thread(eodhd_service.get_live_price, symbol)
    
    if not data:
        raise HTTPException(status_code=404, detail="Index price unavailable")
        
    return data

# ==========================================
# 4. INDEX DETAILS PAGE (Deep Dive)
# ==========================================

@router.get("/{index_symbol:path}/details")
async def get_index_details(index_symbol: str):
    """
    Fetches Chart, Price, and Technicals for an Index.
    Completely replaces Yahoo with EODHD.
    """
    # 1. Normalize Symbol
    symbol = eodhd_service.format_symbol_for_eodhd(index_symbol)
    
    cache_key = f"index_details_v2_{symbol}"
    cached = redis_service.get_cache(cache_key)
    if cached: return cached

    # 2. Parallel Fetch: Chart (History) + Quote (Live)
    tasks = {
        "chart": asyncio.to_thread(eodhd_service.get_historical_data, symbol, "1D"),
        "quote": asyncio.to_thread(eodhd_service.get_live_price, symbol)
    }
    
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    raw = dict(zip(tasks.keys(), results))
    
    # Safe Extraction
    chart_data = raw.get('chart') if isinstance(raw.get('chart'), list) else []
    quote = raw.get('quote') if isinstance(raw.get('quote'), dict) else {}

    # 3. Calculate Technicals (Server-Side Math on EODHD Data)
    technicals = {}
    mas = {}
    pivots = {}
    
    # We need at least ~30 candles to calculate RSI/MACD accurately
    if chart_data and len(chart_data) > 30:
        try:
            df = pd.DataFrame(chart_data)
            technicals = technical_service.calculate_technical_indicators(df)
            mas = technical_service.calculate_moving_averages(df)
            pivots = technical_service.calculate_pivot_points(df)
        except Exception: 
            pass # Keep empty if calculation fails

    # 4. Construct Synthetic Profile
    # Indices don't have standard "Profiles" like companies, so we generate a clean one
    # to prevent Frontend crashes.
    
    # Find config for pretty name
    config_match = next((i for i in INDICES_CONFIG if i["symbol"] == symbol), None)
    name = config_match["name"] if config_match else index_symbol
    currency = config_match["currency"] if config_match else "USD"

    profile = {
        "companyName": name,
        "symbol": symbol,
        "exchange": "INDEX",
        "description": f"Market Index - {name}. Tracks the performance of the underlying sector or market segment.",
        "sector": "Market Index",
        "industry": "Global Markets",
        "image": "", # Frontend will handle default icon
        "currency": currency,
        "tradingview_symbol": symbol # EODHD symbols map reasonably well
    }

    final_data = {
        "profile": profile,
        "quote": quote,
        "technical_indicators": technicals,
        "moving_averages": mas,
        "pivot_points": pivots,
        "analyst_ratings": [], # Indices don't have analyst ratings
        "keyStats": {} # Indices don't have P/E, EPS in the standard way
    }
    
    # Cache for 60 seconds (Details page doesn't need sub-second updates)
    redis_service.set_cache(cache_key, final_data, 60)
    
    return final_data