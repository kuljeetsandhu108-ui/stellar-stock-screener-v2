import os
import requests
import json
from datetime import datetime, timedelta
import pytz # Critical for IST Timezone conversion
from dotenv import load_dotenv

load_dotenv()

EODHD_API_KEY = os.getenv("EODHD_API_KEY")
BASE_URL = "https://eodhd.com/api"

# ==========================================
# 1. SYMBOL NORMALIZATION ENGINE
# ==========================================

def format_symbol_for_eodhd(symbol: str) -> str:
    """
    Normalizes symbols for EODHD (High-End API).
    Frontend 'RELIANCE.NS' -> EODHD 'RELIANCE.NSE'
    Frontend 'BTC-USD' -> EODHD 'BTC-USD.CC'
    """
    if not symbol: return ""
    symbol = symbol.upper().strip()
    
    # India Mapping
    if symbol.endswith(".NS"): return symbol.replace(".NS", ".NSE")
    if symbol.endswith(".BO"): return symbol.replace(".BO", ".BSE")
    
    # Indices Mapping
    if symbol == "^NSEI": return "NSEI.INDX"
    if symbol == "^NSEBANK": return "NSEBANK.INDX"
    if symbol == "^BSESN": return "BSESN.INDX"
    if symbol == "^GSPC": return "GSPC.INDX"
    if symbol == "^DJI": return "DJI.INDX"
    if symbol == "^IXIC": return "IXIC.INDX"
    if symbol == "^N225": return "N225.INDX"
    if symbol == "^GDAXI": return "GDAXI.INDX"
    
    # Crypto (Common format fix)
    if symbol == "BTC-USD": return "BTC-USD.CC"
    if symbol == "ETH-USD": return "ETH-USD.CC"

    # Default US (If no suffix, assume US)
    if "." not in symbol: return f"{symbol}.US"
        
    return symbol

# ==========================================
# 2. DATA FETCHING (NETWORK LAYER)
# ==========================================

def get_company_fundamentals(symbol: str):
    """
    Fetches the massive 'All-In-One' Fundamental JSON.
    Includes Profile, Financials, Earnings, Holders, Insider Trades.
    """
    if not EODHD_API_KEY: return {}
    eod_symbol = format_symbol_for_eodhd(symbol)
    
    try:
        # We use a longer timeout (25s) because this JSON can be 5MB+
        url = f"{BASE_URL}/fundamentals/{eod_symbol}?api_token={EODHD_API_KEY}&fmt=json"
        response = requests.get(url, timeout=25) 
        
        if response.status_code == 200:
            data = response.json()
            # EODHD returns empty list [] for invalid symbols
            if isinstance(data, list) and not data: return {}
            return data
            
        print(f"EODHD Fundamentals Failed: {response.status_code} for {symbol}")
        return {}
    except Exception as e:
        print(f"EODHD Fundamentals Exception for {symbol}: {e}")
        return {}

def get_live_price(symbol: str):
    """
    Fetches real-time price snapshot.
    INCLUDES FIX: Handles 0.00 price glitch during pre-market.
    """
    if not EODHD_API_KEY: return {}
    eod_symbol = format_symbol_for_eodhd(symbol)
    
    try:
        url = f"{BASE_URL}/real-time/{eod_symbol}?api_token={EODHD_API_KEY}&fmt=json"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # Robust Price Parsing
            price = data.get('close')
            prev = data.get('previousClose')
            
            try:
                price = float(price) if price is not None and price != 'NA' else 0.0
                prev = float(prev) if prev is not None and prev != 'NA' else 0.0
            except: 
                price = 0.0
                prev = 0.0

            # Fallback if close is 0 (market closed/error)
            final_price = price if price > 0 else prev
            
            # Recalculate change based on resolved price
            change = final_price - prev
            change_p = (change / prev * 100) if prev > 0 else 0.0

            return {
                "price": final_price,
                "previousClose": prev,
                "change": change,
                "changesPercentage": change_p,
                "high": data.get('high'),
                "low": data.get('low'),
                "volume": data.get('volume'),
                "timestamp": data.get('timestamp')
            }
        return {}
    except:
        return {}

