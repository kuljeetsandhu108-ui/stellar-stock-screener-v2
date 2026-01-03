import asyncio
from fastapi import APIRouter, HTTPException
import yfinance as yf
import pandas as pd
from ..services import yahoo_service, fmp_service, technical_service

router = APIRouter()

# ==========================================
# 1. MASTER INDEX CONFIGURATION
# ==========================================
# We map indices to "Proxy ETFs" to get logos and descriptions,
# but we fetch prices from the actual Index Symbol.

INDEX_MAP = {
    # Indian Markets
    "Nifty 50":           {"symbol": "^NSEI",     "proxy_etf": "INDA", "currency": "INR", "tradingview_symbol": "NSE:NIFTY"},
    "Bank Nifty":         {"symbol": "^NSEBANK",  "proxy_etf": "INDA", "currency": "INR", "tradingview_symbol": "NSE:BANKNIFTY"},
    "Sensex":             {"symbol": "^BSESN",    "proxy_etf": "INDA", "currency": "INR", "tradingview_symbol": "BSE:SENSEX"},
    "India VIX":          {"symbol": "^INDIAVIX", "proxy_etf": None,   "currency": "INR", "tradingview_symbol": "NSE:INDIAVIX"},
    "Gift Nifty":         {"symbol": "NIFTY=F",   "proxy_etf": "INDA", "currency": "USD", "tradingview_symbol": "SGX:IN1!"},

    # US & Global Markets
    "Dow Jones":          {"symbol": "^DJI",      "proxy_etf": "DIA",  "currency": "USD", "tradingview_symbol": "DJ:DJI"},
    "Nasdaq":             {"symbol": "^IXIC",     "proxy_etf": "QQQ",  "currency": "USD", "tradingview_symbol": "NASDAQ:IXIC"},
    "S&P 500":            {"symbol": "^GSPC",     "proxy_etf": "SPY",  "currency": "USD", "tradingview_symbol": "AMEX:SPY"},
    "Nikkei 225":         {"symbol": "^N225",     "proxy_etf": "EWJ",  "currency": "JPY", "tradingview_symbol": "NIKKEI:NI225"},
    
    # Commodities & Crypto
    "Gold":               {"symbol": "GC=F",      "proxy_etf": "GLD",  "currency": "USD", "tradingview_symbol": "TVC:GOLD"},
    "Crude Oil":          {"symbol": "CL=F",      "proxy_etf": "USO",  "currency": "USD", "tradingview_symbol": "TVC:USOIL"},
    "Bitcoin":            {"symbol": "BTC-USD",   "proxy_etf": "BITO", "currency": "USD", "tradingview_symbol": "BINANCE:BTCUSD"},
}

# ==========================================
# 2. HOMEPAGE BANNER DATA
# ==========================================

def fetch_summary_data():
    """
    Fetches live price, change, and % change for the scrolling banner.
    Uses Batch Fetching for speed.
    """
    summary_list = []
    # Create space-separated string of all symbols for yfinance
    symbols = [info["symbol"] for info in INDEX_MAP.values()]
    symbols_str = " ".join(symbols)
    
    try:
        # 1. Batch Fetch
        tickers = yf.Tickers(symbols_str)
        
        for name, info in INDEX_MAP.items():
            symbol = info["symbol"]
            try:
                ticker = tickers.tickers[symbol]
                
                # 2. Extract Price (Try Fast Info first, then Standard Info)
                price = None
                prev_close = None
                
                if hasattr(ticker, 'fast_info'):
                    price = ticker.fast_info.last_price
                    prev_close = ticker.fast_info.previous_close
                
                if price is None:
                    # Fallback to standard info dict
                    info_dict = ticker.info
                    price = info_dict.get('regularMarketPrice') or info_dict.get('currentPrice')
                    prev_close = info_dict.get('previousClose') or info_dict.get('regularMarketPreviousClose')

                if price is None or prev_close is None:
                    continue

                # 3. Calculate Change
                change = price - prev_close
                pct_change = (change / prev_close) * 100
                
                summary_list.append({
                    "name": name, 
                    "symbol": symbol, 
                    "price": price,
                    "change": change, 
                    "percent_change": pct_change,
                    "currency": info["currency"]
                })
            except Exception as e:
                # Silently skip failed indices to keep the banner running
                continue
                
    except Exception as e:
        print(f"Index Summary Fetch Error: {e}")
        return []
        
    return summary_list

