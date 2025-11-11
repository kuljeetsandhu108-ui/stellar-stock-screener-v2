import asyncio
from fastapi import APIRouter, HTTPException
import yfinance as yf
import pandas as pd
from ..services import yahoo_service, fmp_service

router = APIRouter()

# --- THE NEW, SMARTER MASTER LIST ---
# We've added 'currency' and 'tradingview_symbol' to each index.
INDEX_MAP = {
    "Nifty 50":           {"symbol": "^NSEI",     "proxy_etf": "INDA", "currency": "INR", "tradingview_symbol": "NSE:NIFTY"},
    "Bank Nifty":         {"symbol": "^NSEBANK",  "proxy_etf": "INDA", "currency": "INR", "tradingview_symbol": "NSE:BANKNIFTY"},
    "Sensex":             {"symbol": "^BSESN",    "proxy_etf": "INDA", "currency": "INR", "tradingview_symbol": "BSE:SENSEX"},
    "Dow Jones":          {"symbol": "^DJI",      "proxy_etf": "DIA",  "currency": "USD", "tradingview_symbol": "DJ:DJI"},
    "Nasdaq":             {"symbol": "^IXIC",     "proxy_etf": "QQQ",  "currency": "USD", "tradingview_symbol": "NASDAQ:IXIC"},
    "Nikkei 225":         {"symbol": "^N225",     "proxy_etf": "EWJ",  "currency": "JPY", "tradingview_symbol": "NIKKEI:NI225"},
    "Gift Nifty":         {"symbol": "NIFTY=F",   "proxy_etf": "INDA", "currency": "USD", "tradingview_symbol": "SGX:IN1!"}, # Futures are often USD denominated
    "India VIX":          {"symbol": "^INDIAVIX", "proxy_etf": None, "currency": "INR", "tradingview_symbol": "NSE:INDIAVIX"},
}

def fetch_summary_data_simple_and_robust():
    # ... (this function does not need to change)
    summary_list = []
    symbols_string = " ".join([info["symbol"] for info in INDEX_MAP.values()])
    tickers = yf.Tickers(symbols_string)
    for name, info in INDEX_MAP.items():
        symbol = info["symbol"]
        try:
            ticker_info = tickers.tickers[symbol].info
            current_price = ticker_info.get('regularMarketPrice')
            previous_close = ticker_info.get('previousClose')
            if current_price is None or previous_close is None: continue
            change = current_price - previous_close
            percent_change = (change / previous_close) * 100
            summary_list.append({
                "name": name, "symbol": symbol, "price": current_price,
                "change": change, "percent_change": percent_change,
            })
        except Exception as e:
            print(f"Could not process summary for {name} ({symbol}): {e}")
            continue
    return summary_list

@router.get("/summary")
async def get_indices_summary():
    # ... (this endpoint does not change)
    summary_data = await asyncio.to_thread(fetch_summary_data_simple_and_robust)
    return summary_data

@router.get("/{index_symbol:path}/live-price")
async def get_index_live_price(index_symbol: str):
    # ... (this endpoint does not change)
    try:
        ticker = yf.Ticker(index_symbol)
        info = ticker.info
        current_price = info.get('regularMarketPrice')
        previous_close = info.get('previousClose')
        if current_price is None or previous_close is None: raise HTTPException(status_code=404, detail="Live price not available.")
        change = current_price - previous_close
        percent_change = (change / previous_close) * 100
        return {"price": current_price, "change": change, "changesPercentage": percent_change}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch live price.")

# --- THE UPDATED DETAILS ENDPOINT ---
@router.get("/{index_symbol:path}/details")
async def get_index_details(index_symbol: str):
    index_name, proxy_etf, currency, tv_symbol = "Index", None, "USD", index_symbol
    for name, data in INDEX_MAP.items():
        if data["symbol"] == index_symbol:
            index_name, proxy_etf, currency, tv_symbol = name, data["proxy_etf"], data["currency"], data["tradingview_symbol"]
            break

    hist_df = await asyncio.to_thread(yahoo_service.get_historical_data, index_symbol, "5y")
    technicals = await asyncio.to_thread(yahoo_service.calculate_technical_indicators, hist_df.copy() if hist_df is not None else None)
    
    if proxy_etf:
        proxy_tasks = {
            "profile": asyncio.to_thread(fmp_service.get_company_profile, proxy_etf),
            "quote": asyncio.to_thread(fmp_service.get_quote, proxy_etf),
            "analyst_ratings": asyncio.to_thread(yahoo_service.get_analyst_recommendations, proxy_etf),
        }
        proxy_results = await asyncio.gather(*proxy_tasks.values(), return_exceptions=True)
        proxy_data = dict(zip(proxy_tasks.keys(), proxy_results))
        for key, value in proxy_data.items():
            if isinstance(value, Exception): proxy_data[key] = {} if isinstance(proxy_data[key], dict) else []
        proxy_data['profile'] = proxy_data['profile'][0] if isinstance(proxy_data['profile'], list) and proxy_data['profile'] else {}
        proxy_data['quote'] = proxy_data['quote'][0] if isinstance(proxy_data['quote'], list) and proxy_data['quote'] else {}
    else:
        proxy_data = {"profile": {}, "quote": {}, "analyst_ratings": []}

    combined_data = {
        "profile": {
            "companyName": index_name,
            "symbol": index_symbol,
            "image": proxy_data.get("profile", {}).get("image"),
            # --- PASSING THE NEW INTELLIGENCE TO THE FRONTEND ---
            "currency": currency,
            "tradingview_symbol": tv_symbol,
        },
        "quote": proxy_data.get("quote", {}),
        "technical_indicators": technicals,
        "analyst_ratings": proxy_data.get("analyst_ratings", []),
    }
    
    return combined_data