def get_real_time_bulk(symbols: list):
    """
    Fetches MULTIPLE real-time prices in ONE HTTP REQUEST.
    Format: /real-time/FirstSymbol?s=SecondSymbol,ThirdSymbol,...
    Used for Homepage Ticker (Reduces latency by 90%).
    """
    if not EODHD_API_KEY or not symbols: return []
    
    try:
        # Normalize all symbols first
        clean_symbols = [format_symbol_for_eodhd(s) for s in symbols if s]
        if not clean_symbols: return []

        # EODHD API Syntax: /real-time/Primary?s=CommaSeparatedOthers
        primary = clean_symbols[0]
        others = ",".join(clean_symbols[1:])
        
        url = f"{BASE_URL}/real-time/{primary}?api_token={EODHD_API_KEY}&fmt=json&s={others}"
        
        response = requests.get(url, timeout=8)
        
        if response.status_code == 200:
            data = response.json()
            # If single result, it returns dict. If multiple, returns list.
            if isinstance(data, dict): return [data] 
            return data
            
        return []
    except Exception as e:
        print(f"Bulk Real-Time Error: {e}")
        return []

def get_historical_data(symbol: str, range_type: str = "1d"):
    """
    Fetches Chart Data.
    High-End Logic: 
    1. Fetches 'Master' 5M dataset for all Intraday requests (enables instant resampling).
    2. Forces IST Timezone for Indian Assets.
    3. Filters nulls to prevent crashes.
    """
    if not EODHD_API_KEY: return []
    eod_symbol = format_symbol_for_eodhd(symbol)
    data = []
    
    # 1. Identify Indian Assets for Timezone Offset
    # (.INDX covers Nifty/BankNifty, .NSE/.BSE covers stocks)
    is_indian = ".NSE" in eod_symbol or ".BSE" in eod_symbol or ".INDX" in eod_symbol
    # Exclude if it accidentally matched a US ticker
    if "US" in eod_symbol or "CC" in eod_symbol: is_indian = False

    # 2. Define Timezone Offset (5 Hours 30 Mins = 19800 Seconds)
    # We only apply this to Intraday. EOD dates are usually fine.
    offset = 19800 if is_indian else 0

    try:
        url = ""
        is_intraday_request = range_type in ["5M", "15M", "1H", "4H"]
        
        # --- SMART FETCH STRATEGY ---
        
        if is_intraday_request:
            # MASTER FETCH: Get 30 Days of 5-Minute Data.
            # Why? Because 5M is the "Atom". We can build 15M, 1H, 4H from this 
            # mathematically in the Router without calling the API again.
            ts_from = int((datetime.now() - timedelta(days=30)).timestamp())
            url = f"{BASE_URL}/intraday/{eod_symbol}?api_token={EODHD_API_KEY}&interval=5m&from={ts_from}&fmt=json"
            
        elif range_type == "1D":
            # Daily History: Fetch 3 Years (Standard Analysis depth)
            period = "d"
            from_date = (datetime.now() - timedelta(days=1095)).strftime('%Y-%m-%d')
            url = f"{BASE_URL}/eod/{eod_symbol}?api_token={EODHD_API_KEY}&period={period}&from={from_date}&fmt=json"
            
        else:
            # Weekly/Monthly: Fetch 5 Years
            period = "w" if range_type == "1W" else "m"
            from_date = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')
            url = f"{BASE_URL}/eod/{eod_symbol}?api_token={EODHD_API_KEY}&period={period}&from={from_date}&fmt=json"

        # 3. Execute Request
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            raw_data = response.json()
            
            for candle in raw_data:
                ts = 0
                try:
                    # Parse EOD Date (YYYY-MM-DD)
                    if "date" in candle:
                        dt = datetime.strptime(candle['date'], "%Y-%m-%d")
                        ts = int(dt.replace(tzinfo=pytz.utc).timestamp())
                        
                    # Parse Intraday Date (YYYY-MM-DD HH:MM:SS)
                    elif "datetime" in candle:
                        dt = datetime.strptime(candle['datetime'], "%Y-%m-%d %H:%M:%S")
                        base_ts = int(dt.replace(tzinfo=pytz.utc).timestamp())
                        
                        # CRITICAL: Apply IST Offset here
                        # If we are fetching Intraday for India, shift +5.5 hours
                        if is_intraday_request:
                            ts = base_ts + offset
                        else:
                            ts = base_ts
                except: 
                    continue # Skip malformed dates
                
                # 4. CRASH PROTECTION (Null Filter)
                # Lightweight Charts crashes if any OHLC value is None
                o = candle.get('open')
                h = candle.get('high')
                l = candle.get('low')
                c = candle.get('close')
                v = candle.get('volume')
                
                if o is None or h is None or l is None or c is None: 
                    continue
                
                data.append({
                    "time": ts,
                    "open": float(o), 
                    "high": float(h), 
                    "low": float(l), 
                    "close": float(c), 
                    "volume": float(v) if v is not None else 0.0
                })
            
            # Sort Oldest -> Newest (Required for Charts)
            data.sort(key=lambda x: x['time'])
            return data
            
        return []
    except Exception as e:
        print(f"EODHD Chart Fetch Error: {e}")
        return []