@router.get("/summary")
async def get_indices_summary():
    """Endpoint for the Homepage Ticker Tape."""
    data = await asyncio.to_thread(fetch_summary_data)
    return data

@router.get("/{index_symbol:path}/live-price")
async def get_index_live_price(index_symbol: str):
    """Lightweight endpoint for refreshing the header price."""
    try:
        ticker = yf.Ticker(index_symbol)
        
        # Fast Info approach
        if hasattr(ticker, 'fast_info'):
            price = ticker.fast_info.last_price
            prev = ticker.fast_info.previous_close
            if price and prev:
                return {
                    "price": price, 
                    "change": price - prev, 
                    "changesPercentage": ((price - prev)/prev)*100
                }
        
        # Standard Info approach
        info = ticker.info
        price = info.get('regularMarketPrice')
        prev = info.get('previousClose')
        
        if price is None or prev is None:
             raise HTTPException(status_code=404, detail="Price unavailable")

        return {
            "price": price, 
            "change": price - prev, 
            "changesPercentage": ((price - prev)/prev)*100
        }
    except Exception:
        raise HTTPException(status_code=404, detail="Price unavailable")

# ==========================================
# 3. INDEX DETAILS (THE DEEP DIVE)
# ==========================================

@router.get("/{index_symbol:path}/details")
async def get_index_details(index_symbol: str):
    """
    The Smart Aggregator for Index Pages.
    Combines:
    1. Real Index Price & Technicals (from Index Symbol)
    2. Rich Metadata & Ratings (from Proxy ETF)
    """
    
    # 1. Identify Index & Configuration
    index_name = "Market Index"
    proxy_etf = None
    currency = "USD"
    tv_symbol = index_symbol
    
    # Check if we know this index in our map
    for name, data in INDEX_MAP.items():
        if data["symbol"] == index_symbol:
            index_name = name
            proxy_etf = data["proxy_etf"]
            currency = data["currency"]
            tv_symbol = data["tradingview_symbol"]
            break
            
    # Heuristic for unknown indices (e.g. user search)
    if index_name == "Market Index":
        if ".NS" in index_symbol or "^NSE" in index_symbol:
            currency = "INR"

    # 2. Fetch Historical Data (Crucial for Technicals)
    hist_df = await asyncio.to_thread(yahoo_service.get_historical_data, index_symbol, "5y")
    
    # 3. Calculate Technicals (Server-Side Math)
    # We pass copies of the DF to prevent conflicts
    technicals = await asyncio.to_thread(
        yahoo_service.calculate_technical_indicators, 
        hist_df.copy() if hist_df is not None else None
    )
    
    moving_averages = technical_service.calculate_moving_averages(
        hist_df.copy() if hist_df is not None else None
    )
    
    pivot_points = technical_service.calculate_pivot_points(
        hist_df.copy() if hist_df is not None else None
    )
    
    # 4. Fetch Live Quote (from the INDEX, not the ETF)
    index_quote = await asyncio.to_thread(yahoo_service.get_quote, index_symbol)

    # 5. Fetch Proxy Metadata (from the ETF)
    # Indices don't have descriptions/logos, so we steal them from the ETF.
    proxy_profile = {}
    proxy_ratings = []
    
    if proxy_etf:
        p_data = await asyncio.to_thread(fmp_service.get_company_profile, proxy_etf)
        r_data = await asyncio.to_thread(yahoo_service.get_analyst_recommendations, proxy_etf)
        
        if p_data: proxy_profile = p_data
        if r_data: proxy_ratings = r_data

    # 6. Construct Final Response
    final_profile = {
        "companyName": index_name,
        "symbol": index_symbol,
        "exchange": proxy_profile.get("exchange", "INDEX"),
        "description": proxy_profile.get("description", f"Detailed market analysis for {index_name}."),
        "sector": "Index",
        "industry": "Global Markets",
        "image": proxy_profile.get("image"), # Use ETF logo
        "currency": currency,
        "tradingview_symbol": tv_symbol,
    }

    combined_data = {
        "profile": final_profile,
        "quote": index_quote,             # Correct Index Price
        "technical_indicators": technicals,
        "moving_averages": moving_averages, # Populates Technical Meter
        "pivot_points": pivot_points,       # Populates Levels
        "analyst_ratings": proxy_ratings,   # Proxy Sentiment
    }
    
    return combined_data