import yfinance as yf
import pandas as pd
import pandas_ta as ta

def get_historical_data(symbol: str, period: str = "1y", interval: str = "1d"):
    """
    Fetches historical stock price data from Yahoo Finance for a given ticker.
    This now returns a PANDAS DATAFRAME instead of a list of dictionaries.
    """
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period, interval=interval)
        
        if hist.empty:
            print(f"Warning: No historical data found for symbol '{symbol}'.")
            return None
        
        # Ensure column names are lowercase for pandas_ta compatibility
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
        # Calculate all the indicators we need using pandas_ta
        df.ta.rsi(length=14, append=True)
        df.ta.macd(fast=12, slow=26, signal=9, append=True)
        df.ta.stoch(k=14, d=3, smooth_k=3, append=True)
        df.ta.adx(length=14, append=True)
        df.ta.atr(length=14, append=True)
        df.ta.willr(length=14, append=True)
        df.ta.bbands(length=20, std=2, append=True)
        
        # Get the very last row which contains the most recent indicator values
        latest_indicators = df.iloc[-1]

        # Structure the data to match what our frontend component expects
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