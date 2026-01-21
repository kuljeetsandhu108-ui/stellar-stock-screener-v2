import os
import requests
import json
from datetime import datetime, timedelta
import pytz 
from dotenv import load_dotenv

load_dotenv()

EODHD_API_KEY = os.getenv("EODHD_API_KEY")
BASE_URL = "https://eodhd.com/api"

# --- HIGH-END OPTIMIZATION: PERSISTENT SESSION ---
# Keeps the connection open to avoid SSL handshake overhead on every call
session = requests.Session()

# ==========================================
# 1. SMART SYMBOL RESOLVER (TRAINED)
# ==========================================

def format_symbol_for_eodhd(symbol: str) -> str:
    """
    Intelligently maps user inputs to EODHD Tickers.
    Handles Crypto, Indices, and Commodities fallbacks.
    """
    if not symbol: return ""
    symbol = symbol.upper().strip()
    
    # 1. Known Indices (Explicit Map)
    INDICES = {
        "^NSEI": "NSEI.INDX", "NIFTY": "NSEI.INDX", "NIFTY 50": "NSEI.INDX",
        "^NSEBANK": "NSEBANK.INDX", "BANKNIFTY": "NSEBANK.INDX",
        "^BSESN": "BSESN.INDX", "SENSEX": "BSESN.INDX",
        "^GSPC": "GSPC.INDX", "SPX": "GSPC.INDX", "S&P 500": "GSPC.INDX",
        "^DJI": "DJI.INDX", "DOW": "DJI.INDX", "DOW JONES": "DJI.INDX",
        "^IXIC": "IXIC.INDX", "NASDAQ": "IXIC.INDX",
        "^VIX": "INDIAVIX.INDX", "INDIA VIX": "INDIAVIX.INDX",
        "^N225": "N225.INDX", "NIKKEI": "N225.INDX",
        "^GDAXI": "GDAXI.INDX", "DAX": "GDAXI.INDX"
    }
    if symbol in INDICES: return INDICES[symbol]

    # 2. Crypto Logic (The Fix for SOL-USD)
    # If it ends in -USD but doesn't have a dot suffix, add .CC
    if symbol.endswith("-USD") and "." not in symbol:
        return f"{symbol}.CC"
    
    # Common Crypto Shortnames mapping
    CRYPTO_SHORTS = ["BTC", "ETH", "SOL", "XRP", "DOGE", "ADA", "MATIC", "DOT", "LTC", "SHIB", "AVAX"]
    if symbol in CRYPTO_SHORTS:
        return f"{symbol}-USD.CC"

    # 3. Commodity Fallbacks (If FMP fails, EODHD uses ETFs/Futures)
    if symbol in ["USOIL", "WTI", "CRUDE", "CLUSD"]: return "USO.US" # United States Oil Fund
    if symbol in ["GOLD", "XAU", "XAUUSD"]: return "GLD.US" # SPDR Gold Shares
    if symbol in ["SILVER", "XAG", "XAGUSD"]: return "SLV.US" # iShares Silver
    if symbol in ["GAS", "NGUSD", "UNG"]: return "UNG.US" # United States Natural Gas

    # 4. India Mapping
    if symbol.endswith(".NS"): return symbol.replace(".NS", ".NSE")
    if symbol.endswith(".BO"): return symbol.replace(".BO", ".BSE")
    
    # 5. Default US (If no suffix, assume US)
    if "." not in symbol: return f"{symbol}.US"
        
    return symbol

# ==========================================
# 2. DATA FETCHING (NETWORK LAYER)
# ==========================================

def get_company_fundamentals(symbol: str):
    """
    Fetches massive 'All-In-One' Fundamental JSON.
    """
    if not EODHD_API_KEY: return {}
    eod_symbol = format_symbol_for_eodhd(symbol)
    
    try:
        url = f"{BASE_URL}/fundamentals/{eod_symbol}?api_token={EODHD_API_KEY}&fmt=json"
        response = session.get(url, timeout=10) # Longer timeout for large JSON
        
        if response.status_code == 200:
            data = response.json()
            # EODHD returns empty list [] for invalid symbols
            if isinstance(data, list) and not data: return {}
            return data
        return {}
    except: return {}

def get_live_price(symbol: str):
    """
    Fetches real-time price snapshot.
    Includes robustness against 0.00 prices (pre-market issues).
    """
    if not EODHD_API_KEY: return {}
    eod_symbol = format_symbol_for_eodhd(symbol)
    
    try:
        url = f"{BASE_URL}/real-time/{eod_symbol}?api_token={EODHD_API_KEY}&fmt=json"
        # 4s timeout: Fast fail to let fallback happen
        response = session.get(url, timeout=4) 
        
        if response.status_code == 200:
            data = response.json()
            
            # Helper to safely float conversion
            def f(x): 
                try: return float(x)
                except: return 0.0
            
            # Robust Price Parsing: Fallback to previousClose if close is 0
            price = f(data.get('close'))
            if price == 0.0: price = f(data.get('previousClose'))

            return {
                "price": price,
                "change": f(data.get('change')),
                "changesPercentage": f(data.get('change_p')),
                "high": f(data.get('high')),
                "low": f(data.get('low')),
                "volume": f(data.get('volume')),
                "timestamp": data.get('timestamp')
            }
        return {}
    except: return {}

