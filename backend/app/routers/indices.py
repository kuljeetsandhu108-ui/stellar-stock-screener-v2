import asyncio
import pandas as pd
from fastapi import APIRouter, HTTPException
# Import robust services
from ..services import eodhd_service, redis_service, technical_service

router = APIRouter()

# ==========================================
# 1. GLOBAL INDICES CONFIGURATION
# ==========================================

INDICES_CONFIG = [
    # --- INDIA MARKETS (Priority) ---
    {"name": "Nifty 50",    "symbol": "NSEI.INDX",    "currency": "INR"},
    {"name": "Bank Nifty",  "symbol": "NSEBANK.INDX", "currency": "INR"},
    {"name": "Sensex",      "symbol": "BSESN.INDX",   "currency": "INR"},
    {"name": "India VIX",   "symbol": "INDIAVIX.INDX","currency": "INR"},
    
    # --- COMMODITIES ---
    {"name": "Gold (Global)", "symbol": "XAU-USD.CC", "currency": "USD"}, 
    {"name": "Crude Oil",     "symbol": "USO.US",     "currency": "USD"}, 
    
    # --- US MARKETS ---
    {"name": "Dow Jones",   "symbol": "DJI.INDX",     "currency": "USD"},
    {"name": "S&P 500",     "symbol": "GSPC.INDX",    "currency": "USD"},
    {"name": "Nasdaq 100",  "symbol": "NDX.INDX",     "currency": "USD"},
    
    # --- GLOBAL ---
    {"name": "Nikkei 225",  "symbol": "N225.INDX",    "currency": "JPY"},
    {"name": "DAX",         "symbol": "GDAXI.INDX",   "currency": "EUR"},
    
    # --- CRYPTO ---
    {"name": "Bitcoin",     "symbol": "BTC-USD.CC",   "currency": "USD"},
]

# ==========================================
# 2. HOMEPAGE TICKER (BULK + CACHED)
# ==========================================

@router.get("/summary")
async def get_indices_summary():
    """
    Fetches ALL indices in ONE single API call.
    Includes robust 'NA' handling to prevent 500 Errors.
    """
    cache_key = "indices_banner_v6_fix"
    
    # 1. Check Cache (Async)
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached

    # 2. Fetch Bulk Data
    symbols_list = [item["symbol"] for item in INDICES_CONFIG]
    raw_data = await asyncio.to_thread(eodhd_service.get_real_time_bulk, symbols_list)
    
    # 3. Map Results
    data_map = {}
    if raw_data and isinstance(raw_data, list):
        data_map = {item['code']: item for item in raw_data}
    elif raw_data and isinstance(raw_data, dict):
        data_map = {raw_data['code']: raw_data}

    final_results = []
    
    # --- SAFE FLOAT CONVERTER ---
    def safe_float(val):
        try:
            if val is None or val == 'NA' or val == 'None': return 0.0
            return float(val)
        except: return 0.0

    for config in INDICES_CONFIG:
        ticker = config["symbol"]
        code_only = ticker.split('.')[0] 
        
        # Try finding by full ticker or just code
        market_data = data_map.get(ticker) or data_map.get(code_only)
        
        if market_data:
            final_results.append({
                "name": config["name"],
                "symbol": config["symbol"],
                "price": safe_float(market_data.get('close') or market_data.get('previousClose')),
                "change": safe_float(market_data.get('change')),
                "percent_change": safe_float(market_data.get('change_p')),
                "currency": config["currency"]
            })
        else:
            # Fallback for missing data so UI doesn't break
            final_results.append({
                "name": config["name"],
                "symbol": config["symbol"],
                "price": 0.0, "change": 0.0, "percent_change": 0.0,
                "currency": config["currency"]
            })

    # 4. Cache Result (Short TTL for live feel)
    has_data = any(x['price'] > 0 for x in final_results)
    if has_data:
        await redis_service.redis_client.set_cache(cache_key, final_results, 10)
    
    return final_results

