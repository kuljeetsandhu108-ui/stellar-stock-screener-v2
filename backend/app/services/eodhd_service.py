import os
import requests
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EODHD_API_KEY = os.getenv("EODHD_API_KEY")
BASE_URL = "https://eodhd.com/api"

# ==========================================
# 1. SYMBOL NORMALIZATION ENGINE
# ==========================================

def format_symbol_for_eodhd(symbol: str) -> str:
    """
    Intelligently converts Frontend symbols to EODHD format.
    Handles NSE, BSE, Indices, Crypto, and US Stocks.
    """
    if not symbol: return ""
    symbol = symbol.upper().strip()
    
    # India Mapping
    if symbol.endswith(".NS"): return symbol.replace(".NS", ".NSE")
    if symbol.endswith(".BO"): return symbol.replace(".BO", ".BSE")
    
    # Indices Mapping (Major Global)
    if symbol == "^NSEI": return "NSEI.INDX"
    if symbol == "^NSEBANK": return "NSEBANK.INDX"
    if symbol == "^BSESN": return "BSESN.INDX"
    if symbol == "^GSPC": return "GSPC.INDX" # S&P 500
    if symbol == "^DJI": return "DJI.INDX"   # Dow Jones
    if symbol == "^IXIC": return "IXIC.INDX" # Nasdaq
    if symbol == "^N225": return "N225.INDX" # Nikkei
    if symbol == "^FTSE": return "FTSE.INDX" # FTSE 100
    
    # Crypto (Common format fix)
    if symbol == "BTC-USD": return "BTC-USD.CC"
    if symbol == "ETH-USD": return "ETH-USD.CC"

    # Default US (If no suffix, assume US)
    if "." not in symbol: return f"{symbol}.US"
        
    return symbol

# ==========================================
# 2. HIGH-PERFORMANCE DATA FETCHING
# ==========================================

def get_company_fundamentals(symbol: str):
    """
    Fetches the 'All-In-One' Fundamental JSON.
    This single call powers 80% of the dashboard (Profile, Financials, Metrics, Ratings).
    """
    if not EODHD_API_KEY: return {}
    eod_symbol = format_symbol_for_eodhd(symbol)
    
    try:
        # Extended timeout (25s) because this JSON can be 5MB+ for large corps
        url = f"{BASE_URL}/fundamentals/{eod_symbol}?api_token={EODHD_API_KEY}&fmt=json"
        response = requests.get(url, timeout=25) 
        
        if response.status_code == 200:
            data = response.json()
            # EODHD sometimes returns an empty list [] for invalid symbols
            if isinstance(data, list) and not data: return {}
            return data
            
        print(f"EODHD Fundamentals Failed: {response.status_code} for {symbol}")
        return {}
    except Exception as e:
        print(f"EODHD Fundamentals Connection Exception: {e}")
        return {}

def get_live_price(symbol: str):
    """
    Fetches real-time price snapshot.
    Includes 'Zero-Price Fix' logic for pre-market/glitch scenarios.
    """
    if not EODHD_API_KEY: return {}
    eod_symbol = format_symbol_for_eodhd(symbol)
    
    try:
        url = f"{BASE_URL}/real-time/{eod_symbol}?api_token={EODHD_API_KEY}&fmt=json"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # --- THE 0.00 FIX ---
            # EODHD sometimes returns 'close': 'NA' or 0 during maintenance
            price = data.get('close')
            prev = data.get('previousClose')
            
            try:
                price = float(price) if price is not None and price != 'NA' else 0.0
                prev = float(prev) if prev is not None and prev != 'NA' else 0.0
            except: 
                price = 0.0
                prev = 0.0

            # If current price is 0 (market closed/error), use previous close
            final_price = price if price > 0 else prev
            
            # Recalculate change if needed
            change = final_price - prev
            change_p = (change / prev * 100) if prev > 0 else 0.0

            return {
                "price": final_price,
                "previousClose": prev,
                "change": change,
                "changesPercentage": change_p,
                "high": data.get('high'),
                "low": data.get('low'),
                "open": data.get('open'),
                "volume": data.get('volume'),
                "timestamp": data.get('timestamp')
            }
        return {}
    except:
        return {}

