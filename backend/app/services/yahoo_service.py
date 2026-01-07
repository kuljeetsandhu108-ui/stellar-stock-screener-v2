import yfinance as yf
import pandas as pd
import pandas_ta as ta
import re
from datetime import datetime

# ==========================================
# 1. CORE DATA FALLBACKS (The Safety Net)
# ==========================================

def get_company_profile(symbol: str):
    """
    Fetches profile data from Yahoo Finance formatted EXACTLY like FMP.
    Used automatically if FMP returns empty data.
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        return {
            "companyName": info.get('longName') or info.get('shortName') or symbol,
            "symbol": symbol,
            "description": info.get('longBusinessSummary', 'No description available.'),
            "industry": info.get('industry', 'N/A'),
            "sector": info.get('sector', 'N/A'),
            "ceo": "N/A", # Yahoo often hides CEO deep in governance data
            "website": info.get('website', ''),
            "image": info.get('logo_url', ''), 
            "currency": info.get('currency', 'USD'),
            "exchange": info.get('exchange', 'N/A'),
            "mktCap": info.get('marketCap'),
            "beta": info.get('beta'),
            "fullTimeEmployees": info.get('fullTimeEmployees')
        }
    except Exception as e:
        # print(f"Yahoo Profile Error for {symbol}: {e}")
        return {}

def get_quote(symbol: str):
    """
    Fetches real-time quote data from Yahoo Finance.
    Used for the "Live Stitching" feature to patch charts in real-time.
    """
    try:
        ticker = yf.Ticker(symbol)
        
        # Priority: Fast Info (Realtime) -> Standard Info
        price = None
        prev_close = None
        
        if hasattr(ticker, 'fast_info'):
            price = ticker.fast_info.last_price
            prev_close = ticker.fast_info.previous_close
            
        if not price:
            info = ticker.info
            price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')
            prev_close = info.get('previousClose')
        
        # Fallback info dict for volume/ranges
        info = ticker.info
        
        change = 0.0
        percent = 0.0
        
        if price and prev_close:
            change = price - prev_close
            percent = (change / prev_close) * 100

        return {
            "price": price,
            "change": change,
            "changesPercentage": percent,
            "dayLow": info.get('dayLow'),
            "dayHigh": info.get('dayHigh'),
            "yearHigh": info.get('fiftyTwoWeekHigh'),
            "yearLow": info.get('fiftyTwoWeekLow'),
            "volume": info.get('volume') or info.get('regularMarketVolume'),
            "avgVolume": info.get('averageVolume'),
            "open": info.get('open') or info.get('regularMarketOpen'),
            "previousClose": prev_close,
            "timestamp": pd.Timestamp.now().timestamp()
        }
    except Exception as e:
        return {}

# ==========================================
# 2. CHARTING ENGINE (WEEKLY/MONTHLY SPECIALIST)
# ==========================================

def get_chart_data(symbol: str, range_type: str = "1d", interval: str = "1d"):
    """
    Fetches OHLCV data.
    CRITICAL: Handles '1W' and '1M' aggregation which FMP struggles with.
    """
    try:
        ticker = yf.Ticker(symbol)
        
        # Default settings
        period = "1y"
        yf_interval = "1d"
        
        # Normalize input
        r = range_type.lower()

        # --- SMART INTERVAL MAPPING ---
        if r == "5m":
            period = "5d"; yf_interval = "5m"
        elif r == "15m":
            period = "5d"; yf_interval = "15m"
        elif r == "30m":
            period = "5d"; yf_interval = "30m"
        elif r == "1h":
            period = "1mo"; yf_interval = "60m"
        elif r == "4h":
            # Yahoo free doesn't do 4h. Fallback to 1h for 6 months.
            period = "6mo"; yf_interval = "60m" 
        elif r == "1d":
            period = "2y"; yf_interval = "1d"
        
        # --- WEEKLY / MONTHLY HANDLERS ---
        elif r == "1w":
            period = "5y"; yf_interval = "1wk"
        elif r == "1m":
            period = "max"; yf_interval = "1mo"

        # Fetch Data
        df = ticker.history(period=period, interval=yf_interval)
        
        if df.empty: 
            return []

        # Clean Data
        df.reset_index(inplace=True)
        df.columns = [col.lower() for col in df.columns]
        
        chart_data = []
        for _, row in df.iterrows():
            # Lightweight charts requires Seconds (Unix Timestamp)
            date_val = row['date']
            time_val = int(date_val.timestamp())
            
            chart_data.append({
                "time": time_val,
                "open": row['open'],
                "high": row['high'],
                "low": row['low'],
                "close": row['close'],
                "volume": row['volume']
            })
            
        return chart_data
    except Exception as e:
        print(f"Yahoo Chart Error: {e}")
        return []

def get_historical_data(symbol: str, period: str = "1y", interval: str = "1d"):
    """
    Fetches raw Pandas DataFrame for server-side calculations (Technicals, Pivots).
    """
    try:
        # Robust Interval Mapping for Calculations
        adjusted_period = period 
        
        if interval == "1m": adjusted_period = "5d"
        elif interval in ["2m", "5m", "15m", "30m", "90m"]: adjusted_period = "5d"
        elif interval in ["60m", "1h"]: adjusted_period = "1mo"
        elif interval == "1wk": adjusted_period = "2y"
        elif interval == "1mo": adjusted_period = "5y"
        
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=adjusted_period, interval=interval)
        
        if hist.empty: return None
        
        # Lowercase columns for pandas_ta compatibility
        hist.columns = [col.lower() for col in hist.columns]
        return hist
    except Exception: 
        return None

# ==========================================
# 3. TECHNICAL ANALYSIS ENGINE (PANDAS_TA)
# ==========================================

def calculate_technical_indicators(df: pd.DataFrame):
    """
    Calculates RSI, MACD, Stoch, ADX, ATR, Bollinger Bands.
    """
    if df is None or df.empty: return {}
    try:
        # Execute Pandas TA strategies
        df.ta.rsi(length=14, append=True)
        df.ta.macd(fast=12, slow=26, signal=9, append=True)
        df.ta.stoch(k=14, d=3, smooth_k=3, append=True)
        df.ta.adx(length=14, append=True)
        df.ta.atr(length=14, append=True)
        df.ta.willr(length=14, append=True)
        df.ta.bbands(length=20, std=2, append=True)
        
        # Get the most recent data point
        latest = df.iloc[-1]
        # Get previous point for Trend Direction
        prev = df.iloc[-2] if len(df) > 1 else latest

        return {
            "rsi": latest.get('RSI_14'),
            "macd": latest.get('MACD_12_26_9'),
            "macdsignal": latest.get('MACDs_12_26_9'),
            "stochasticsk": latest.get('STOCHk_14_3_3'),
            "adx": latest.get('ADX_14'),
            "atr": latest.get('ATRr_14'),
            "williamsr": latest.get('WILLR_14'),
            "bollingerBands": {
                "upperBand": latest.get('BBU_20_2.0'),
                "middleBand": latest.get('BBM_20_2.0'),
                "lowerBand": latest.get('BBL_20_2.0'),
            },
            # Context for AI
            "price_action": {
                "current_close": latest.get('close'),
                "prev_close": prev.get('close'),
                "trend": "UP" if latest.get('close') > prev.get('close') else "DOWN"
            }
        }
    except Exception as e: 
        print(f"Technical Calc Error: {e}")
        return {}

# ==========================================
# 4. FINANCIALS & METRICS (FUZZY MATCHING)
# ==========================================

def _parse_yfinance_financials(df):
    """
    Robust Fuzzy Matcher for Financial Statements.
    Fixes the '0/9 Piotroski Score' issue by finding keys even if Yahoo changes them.
    """
    if df is None or df.empty: return []
    try:
        df_t = df.transpose()
        df_t.reset_index(inplace=True)
        df_t.columns.values[0] = "date"
        
        records = df_t.to_dict('records')
        formatted_data = []

        for row in records:
            date_val = row['date']
            date_str = str(date_val).split(' ')[0]

            def find_val(keywords):
                """Searches all row keys for a keyword match"""
                for key in row.keys():
                    key_str = str(key).lower()
                    if any(kw in key_str for kw in keywords):
                        val = row[key]
                        if pd.notna(val): return float(val)
                return 0.0

            item = {
                "date": date_str,
                "calendarYear": date_str[:4],
                # Income
                "netIncome": find_val(['net income', 'netincome', 'net income common']),
                "revenue": find_val(['total revenue', 'operating revenue', 'totalrevenue']),
                "grossProfit": find_val(['gross profit', 'grossprofit']),
                "eps": find_val(['basic eps', 'diluted eps']),
                # Balance Sheet
                "totalAssets": find_val(['total assets', 'totalassets']),
                "longTermDebt": find_val(['long term debt', 'longtermdebt']),
                "totalCurrentAssets": find_val(['total current assets', 'current assets']),
                "totalCurrentLiabilities": find_val(['total current liabilities', 'current liabilities']),
                "totalStockholdersEquity": find_val(['stockholders equity', 'total equity']),
                # Cash Flow
                "operatingCashFlow": find_val(['operating cash flow', 'operatingcashflow']),
                "dividendsPaid": find_val(['cash dividends paid', 'dividends paid']),
                "weightedAverageShsOut": find_val(['share issued', 'average shares'])
            }
            
            # Filter out TTM rows if they are incomplete
            if 'TTM' not in date_str:
                formatted_data.append(item)

        return formatted_data
    except Exception: return []

def get_historical_financials(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        # Try both new (.income_stmt) and old (.financials) properties
        inc = ticker.income_stmt if not ticker.income_stmt.empty else ticker.financials
        bal = ticker.balance_sheet if not ticker.balance_sheet.empty else ticker.balance_sheet
        cf = ticker.cashflow if not ticker.cashflow.empty else ticker.cashflow
        
        return {
            "income": _parse_yfinance_financials(inc),
            "balance": _parse_yfinance_financials(bal),
            "cash_flow": _parse_yfinance_financials(cf),
        }
    except: return {"income": [], "balance": [], "cash_flow": []}

def get_quarterly_financials(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        inc = ticker.quarterly_income_stmt if not ticker.quarterly_income_stmt.empty else ticker.quarterly_financials
        bal = ticker.quarterly_balance_sheet if not ticker.quarterly_balance_sheet.empty else ticker.quarterly_balance_sheet
        cf = ticker.quarterly_cashflow if not ticker.quarterly_cashflow.empty else ticker.quarterly_cashflow

        return {
            "income": _parse_yfinance_financials(inc),
            "balance": _parse_yfinance_financials(bal),
            "cash_flow": _parse_yfinance_financials(cf),
        }
    except: return {"income": [], "balance": [], "cash_flow": []}

def get_analyst_recommendations(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        recs = ticker.recommendations
        if recs is None or recs.empty: return []
        latest = recs.iloc[-1]
        
        def get_col(name):
            for col in latest.index:
                if name.lower() in str(col).lower(): return int(latest[col])
            return 0
            
        return [{
            "ratingStrongBuy": get_col('strongBuy'),
            "ratingBuy": get_col('buy'),
            "ratingHold": get_col('hold'),
            "ratingSell": get_col('sell'),
            "ratingStrongSell": get_col('strongSell'),
        }]
    except: return []

def get_price_target_data(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "targetHigh": info.get('targetHighPrice'),
            "targetLow": info.get('targetLowPrice'),
            "targetConsensus": info.get('targetMeanPrice'),
        }
    except: return {}

def get_key_fundamentals(symbol: str):
    """
    Robust Metrics Fetcher.
    Calculates P/E manually if missing (Critical for International Stocks).
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        price = info.get('currentPrice') or info.get('regularMarketPrice')
        eps = info.get('trailingEps')
        
        # Manual P/E Calculation
        pe = info.get('trailingPE')
        if pe is None and price and eps and eps != 0:
            pe = price / eps
            
        ey = (eps / price) if (eps and price) else None
        
        return {
            "peRatioTTM": pe,
            "earningsYieldTTM": ey,
            "returnOnCapitalEmployedTTM": info.get('returnOnEquity'),
            "marketCap": info.get('marketCap'),
            "revenueGrowth": info.get('revenueGrowth'),
            "grossMargins": info.get('grossMargins'),
            "dividendYieldTTM": info.get('dividendYield'),
            "epsTTM": eps,
            "netIncomePerShareTTM": eps,
            "revenuePerShareTTM": info.get('revenuePerShare'),
            "sharesOutstanding": info.get('sharesOutstanding'),
            "beta": info.get('beta'),
            "fullTimeEmployees": info.get('fullTimeEmployees')
        }
    except: return {}

