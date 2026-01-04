import yfinance as yf
import pandas as pd
import pandas_ta as ta
import re

# ==========================================
# 1. CORE DATA FALLBACKS
# ==========================================

def get_company_profile(symbol: str):
    """Fetches profile data from Yahoo Finance."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "companyName": info.get('longName') or info.get('shortName') or symbol,
            "symbol": symbol,
            "description": info.get('longBusinessSummary', 'No description available.'),
            "industry": info.get('industry', 'N/A'),
            "sector": info.get('sector', 'N/A'),
            "ceo": "N/A",
            "website": info.get('website', ''),
            "image": info.get('logo_url', ''), 
            "currency": info.get('currency', 'USD'),
            "exchange": info.get('exchange', 'N/A'),
            "mktCap": info.get('marketCap'),
            "beta": info.get('beta'),
            "fullTimeEmployees": info.get('fullTimeEmployees')
        }
    except Exception: return {}

def get_quote(symbol: str):
    """Fetches real-time quote data."""
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        price = info.get('currentPrice') or info.get('regularMarketPrice') or info.get('previousClose')
        prev_close = info.get('previousClose')
        
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
            "open": info.get('open'),
            "previousClose": prev_close,
            "timestamp": pd.Timestamp.now().timestamp()
        }
    except Exception: return {}

# ==========================================
# 2. CHARTING ENGINE (THE FIX)
# ==========================================

def get_chart_data(symbol: str, range_type: str = "1d", interval: str = "1d"):
    """
    Fetches OHLCV data.
    FIXED: Now treats inputs as INTERVALS (Candle Size) rather than Ranges.
    """
    try:
        ticker = yf.Ticker(symbol)
        
        # Default
        period = "1y"
        yf_interval = "1d"
        
        # Normalize input
        r = range_type.lower()

        # --- SMART INTERVAL MAPPING ---
        # Maps the Frontend Button (e.g., '1W') to the correct Yahoo settings
        
        if r == "5m":
            period = "5d"   # 5 Days of 5-min candles
            yf_interval = "5m"
        elif r == "15m":
            period = "5d"   # 5 Days of 15-min candles
            yf_interval = "15m"
        elif r == "30m":
            period = "5d"   # 5 Days of 30-min candles
            yf_interval = "30m"
        elif r == "1h":
            period = "1mo"  # 1 Month of 1-hour candles
            yf_interval = "60m"
        elif r == "4h":
            # Yahoo Free doesn't support 4h. We fall back to 1h data over 3 months.
            # Or map to Daily if user prefers trend. 
            # Best fallback for charts:
            period = "6mo"
            yf_interval = "1d" 
        elif r == "1d":
            period = "2y"   # 2 Years of Daily candles
            yf_interval = "1d"
        elif r == "1w":
            period = "5y"   # 5 Years of Weekly candles (THE FIX)
            yf_interval = "1wk"
        elif r == "1m":
            period = "max"  # Max history of Monthly candles (THE FIX)
            yf_interval = "1mo"

        # Fetch Data
        df = ticker.history(period=period, interval=yf_interval)
        
        if df.empty: 
            return []

        # Format
        df.reset_index(inplace=True)
        df.columns = [col.lower() for col in df.columns]
        
        chart_data = []
        for _, row in df.iterrows():
            date_val = row['date']
            # Lightweight charts needs seconds
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
        print(f"Chart Data Error: {e}")
        return []

def get_historical_data(symbol: str, period: str = "1y", interval: str = "1d"):
    """Fetches raw dataframe for technical calculations."""
    try:
        # Map frontend interval request to yahoo period
        adjusted_period = period 
        
        if interval == "1m": adjusted_period = "5d"
        elif interval in ["2m", "5m", "15m", "30m", "90m"]: adjusted_period = "5d"
        elif interval in ["60m", "1h"]: adjusted_period = "1mo"
        elif interval == "1wk": adjusted_period = "2y"
        elif interval == "1mo": adjusted_period = "5y"
        
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=adjusted_period, interval=interval)
        if hist.empty: return None
        hist.columns = [col.lower() for col in hist.columns]
        return hist
    except: return None

# ==========================================
# 3. TECHNICALS & FINANCIALS
# ==========================================

def calculate_technical_indicators(df: pd.DataFrame):
    if df is None or df.empty: return {}
    try:
        df.ta.rsi(length=14, append=True)
        df.ta.macd(fast=12, slow=26, signal=9, append=True)
        df.ta.stoch(k=14, d=3, smooth_k=3, append=True)
        df.ta.adx(length=14, append=True)
        df.ta.atr(length=14, append=True)
        df.ta.willr(length=14, append=True)
        df.ta.bbands(length=20, std=2, append=True)
        
        latest = df.iloc[-1]
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
            "price_action": {
                "current_close": latest.get('close'),
                "trend": "UP" if latest.get('close') > prev.get('close') else "DOWN"
            }
        }
    except: return {}

def _parse_yfinance_financials(df):
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
                for key in row.keys():
                    key_str = str(key).lower()
                    if any(kw in key_str for kw in keywords):
                        val = row[key]
                        if pd.notna(val): return float(val)
                return 0.0

            item = {
                "date": date_str,
                "calendarYear": date_str[:4],
                "netIncome": find_val(['net income', 'netincome']),
                "revenue": find_val(['total revenue', 'operating revenue', 'totalrevenue']),
                "grossProfit": find_val(['gross profit', 'grossprofit']),
                "eps": find_val(['basic eps', 'diluted eps']),
                "totalAssets": find_val(['total assets', 'totalassets']),
                "longTermDebt": find_val(['long term debt', 'longtermdebt']),
                "totalCurrentAssets": find_val(['total current assets', 'current assets']),
                "totalCurrentLiabilities": find_val(['total current liabilities', 'current liabilities']),
                "operatingCashFlow": find_val(['operating cash flow', 'operatingcashflow']),
                "dividendsPaid": find_val(['cash dividends paid', 'dividends paid']),
                "totalStockholdersEquity": find_val(['stockholders equity', 'total equity']),
                "weightedAverageShsOut": find_val(['share issued', 'average shares'])
            }
            if 'TTM' not in date_str: formatted_data.append(item)
        return formatted_data
    except: return []

def get_historical_financials(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        return {
            "income": _parse_yfinance_financials(ticker.financials),
            "balance": _parse_yfinance_financials(ticker.balance_sheet),
            "cash_flow": _parse_yfinance_financials(ticker.cashflow),
        }
    except: return {"income": [], "balance": [], "cash_flow": []}

def get_quarterly_financials(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        return {
            "income": _parse_yfinance_financials(ticker.quarterly_financials),
            "balance": _parse_yfinance_financials(ticker.quarterly_balance_sheet),
            "cash_flow": _parse_yfinance_financials(ticker.quarterly_cashflow),
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
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        eps = info.get('trailingEps')
        price = info.get('currentPrice') or info.get('regularMarketPrice')
        return {
            "peRatioTTM": info.get('trailingPE'),
            "earningsYieldTTM": (eps / price) if (eps and price) else None,
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
    try:
        ticker = yf.Ticker(symbol)
        insider = (ticker.info.get('heldPercentInsiders', 0) or 0) * 100
        inst = (ticker.info.get('heldPercentInstitutions', 0) or 0) * 100
        
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
        return { "promoter": insider, "fii": inst * 0.6, "dii": inst * 0.4, "public": public }
    except: return {}

def get_company_info(symbol: str):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info or {}
    except: return {}