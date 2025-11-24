import yfinance as yf
import pandas as pd
import pandas_ta as ta

def get_historical_data(symbol: str, period: str = "1y", interval: str = "1d"):
    """
    Fetches historical stock price data from Yahoo Finance for a given ticker.
    Returns a pandas DataFrame.
    """
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)
        
        if hist.empty:
            print(f"Warning: No historical data found for symbol '{symbol}'.")
            return None
        
        # Ensure all column names are lowercase for compatibility with pandas_ta
        hist.columns = [col.lower() for col in hist.columns]
        return hist

    except Exception as e:
        print(f"An error occurred while fetching historical data for {symbol} from yfinance: {e}")
        return None

def calculate_technical_indicators(df: pd.DataFrame):
    """
    Calculates a set of technical indicators from a DataFrame of historical price data.
    """
    if df is None or df.empty:
        return {}

    try:
        # Use pandas_ta to calculate indicators
        df.ta.rsi(length=14, append=True)
        df.ta.macd(fast=12, slow=26, signal=9, append=True)
        df.ta.stoch(k=14, d=3, smooth_k=3, append=True)
        df.ta.adx(length=14, append=True)
        df.ta.atr(length=14, append=True)
        df.ta.willr(length=14, append=True)
        df.ta.bbands(length=20, std=2, append=True)
        
        latest_indicators = df.iloc[-1]

        return {
            "rsi": latest_indicators.get('RSI_14'),
            "macd": latest_indicators.get('MACD_12_26_9'),
            "macdsignal": latest_indicators.get('MACDs_12_26_9'),
            "stochasticsk": latest_indicators.get('STOCHk_14_3_3'),
            "adx": latest_indicators.get('ADX_14'),
            "atr": latest_indicators.get('ATRr_14'),
            "williamsr": latest_indicators.get('WILLR_14'),
            "bollingerBands": {
                "upperBand": latest_indicators.get('BBU_20_2.0'),
                "middleBand": latest_indicators.get('BBM_20_2.0'),
                "lowerBand": latest_indicators.get('BBL_20_2.0'),
            }
        }
    except Exception as e:
        print(f"Error calculating technical indicators: {e}")
        return {}

def get_analyst_recommendations(symbol: str):
    """
    Fetches analyst recommendation data (strong buy, buy, hold, etc.) from Yahoo Finance.
    """
    try:
        ticker = yf.Ticker(symbol)
        recommendations = ticker.recommendations
        if recommendations is None or recommendations.empty:
            return []
        
        latest_summary = recommendations.iloc[-1]
        
        return [{
            "ratingStrongBuy": int(latest_summary.get('strong buy', 0)),
            "ratingBuy": int(latest_summary.get('buy', 0)),
            "ratingHold": int(latest_summary.get('hold', 0)),
            "ratingSell": int(latest_summary.get('sell', 0)),
            "ratingStrongSell": int(latest_summary.get('strong sell', 0)),
        }]
    except Exception as e:
        print(f"Error fetching yfinance recommendations for {symbol}: {e}")
        return []

def get_price_target_data(symbol: str):
    """
    Fetches price target data (high, low, average) from Yahoo Finance's analysis info.
    """
    try:
        ticker = yf.Ticker(symbol)
        analysis = ticker.info
        
        if not analysis or 'targetMeanPrice' not in analysis or analysis.get('targetMeanPrice') is None:
            return {}
            
        return {
            "targetHigh": analysis.get('targetHighPrice'),
            "targetLow": analysis.get('targetLowPrice'),
            "targetConsensus": analysis.get('targetMeanPrice'),
        }
    except Exception as e:
        print(f"Error fetching yfinance price target for {symbol}: {e}")
        return {}