def get_historical_data(symbol: str, range_type: str = "1d"):
    """
    Fetches Chart Data (OHLCV).
    Features:
    1. Auto-switch between Intraday and EOD endpoints.
    2. Filters out 'None' values to prevent Chart Library crashes.
    """
    if not EODHD_API_KEY: return []
    eod_symbol = format_symbol_for_eodhd(symbol)
    data = []
    
    try:
        url = ""
        # Intraday Logic (5m for 1D, 1h for longer)
        if range_type in ["1D", "5M", "15M"]:
            url = f"{BASE_URL}/intraday/{eod_symbol}?api_token={EODHD_API_KEY}&interval=5m&fmt=json"
        elif range_type in ["1H", "4H"]:
            url = f"{BASE_URL}/intraday/{eod_symbol}?api_token={EODHD_API_KEY}&interval=1h&fmt=json"
        else:
            # EOD Logic (Daily/Weekly/Monthly)
            period = "d"
            if range_type == "1W": period = "w"
            if range_type == "1M": period = "m"
            
            # Limit to 3 years (1095 days) to keep payload light & fast
            from_date = (datetime.now() - timedelta(days=1095)).strftime('%Y-%m-%d')
            url = f"{BASE_URL}/eod/{eod_symbol}?api_token={EODHD_API_KEY}&period={period}&from={from_date}&fmt=json"

        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            raw_data = response.json()
            
            for candle in raw_data:
                ts = 0
                try:
                    # Smart Date Parser (Handles both Intraday and EOD formats)
                    if "date" in candle:
                        ts = int(datetime.strptime(candle['date'], "%Y-%m-%d").timestamp())
                    elif "datetime" in candle:
                        ts = int(datetime.strptime(candle['datetime'], "%Y-%m-%d %H:%M:%S").timestamp())
                except: continue 
                
                # --- CRASH PROTECTION: STRICT NULL CHECK ---
                o, h, l, c, v = candle.get('open'), candle.get('high'), candle.get('low'), candle.get('close'), candle.get('volume')
                
                # Skip if any essential price data is missing
                if o is None or h is None or l is None or c is None: continue
                
                data.append({
                    "time": ts,
                    "open": float(o), 
                    "high": float(h), 
                    "low": float(l), 
                    "close": float(c), 
                    "volume": float(v) if v is not None else 0.0
                })
            
            # Ensure sorted oldest -> newest for charts
            data.sort(key=lambda x: x['time'])
            return data
            
        return []
    except Exception as e:
        print(f"EODHD Chart Error for {symbol}: {e}")
        return []

# ==========================================
# 3. ROBUST DATA PARSERS (THE BRAIN)
# ==========================================

def parse_profile_from_fundamentals(fund_data: dict, symbol: str):
    """
    Extracts Profile data. 
    FIX: Handles 'Officers' being a Dict OR List (Prevents KeyError: 0).
    """
    if not fund_data: return {}
    general = fund_data.get('General') or {}
    highlights = fund_data.get('Highlights') or {}
    
    # --- OFFICERS CRASH FIX ---
    ceo_name = "N/A"
    officers = general.get('Officers')
    
    if officers:
        try:
            # Case A: Dictionary (e.g. {"0": {...}})
            if isinstance(officers, dict):
                first_key = next(iter(officers)) 
                ceo_name = officers[first_key].get('Name', 'N/A')
            # Case B: List (e.g. [{...}])
            elif isinstance(officers, list) and len(officers) > 0:
                ceo_name = officers[0].get('Name', 'N/A')
        except:
            ceo_name = "N/A"
    # --------------------------

    # Market Cap Fallback (Try General, then Highlights)
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
        "fullTimeEmployees": general.get('FullTimeEmployees', 'N/A')
    }

def parse_metrics_from_fundamentals(fund_data: dict):
    """
    Extracts Key Metrics (PE, EPS, etc) and manually calculates missing ones
    like Earnings Yield and Current Ratio to ensure AI tabs work.
    """
    if not fund_data: return {}
    
    # Extract sub-sections safely
    highlights = fund_data.get('Highlights') or {}
    valuation = fund_data.get('Valuation') or {}
    technicals = fund_data.get('Technicals') or {} 
    
    # Helper to clean invalid numbers (None, 'NA', 'None')
    def get_val(source, key):
        val = source.get(key)
        try: 
            return float(val) if val is not None and val != 'NA' and val != 'None' else None
        except: 
            return None

    # --- 1. Robust PE & Earnings Yield ---
    pe = get_val(valuation, 'TrailingPE')
    eps = get_val(highlights, 'DilutedEPSTTM')
    
    # Calculate Earnings Yield (The inverse of P/E)
    # This is critical for the "Value Investing" tab
    earnings_yield = None
    if pe and pe > 0:
        earnings_yield = 1 / pe
    
    # --- 2. Robust ROCE (Return on Capital) ---
    # Priority: Explicit ROCE -> ROE -> ROA
    roce = get_val(highlights, 'ReturnOnCapitalEmployedTTM')
    if roce is None:
        roce = get_val(highlights, 'ReturnOnEquityTTM') # ROE is a common proxy
    if roce is None:
        roce = get_val(highlights, 'ReturnOnAssetsTTM')

    # --- 3. Current Ratio (Manual Calculation) ---
    # Critical for Benjamin Graham Scan
    current_ratio = None
    try:
        # Navigate to Quarterly Balance Sheet
        bs = fund_data.get('Financials', {}).get('Balance_Sheet', {}).get('quarterly', {})
        if bs:
            # Get the most recent date key
            latest_date = sorted(bs.keys(), reverse=True)[0]
            latest = bs[latest_date]
            
            ca = float(latest.get('totalCurrentAssets') or 0)
            cl = float(latest.get('totalCurrentLiabilities') or 0)
            
            if cl > 0:
                current_ratio = ca / cl
    except: 
        pass

    return {
        "marketCap": get_val(highlights, 'MarketCapitalization'),
        "peRatioTTM": pe,
        "earningsYieldTTM": earnings_yield, # Now calculated!
        "epsTTM": eps,
        "dividendYieldTTM": get_val(highlights, 'DividendYield'),
        "revenueGrowth": get_val(highlights, 'RevenueTTM'),
        "grossMargins": get_val(highlights, 'GrossProfitTTM'),
        "returnOnCapitalEmployedTTM": roce, # Now robust!
        "sharesOutstanding": fund_data.get('SharesStats', {}).get('SharesOutstanding'),
        "beta": get_val(technicals, 'Beta'),
        "priceToBookRatioTTM": get_val(valuation, 'PriceBookMRQ'),
        "currentRatioTTM": current_ratio # Now calculated!
    }
    