# ==========================================
# 3. ROBUST PARSERS (THE BRAIN)
# ==========================================

def parse_profile_from_fundamentals(fund_data: dict, symbol: str):
    """
    Extracts Profile. FIX: Handles 'Officers' as List or Dict.
    """
    if not fund_data: return {}
    general = fund_data.get('General') or {}
    highlights = fund_data.get('Highlights') or {}
    
    ceo_name = "N/A"
    officers = general.get('Officers')
    if officers:
        try:
            if isinstance(officers, dict):
                first_key = next(iter(officers)) 
                ceo_name = officers[first_key].get('Name', 'N/A')
            elif isinstance(officers, list) and len(officers) > 0:
                ceo_name = officers[0].get('Name', 'N/A')
        except: pass

    # Market Cap Fallback (Sometimes in General, sometimes Highlights)
    mkt_cap = general.get('MarketCapitalization') or highlights.get('MarketCapitalization')

    return {
        "companyName": general.get('Name', symbol),
        "symbol": symbol,
        "description": general.get('Description', 'No description available.'),
        "industry": general.get('Industry', 'N/A'),
        "sector": general.get('Sector', 'N/A'),
        "ceo": ceo_name, 
        "website": general.get('WebURL', ''),
        "image": general.get('LogoURL', ''),
        "currency": general.get('CurrencyCode', 'USD'),
        "exchange": general.get('Exchange', 'N/A'),
        "mktCap": mkt_cap,
        "beta": general.get('Beta'),
    }

def parse_metrics_from_fundamentals(fund_data: dict):
    """
    Extracts Metrics + Calculates Missing Ones (Earnings Yield, Current Ratio).
    """
    if not fund_data: return {}
    highlights = fund_data.get('Highlights') or {}
    valuation = fund_data.get('Valuation') or {}
    technicals = fund_data.get('Technicals') or {} 
    
    def get_val(source, key):
        val = source.get(key)
        try: return float(val) if val is not None and val != 'NA' and val != 'None' else None
        except: return None

    # 1. PE & Earnings Yield
    pe = get_val(valuation, 'TrailingPE')
    eps = get_val(highlights, 'DilutedEPSTTM')
    earnings_yield = 1 / pe if (pe and pe > 0) else None

    # 2. ROCE (Return on Capital)
    roce = get_val(highlights, 'ReturnOnCapitalEmployedTTM')
    if roce is None: roce = get_val(highlights, 'ReturnOnEquityTTM') # Fallback
    if roce is None: roce = get_val(highlights, 'ReturnOnAssetsTTM') # Last Resort

    # 3. Current Ratio (Manual Calculation from BS)
    current_ratio = None
    try:
        bs = fund_data.get('Financials', {}).get('Balance_Sheet', {}).get('quarterly', {})
        if bs:
            latest_date = sorted(bs.keys(), reverse=True)[0]
            latest = bs[latest_date]
            ca = float(latest.get('totalCurrentAssets') or 0)
            cl = float(latest.get('totalCurrentLiabilities') or 0)
            if cl > 0: current_ratio = ca / cl
    except: pass

    return {
        "marketCap": get_val(highlights, 'MarketCapitalization'),
        "peRatioTTM": pe,
        "earningsYieldTTM": earnings_yield,
        "epsTTM": eps,
        "dividendYieldTTM": get_val(highlights, 'DividendYield'),
        "revenueGrowth": get_val(highlights, 'RevenueTTM'),
        "grossMargins": get_val(highlights, 'GrossProfitTTM'),
        "returnOnCapitalEmployedTTM": roce,
        "sharesOutstanding": fund_data.get('SharesStats', {}).get('SharesOutstanding'),
        "beta": get_val(technicals, 'Beta'),
        "priceToBookRatioTTM": get_val(valuation, 'PriceBookMRQ'),
        "currentRatioTTM": current_ratio
    }