def get_key_fundamentals(symbol: str):
    """
    This is our ultimate fallback. It gets all equivalent metrics for our features
    directly from Yahoo Finance's reliable .info dictionary.
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        # Safe helper to extract numbers
        def get_float(key):
            val = info.get(key)
            return val if val is not None and isinstance(val, (int, float)) else None

        trailing_eps = get_float('trailingEps')
        market_price = get_float('regularMarketPrice') or get_float('previousClose')
        
        earnings_yield = None
        if trailing_eps is not None and market_price is not None and market_price != 0:
            earnings_yield = trailing_eps / market_price
        
        # Return on Equity is a good proxy for Return on Capital
        roe = get_float('returnOnEquity')
        
        # This dictionary maps Yahoo keys to the FMP keys expected by our frontend
        return {
            "symbol": symbol,
            "peRatioTTM": get_float('trailingPE'),
            "earningsYieldTTM": earnings_yield,
            "returnOnCapitalEmployedTTM": roe,
            "marketCap": get_float('marketCap'),
            "revenueGrowth": get_float('revenueGrowth'),
            "grossMargins": get_float('grossMargins'),
            "dividendYieldTTM": get_float('dividendYield'),
            "epsTTM": trailing_eps,
            "netIncomePerShareTTM": trailing_eps, # Approximation using EPS
            "revenuePerShareTTM": get_float('revenuePerShare'),
            "sharesOutstanding": get_float('sharesOutstanding'),
            "beta": get_float('beta'),
            "fullTimeEmployees": info.get('fullTimeEmployees')
        }
    except Exception as e:
        print(f"Error fetching yfinance key fundamentals for {symbol}: {e}")
        return {}

def _parse_yfinance_financials(df):
    """
    Internal helper to transpose Yahoo Finance DataFrame and map columns to FMP format.
    This is crucial for making the data work with our existing frontend.
    """
    if df is None or df.empty:
        return []
    
    try:
        # Transpose so dates are rows and metrics are columns
        df_t = df.transpose()
        df_t.reset_index(inplace=True)
        
        # The first column is the date (might be named 'Date' or 'index')
        date_col_name = df_t.columns[0]
        df_t.rename(columns={date_col_name: 'date'}, inplace=True)
        
        # Convert date objects to string 'YYYY-MM-DD'
        df_t['date'] = df_t['date'].astype(str).str.slice(0, 10)
        
        # Convert to list of dictionaries for processing
        records = df_t.to_dict('records')
        
        mapped_records = []
        for record in records:
            new_record = {'date': record['date']}
            
            # Helper to safely get value from record, handling potential NaN
            def get_val(keys):
                for k in keys:
                    if k in record and pd.notna(record[k]):
                        return float(record[k])
                return 0.0

            # Map Yahoo specific keys to our FMP standard keys
            new_record['netIncome'] = get_val(['Net Income', 'NetIncome', 'Net Income Common Stockholders'])
            new_record['revenue'] = get_val(['Total Revenue', 'TotalRevenue', 'Operating Revenue'])
            new_record['grossProfit'] = get_val(['Gross Profit', 'GrossProfit'])
            new_record['eps'] = get_val(['Basic EPS', 'BasicEPS'])
            new_record['weightedAverageShsOut'] = get_val(['Basic Average Shares', 'Average Diluted Shares'])
            
            new_record['totalAssets'] = get_val(['Total Assets', 'TotalAssets'])
            new_record['longTermDebt'] = get_val(['Long Term Debt', 'LongTermDebt'])
            new_record['totalCurrentAssets'] = get_val(['Total Current Assets', 'Current Assets'])
            new_record['totalCurrentLiabilities'] = get_val(['Total Current Liabilities', 'Current Liabilities'])
            new_record['totalStockholdersEquity'] = get_val(['Stockholders Equity', 'Total Stockholder Equity'])
            
            new_record['operatingCashFlow'] = get_val(['Operating Cash Flow', 'OperatingCashFlow'])
            new_record['dividendsPaid'] = get_val(['Cash Dividends Paid', 'CashDividendsPaid'])
            
            # Add calendar year for charts
            new_record['calendarYear'] = new_record['date'][:4]
            
            mapped_records.append(new_record)
            
        return mapped_records

    except Exception as e:
        print(f"Error parsing yfinance financials: {e}")
        return []

def get_historical_financials(symbol: str):
    """
    Fetches ANNUAL historical financial statements from Yahoo Finance.
    """
    try:
        ticker = yf.Ticker(symbol)
        return {
            "income": _parse_yfinance_financials(ticker.financials),
            "balance": _parse_yfinance_financials(ticker.balance_sheet),
            "cash_flow": _parse_yfinance_financials(ticker.cashflow),
        }
    except Exception as e:
        print(f"Error fetching yfinance historical financials for {symbol}: {e}")
        return {"income": [], "balance": [], "cash_flow": []}

def get_quarterly_financials(symbol: str):
    """
    Fetches QUARTERLY historical financial statements from Yahoo Finance.
    Critical for CANSLIM.
    """
    try:
        ticker = yf.Ticker(symbol)
        return {
            "income": _parse_yfinance_financials(ticker.quarterly_financials),
            "balance": _parse_yfinance_financials(ticker.quarterly_balance_sheet),
            "cash_flow": _parse_yfinance_financials(ticker.quarterly_cashflow),
        }
    except Exception as e:
        print(f"Error fetching yfinance quarterly financials for {symbol}: {e}")
        return {"income": [], "balance": [], "cash_flow": []}

def get_shareholding_summary(symbol: str):
    """
    Fetches detailed shareholding breakdown.
    """
    try:
        ticker = yf.Ticker(symbol)
        major_holders = ticker.major_holders
        if major_holders is None or major_holders.empty:
            return {}

        # Handle variations in how yfinance returns major_holders
        holders_dict = {}
        if isinstance(major_holders, pd.DataFrame):
             # Sometimes it's (0, 1) cols, sometimes named. We grab by position.
             try:
                holders_dict = dict(zip(major_holders.iloc[:, 1], major_holders.iloc[:, 0]))
             except:
                 pass

        def parse_percent(key_fragment):
            for k, v in holders_dict.items():
                if key_fragment.lower() in str(k).lower():
                    try:
                        return float(str(v).replace('%', '').replace(',', '')) / 100.0 if '%' in str(v) else float(str(v).replace('%', '').replace(',', ''))
                    except: return 0.0
            return 0.0

        insider_percent = parse_percent('insider')
        institutional_percent = parse_percent('institution')
        
        promoter_percent = insider_percent
        # Calculate public as remainder. Max 100.
        public_percent = max(0, 1 - promoter_percent - institutional_percent)
        
        # Convert to 0-100 scale for frontend
        return {
            "promoter": promoter_percent * 100,
            "fii": (institutional_percent * 0.6) * 100,
            "dii": (institutional_percent * 0.4) * 100,
            "public": public_percent * 100,
        }
        
    except Exception as e:
        print(f"Error fetching yfinance shareholding summary for {symbol}: {e}")
        return {}

def get_company_info(symbol: str):
    """
    Fetches company info like sector and industry.
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        if not info or 'symbol' not in info:
            return {}
        return info
    except Exception as e:
        print(f"Error fetching yfinance company info for {symbol}: {e}")
        return {}