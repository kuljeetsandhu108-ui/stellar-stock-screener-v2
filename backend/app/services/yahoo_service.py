import yfinance as yf
import pandas as pd
import pandas_ta as ta

def get_historical_data(symbol: str, period: str = "1y", interval: str = "1d"):
    """
    Fetches historical stock price data from Yahoo Finance for a given ticker.
    This returns a pandas DataFrame, which is ideal for calculations.
    """
    try:
        ticker = yf.Ticker(symbol)
        # Fetch the historical market data
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
        # Use pandas_ta to calculate all indicators and append them to the DataFrame
        df.ta.rsi(length=14, append=True)
        df.ta.macd(fast=12, slow=26, signal=9, append=True)
        df.ta.stoch(k=14, d=3, smooth_k=3, append=True)
        df.ta.adx(length=14, append=True)
        df.ta.atr(length=14, append=True)
        df.ta.willr(length=14, append=True)
        df.ta.bbands(length=20, std=2, append=True)
        
        # Get the very last row, which contains the most recent indicator values
        latest_indicators = df.iloc[-1]

        # Structure the data into a clean dictionary that our frontend component expects
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
    Fetches analyst recommendation data from Yahoo Finance.
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
    Fetches price target data from Yahoo Finance's analysis info.
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