def parse_financials(fund_data: dict, type_key: str, period: str = 'yearly'):
    """
    Parses Financials with Fuzzy Key Matching.
    Handles 'totalRevenue' vs 'TotalRevenue' mismatches.
    """
    if not fund_data: return []
    try:
        # Navigate keys safely: e.g., Financials -> Income_Statement -> yearly
        category, sub = type_key.split('::')
        
        cat_data = fund_data.get(category) or {}
        sub_data = cat_data.get(sub) or {}
        stmts = sub_data.get(period) or {}
        
        formatted = []
        for date_str, data in stmts.items():
            if not data: continue
            
            # Robust Float Helper: Checks multiple key variations
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
            
            # EPS Fallback if missing
            if item['netIncome'] and item['weightedAverageShsOut']:
                item['eps'] = item['netIncome'] / item['weightedAverageShsOut']
            else:
                item['eps'] = 0.0
                
            formatted.append(item)
            
        # Newest First
        formatted.sort(key=lambda x: x['date'], reverse=True)
        return formatted[:10] 
    except Exception as e:
        print(f"Financial Parse Error ({type_key}): {e}")
        return []

def parse_analyst_data(fund_data: dict):
    """
    Extracts Analyst Ratings and Price Targets.
    Used to populate the 'Forecasts' tab.
    """
    if not fund_data: return [], {}
    
    # EODHD usually stores this under 'AnalystRatings'
    ar = fund_data.get('AnalystRatings')
    
    if not ar or not isinstance(ar, dict): 
        return [], {}

    # 1. Format Ratings
    try:
        ratings = [{
            "ratingStrongBuy": int(ar.get('StrongBuy') or 0),
            "ratingBuy": int(ar.get('Buy') or 0),
            "ratingHold": int(ar.get('Hold') or 0),
            "ratingSell": int(ar.get('Sell') or 0),
            "ratingStrongSell": int(ar.get('StrongSell') or 0)
        }]
    except:
        ratings = []

    # 2. Format Price Target
    try:
        tp = float(ar.get('TargetPrice') or 0)
        target = {}
        if tp > 0:
            target = {
                "targetHigh": tp,
                "targetLow": tp,
                "targetConsensus": tp
            }
    except:
        target = {}

    return ratings, target

def parse_shareholding_breakdown(fund_data: dict):
    """
    Extracts Insider vs Institution vs Public % for Donut Chart.
    """
    if not fund_data: return {}
    stats = fund_data.get('SharesStats') or {}
    
    try:
        insiders = float(stats.get('PercentInsiders') or 0)
        institutions = float(stats.get('PercentInstitutions') or 0)
        
        # Heuristic: Split Institutions into FII/DII for display
        fii = institutions * 0.55
        dii = institutions * 0.45
        
        public = max(0, 100 - (insiders + institutions))
        
        return {
            "promoter": insiders,
            "fii": fii,
            "dii": dii,
            "public": public
        }
    except:
        return {"promoter": 0, "fii": 0, "dii": 0, "public": 100}

def parse_holders(fund_data: dict):
    """
    Extracts Top Holders List.
    """
    if not fund_data: return []
    holders = fund_data.get('Holders') or {}
    
    # Try Institutions or Funds keys
    source_raw = holders.get('Institutions') or holders.get('Funds')
    
    if not source_raw: 
        # Return dummy so tab doesn't hide
        return [{"holder": "Data Aggregated", "shares": 0}]

    output = []
    try:
        # Handle if source is dict or list
        iterator = source_raw.values() if isinstance(source_raw, dict) else source_raw
        
        for h in iterator:
            output.append({
                "holder": h.get('name') or h.get('Name') or "Unknown",
                "shares": float(h.get('shares') or h.get('Shares') or 0),
                "date": h.get('date_reported') or h.get('DateReported'),
                "value": float(h.get('value') or h.get('Value') or 0)
            })
        return output[:15] # Top 15
    except:
        return [{"holder": "Data Aggregated", "shares": 0}]