@router.get("/market-mood")
async def get_market_mood():
    """
    Calculates the Stellar Market Mood Index (MMI) 0-100.
    Uses India VIX, Nifty RSI, and Nifty Trend Distance.
    """
    cache_key = "stellar_mmi_v1"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached

    try:
        # Fetch Nifty 50 Daily History & Live India VIX
        tasks = {
            "nifty": asyncio.to_thread(eodhd_service.get_historical_data, "NSEI.INDX", "1D"),
            "vix": asyncio.to_thread(eodhd_service.get_live_price, "INDIAVIX.INDX")
        }
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        raw = dict(zip(tasks.keys(), results))
        
        nifty_data = raw.get("nifty")
        vix_data = raw.get("vix")

        mmi = 50.0
        status = "Neutral"

        if nifty_data and len(nifty_data) > 50 and vix_data:
            # 1. Volatility Proxy (India VIX)
            vix = float(vix_data.get('price', 15.0))
            # VIX mapped to 0-100 (Inverse: High VIX = Fear/0, Low VIX = Greed/100)
            vix_score = max(0, min(100, 100 - ((vix - 10) / 15) * 100))

            # 2. Momentum Proxy (Nifty RSI)
            df = pd.DataFrame(nifty_data)
            techs = technical_service.calculate_technical_indicators(df)
            mas = technical_service.calculate_moving_averages(df)
            
            rsi = float(techs.get('rsi', 50))
            
            # 3. Trend Proxy (Distance from 50 SMA)
            price = float(nifty_data[-1]['close'])
            sma50 = float(mas.get('50', price))
            diff = (price - sma50) / sma50
            # Diff mapping: -5% = Fear(0), +5% = Greed(100)
            trend_score = max(0, min(100, 50 + (diff * 10) * 100))

            # Weighted Synthesis
            mmi = (vix_score * 0.40) + (rsi * 0.40) + (trend_score * 0.20)

        # Categorize Sentiment
        if mmi <= 30: 
            status = "Extreme Fear"
            desc = "suggests a good time to open fresh positions, as markets are likely to be oversold and might turn upwards."
            color = "#10B981" # Green
        elif mmi <= 50: 
            status = "Fear"
            desc = "suggests investors are fearful. Market may be presenting value opportunities."
            color = "#34D399" # Light Green
        elif mmi <= 70: 
            status = "Greed"
            desc = "suggests investors are acting greedily. Caution is advised as markets may be overvalued."
            color = "#F59E0B" # Orange
        else: 
            status = "Extreme Greed"
            desc = "suggests a good time to book profits or hedge, as markets are likely to be overbought and might turn downwards."
            color = "#EF4444" # Red

        res = {"mmi": round(mmi, 2), "status": status, "description": desc, "color": color}
        await redis_service.redis_client.set_cache(cache_key, res, 300) # 5 Min Cache
        return res
    except Exception as e:
        return {"mmi": 50.0, "status": "Neutral", "description": "Analyzing market data...", "color": "#EDBB5A"}

# ==========================================
# 3. HEADER PRICE (Index Details)
# ==========================================

@router.get("/{index_symbol:path}/live-price")
async def get_index_live_price(index_symbol: str):
    symbol = eodhd_service.format_symbol_for_eodhd(index_symbol)
    data = await asyncio.to_thread(eodhd_service.get_live_price, symbol)
    if not data: raise HTTPException(status_code=404, detail="Unavailable")
    return data

# ==========================================
# 4. INDEX DETAILS PAGE (CHART + TECHS)
# ==========================================

@router.get("/{index_symbol:path}/details")
async def get_index_details(index_symbol: str):
    symbol = eodhd_service.format_symbol_for_eodhd(index_symbol)
    cache_key = f"index_details_v4_{symbol}"
    
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached

    # Parallel Fetch
    tasks = {
        "chart": asyncio.to_thread(eodhd_service.get_historical_data, symbol, "1D"),
        "quote": asyncio.to_thread(eodhd_service.get_live_price, symbol)
    }
    
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    raw = dict(zip(tasks.keys(), results))
    
    chart_data = raw.get('chart', [])
    quote = raw.get('quote', {})

    # Calculate Technicals
    technicals, mas, pivots = {}, {}, {}
    if chart_data and len(chart_data) > 30:
        try:
            df = pd.DataFrame(chart_data)
            technicals = technical_service.calculate_technical_indicators(df)
            mas = technical_service.calculate_moving_averages(df)
            pivots = technical_service.calculate_pivot_points(df)
        except: pass

    # Profile Construction
    config_match = next((i for i in INDICES_CONFIG if i["symbol"] == symbol), None)
    name = config_match["name"] if config_match else index_symbol
    curr = config_match["currency"] if config_match else "USD"

    profile = {
        "companyName": name, 
        "symbol": symbol, 
        "exchange": "INDEX",
        "description": f"Global Market Index - {name}", 
        "sector": "Market Index",
        "industry": "Indices", 
        "image": "", 
        "currency": curr,
        "tradingview_symbol": symbol
    }

    final_data = {
        "profile": profile, 
        "quote": quote,
        "technical_indicators": technicals, 
        "moving_averages": mas, 
        "pivot_points": pivots,
        "analyst_ratings": [], 
        "keyStats": {}
    }
    
    await redis_service.redis_client.set_cache(cache_key, final_data, 60)
    return final_data
