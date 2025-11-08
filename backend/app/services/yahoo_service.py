import yfinance as yf
from pandas import DataFrame

def get_historical_data(symbol: str, period: str = "5y", interval: str = "1d") -> list:
    """
    Fetches historical stock price data from Yahoo Finance for a given ticker.
    This data is ideal for charting libraries.
    
    Args:
        symbol (str): The stock ticker symbol (e.g., "AAPL", "MSFT").
        period (str): The time period for the data (e.g., "1d", "5d", "1mo", "1y", "5y", "max").
        interval (str): The data interval (e.g., "1m", "2m", "1d", "1wk", "1mo").

    Returns:
        list: A list of dictionaries, where each dictionary represents a time point
              with keys like 'Date', 'Open', 'High', 'Low', 'Close', 'Volume'.
              Returns an empty list if the ticker is invalid or data cannot be fetched.
    """
    try:
        ticker = yf.Ticker(symbol)
        
        # Fetch the historical market data
        hist: DataFrame = ticker.history(period=period, interval=interval)
        
        if hist.empty:
            print(f"Warning: No historical data found for symbol '{symbol}'. It may be an invalid ticker.")
            return []
            
        # Reset the index to turn the 'Date' index into a column
        hist = hist.reset_index()
        
        # Convert the 'Date' column to a string format 'YYYY-MM-DD'
        # TradingView and other libraries often work best with this format.
        # We need to handle both datetime and date objects.
        if 'Date' in hist.columns:
            hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d')
        elif 'Datetime' in hist.columns:
            hist.rename(columns={'Datetime': 'Date'}, inplace=True)
            hist['Date'] = hist['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Convert the DataFrame to a list of dictionaries, which is a common JSON format
        return hist.to_dict('records')

    except Exception as e:
        print(f"An error occurred while fetching historical data for {symbol} from yfinance: {e}")
        return []

def get_company_info(symbol: str) -> dict:
    """
    Fetches general company information and summary from Yahoo Finance.
    This can supplement data from FMP if needed.
    """
    try:
        ticker = yf.Ticker(symbol)
        
        # The .info dictionary contains a wealth of information
        info = ticker.info
        
        if not info or 'symbol' not in info:
             print(f"Warning: No company info found for symbol '{symbol}'.")
             return {}

        return info
        
    except Exception as e:
        print(f"An error occurred while fetching company info for {symbol} from yfinance: {e}")
        return {}