def get_real_time_bulk(symbols: list):
    """
    Fetches MULTIPLE real-time prices (Credit Saver).
    Used by Stream Hub to update 50 stocks with 1 API credit.
    """
    if not EODHD_API_KEY or not symbols: return []
    
    try:
        # Normalize all
        clean_symbols = [format_symbol_for_eodhd(s) for s in symbols if s]
        if not clean_symbols: return []

        primary = clean_symbols[0]
        others = ",".join(clean_symbols[1:])
        
        url = f"{BASE_URL}/real-time/{primary}?api_token={EODHD_API_KEY}&fmt=json&s={others}"
        response = session.get(url, timeout=6)
        
        if response.status_code == 200:
            data = response.json()
            # If only 1 result, EODHD returns dict. If multiple, returns list.
            if isinstance(data, dict): return [data] 
            return data
        return []
    except: return []

def get_historical_data(symbol: str, range_type: str = "1d"):
    """
    Fetches Chart Data.
    Features: 
    1. IST Timezone alignment for India.
    2. Null value filtering (Crucial for Charts).
    """
    if not EODHD_API_KEY: return []
    eod_symbol = format_symbol_for_eodhd(symbol)
    data = []
    
    # Identify Indian Assets for Timezone Offset (5h 30m = 19800s)
    is_indian = ".NSE" in eod_symbol or ".BSE" in eod_symbol or ".INDX" in eod_symbol
    offset = 19800 if is_indian else 0

    try:
        is_intraday = range_type in ["5M", "15M", "1H", "4H"]
        
        if is_intraday:
            # Fetch last 30 days of 5m data (Master Dataset)
            ts_from = int((datetime.now() - timedelta(days=30)).timestamp())
            url = f"{BASE_URL}/intraday/{eod_symbol}?api_token={EODHD_API_KEY}&interval=5m&from={ts_from}&fmt=json"
        else:
            # Daily History (3 Years)
            from_date = (datetime.now() - timedelta(days=1095)).strftime('%Y-%m-%d')
            url = f"{BASE_URL}/eod/{eod_symbol}?api_token={EODHD_API_KEY}&period=d&from={from_date}&fmt=json"

        response = session.get(url, timeout=10)
        
        if response.status_code == 200:
            raw_data = response.json()
            
            for candle in raw_data:
                try:
                    ts = 0
                    # Parse EOD Date (YYYY-MM-DD)
                    if "date" in candle:
                        dt = datetime.strptime(candle['date'], "%Y-%m-%d")
                        ts = int(dt.replace(tzinfo=pytz.utc).timestamp())
                    # Parse Intraday Date (YYYY-MM-DD HH:MM:SS)
                    elif "datetime" in candle:
                        dt = datetime.strptime(candle['datetime'], "%Y-%m-%d %H:%M:%S")
                        base_ts = int(dt.replace(tzinfo=pytz.utc).timestamp())
                        # Apply IST Offset for Indian Intraday
                        ts = base_ts + offset if is_intraday else base_ts
                    
                    # 4. CRASH PROTECTION (Null Filter)
                    o = candle.get('open'); h = candle.get('high')
                    l = candle.get('low'); c = candle.get('close')
                    v = candle.get('volume')
                    
                    if o is None or h is None or l is None or c is None: continue
                    
                    data.append({
                        "time": ts,
                        "open": float(o), "high": float(h), 
                        "low": float(l), "close": float(c), 
                        "volume": float(v) if v is not None else 0.0
                    })
                except: continue
            
            # Sort Oldest -> Newest (Required for Lightweight Charts)
            data.sort(key=lambda x: x['time'])
            return data
            
        return []
    except: return []

# ==========================================
# 3. ROBUST PARSERS (THE BRAIN)
# ==========================================

def parse_profile_from_fundamentals(fund_data: dict, symbol: str):
    """Extracts Profile."""
    if not fund_data: return {}
    g = fund_data.get('General') or {}
    # Handles dynamic keys in Officers list
    ceo = "N/A"
    try:
        officers = g.get('Officers')
        if isinstance(officers, dict): ceo = list(officers.values())[0].get('Name')
        elif isinstance(officers, list) and officers: ceo = officers[0].get('Name')
    except: pass

    return {
        "companyName": g.get('Name', symbol), "symbol": symbol,
        "description": g.get('Description', 'No description available.'),
        "industry": g.get('Industry', 'N/A'), "sector": g.get('Sector', 'N/A'),
        "image": g.get('LogoURL', ''), "currency": g.get('CurrencyCode', 'USD'),
        "exchange": g.get('Exchange', 'N/A'), "beta": g.get('Beta'), "ceo": ceo
    }