def get_shareholding_summary(symbol: str):
    """
    Scrapes 'major_holders' table if standard 'info' is empty.
    Critical for NSE stocks.
    """
    try:
        ticker = yf.Ticker(symbol)
        
        insider = 0.0
        inst = 0.0
        
        # 1. Try Info Dictionary
        if ticker.info.get('heldPercentInsiders') is not None:
            insider = ticker.info.get('heldPercentInsiders') * 100
        if ticker.info.get('heldPercentInstitutions') is not None:
            inst = ticker.info.get('heldPercentInstitutions') * 100
            
        # 2. If Info failed, try Major Holders DataFrame (Critical for Indian Stocks)
        if insider == 0 and inst == 0:
            holders = ticker.major_holders
            if holders is not None and not holders.empty:
                for index, row in holders.iterrows():
                    try:
                        val_str = str(row.iloc[0])
                        label = str(row.iloc[1]).lower()
                        
                        if '%' in val_str:
                            val = float(val_str.replace('%', ''))
                            if 'insider' in label: insider = val
                            elif 'institution' in label: inst = val
                    except: continue

        public = max(0, 100 - insider - inst) if (insider + inst) > 0 else 0
        
        return {
            "promoter": insider,
            "fii": inst * 0.6, 
            "dii": inst * 0.4, 
            "public": public
        }
    except: return {}

def get_company_info(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info or {}
    except: return {}