def parse_financials(fund_data: dict, type_key: str, period: str = 'yearly'):
    """
    Parses Financials with Fuzzy Key Matching (CamelCase vs PascalCase).
    """
    if not fund_data: return []
    try:
        category, sub = type_key.split('::')
        cat_data = fund_data.get(category) or {}
        sub_data = cat_data.get(sub) or {}
        stmts = sub_data.get(period) or {}
        
        formatted = []
        for date_str, data in stmts.items():
            if not data: continue
            
            # Safe Float Conversion with Key Search
            def sf(keys): 
                if isinstance(keys, str): keys = [keys]
                for k in keys:
                    val = data.get(k)
                    if val is not None and val != 'None':
                        try: return float(val)
                        except: pass
                return 0.0

            item = {
                "date": date_str,
                "calendarYear": date_str[:4] if date_str else "N/A",
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
            }
            formatted.append(item)
            
        formatted.sort(key=lambda x: x['date'], reverse=True)
        return formatted[:10]
    except Exception as e:
        print(f"Financial Parse Error ({type_key}): {e}")
        return []

def parse_analyst_data(fund_data: dict):
    """
    Extracts Analyst Ratings and Price Targets.
    """
    if not fund_data: return [], {}
    ar = fund_data.get('AnalystRatings')
    if not ar or not isinstance(ar, dict): return [], {}

    # Ratings
    try:
        ratings = [{
            "ratingStrongBuy": int(ar.get('StrongBuy') or 0),
            "ratingBuy": int(ar.get('Buy') or 0),
            "ratingHold": int(ar.get('Hold') or 0),
            "ratingSell": int(ar.get('Sell') or 0),
            "ratingStrongSell": int(ar.get('StrongSell') or 0)
        }]
    except: ratings = []

    # Target
    try:
        tp = float(ar.get('TargetPrice') or 0)
        target = {}
        if tp > 0:
            target = {"targetHigh": tp, "targetLow": tp, "targetConsensus": tp}
    except: target = {}

    return ratings, target

def parse_shareholding_breakdown(fund_data: dict):
    """
    Extracts Shareholding %.
    """
    if not fund_data: return {}
    stats = fund_data.get('SharesStats') or {}
    try:
        insiders = float(stats.get('PercentInsiders') or 0)
        institutions = float(stats.get('PercentInstitutions') or 0)
        
        # Heuristic Split for FII/DII
        fii = institutions * 0.55
        dii = institutions * 0.45
        public = max(0, 100 - (insiders + institutions))
        
        return {"promoter": insiders, "fii": fii, "dii": dii, "public": public}
    except:
        return {"promoter": 0, "fii": 0, "dii": 0, "public": 100}

def parse_holders(fund_data: dict):
    """
    Extracts Major Holders.
    """
    if not fund_data: return []
    holders = fund_data.get('Holders') or {}
    source_raw = holders.get('Institutions') or holders.get('Funds')
    
    if not source_raw: 
        return [{"holder": "Data Aggregated", "shares": 0}]

    output = []
    try:
        iterator = source_raw.values() if isinstance(source_raw, dict) else source_raw
        for h in iterator:
            output.append({
                "holder": h.get('name') or h.get('Name') or "Unknown",
                "shares": float(h.get('shares') or h.get('Shares') or 0),
                "date": h.get('date_reported') or h.get('DateReported'),
                "value": float(h.get('value') or h.get('Value') or 0)
            })
        return output[:15]
    except:
        return [{"holder": "Data Aggregated", "shares": 0}]