def parse_metrics_from_fundamentals(fund_data: dict):
    """Extracts Metrics."""
    if not fund_data: return {}
    h = fund_data.get('Highlights') or {}
    v = fund_data.get('Valuation') or {}
    
    def get_val(s, k):
        try: 
            val = s.get(k)
            return float(val) if val is not None and val != 'NA' else None
        except: return None

    pe = get_val(v, 'TrailingPE')
    return {
        "marketCap": get_val(h, 'MarketCapitalization'),
        "peRatioTTM": pe,
        "earningsYieldTTM": (1 / pe) if pe and pe > 0 else None,
        "epsTTM": get_val(h, 'DilutedEPSTTM'),
        "dividendYieldTTM": get_val(h, 'DividendYield'),
        "revenueGrowth": get_val(h, 'RevenueTTM'),
        "grossMargins": get_val(h, 'GrossProfitTTM'),
        "returnOnCapitalEmployedTTM": get_val(h, 'ReturnOnCapitalEmployedTTM'),
        "sharesOutstanding": fund_data.get('SharesStats', {}).get('SharesOutstanding'),
        "priceToBookRatioTTM": get_val(v, 'PriceBookMRQ'),
        "beta": get_val(fund_data.get('Technicals', {}), 'Beta')
    }

def parse_financials(fund_data: dict, type_key: str, period: str = 'yearly'):
    """Parses Financials with Fuzzy Key Matching."""
    if not fund_data: return []
    try:
        cat, sub = type_key.split('::')
        stmts = fund_data.get(cat, {}).get(sub, {}).get(period, {})
        
        formatted = []
        for date_str, data in stmts.items():
            if not data: continue
            
            # Helper to find keys like 'netIncome' OR 'NetIncome'
            def sf(keys): 
                if isinstance(keys, str): keys = [keys]
                for k in keys:
                    try: 
                        val = data.get(k)
                        if val is not None and val != 'None': return float(val)
                    except: pass
                return 0.0

            formatted.append({
                "date": date_str,
                "calendarYear": date_str[:4],
                "netIncome": sf(['netIncome', 'NetIncome']),
                "revenue": sf(['totalRevenue', 'TotalRevenue']),
                "grossProfit": sf(['grossProfit', 'GrossProfit']),
                "totalAssets": sf(['totalAssets', 'TotalAssets']),
                "totalCurrentAssets": sf(['totalCurrentAssets', 'TotalCurrentAssets']),
                "totalCurrentLiabilities": sf(['totalCurrentLiabilities', 'TotalCurrentLiabilities']),
                "longTermDebt": sf(['longTermDebt', 'LongTermDebt']),
                "totalStockholdersEquity": sf(['totalStockholderEquity', 'TotalStockholderEquity']),
                "operatingCashFlow": sf(['totalCashFromOperatingActivities', 'TotalCashFromOperatingActivities']),
                "dividendsPaid": sf(['dividendsPaid', 'DividendsPaid']),
                "weightedAverageShsOut": sf(['commonStockSharesOutstanding', 'CommonStockSharesOutstanding'])
            })
            
        formatted.sort(key=lambda x: x['date'], reverse=True)
        return formatted[:10]
    except: return []

def parse_analyst_data(fund_data: dict):
    if not fund_data: return [], {}
    ar = fund_data.get('AnalystRatings') or {}
    
    try:
        ratings = [{
            "ratingStrongBuy": int(ar.get('StrongBuy') or 0),
            "ratingBuy": int(ar.get('Buy') or 0),
            "ratingHold": int(ar.get('Hold') or 0),
            "ratingSell": int(ar.get('Sell') or 0),
            "ratingStrongSell": int(ar.get('StrongSell') or 0)
        }]
    except: ratings = []

    try:
        tp = float(ar.get('TargetPrice') or 0)
        target = {"targetHigh": tp, "targetLow": tp, "targetConsensus": tp} if tp > 0 else {}
    except: target = {}

    return ratings, target

def parse_shareholding_breakdown(fund_data: dict):
    if not fund_data: return {}
    stats = fund_data.get('SharesStats') or {}
    try:
        insiders = float(stats.get('PercentInsiders') or 0)
        institutions = float(stats.get('PercentInstitutions') or 0)
        fii = institutions * 0.55
        dii = institutions * 0.45
        public = max(0, 100 - (insiders + institutions))
        return {"promoter": insiders, "fii": fii, "dii": dii, "public": public}
    except: return {"promoter": 0, "fii": 0, "dii": 0, "public": 100}

def parse_holders(fund_data: dict):
    if not fund_data: return []
    holders = fund_data.get('Holders') or {}
    source = holders.get('Institutions') or holders.get('Funds') or {}
    output = []
    try:
        iterator = source.values() if isinstance(source, dict) else source
        for h in iterator:
            output.append({
                "holder": h.get('name') or h.get('Name') or "Unknown",
                "shares": float(h.get('shares') or h.get('Shares') or 0),
                "date": h.get('date_reported') or h.get('DateReported')
            })
        return output[:15]
    except: return [{"holder": "Data Aggregated", "shares": 0}]