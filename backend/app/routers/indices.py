import asyncio
import pandas as pd
from fastapi import APIRouter, HTTPException
from ..services import yahoo_service, binance_service, redis_service, technical_service

router = APIRouter()

INDICES_CONFIG = [
    {"name": "Nifty 50",    "symbol": "^NSEI",     "currency": "INR"},
    {"name": "Bank Nifty",  "symbol": "^NSEBANK",  "currency": "INR"},
    {"name": "Sensex",      "symbol": "^BSESN",    "currency": "INR"},
    {"name": "India VIX",   "symbol": "^INDIAVIX", "currency": "INR"},
    {"name": "Gold (Global)", "symbol": "GC=F",     "currency": "USD"},
    {"name": "Crude Oil",     "symbol": "CL=F",     "currency": "USD"},
    {"name": "Dow Jones",   "symbol": "^DJI",      "currency": "USD"},
    {"name": "S&P 500",     "symbol": "^GSPC",     "currency": "USD"},
    {"name": "Nasdaq 100",  "symbol": "^IXIC",     "currency": "USD"},
    {"name": "Nikkei 225",  "symbol": "^N225",     "currency": "JPY"},
    {"name": "DAX",         "symbol": "^GDAXI",    "currency": "EUR"},
    {"name": "Bitcoin",     "symbol": "BTCUSDT",   "currency": "USD"},
    {"name": "Ethereum",    "symbol": "ETHUSDT",   "currency": "USD"},
    {"name": "Solana",      "symbol": "SOLUSDT",   "currency": "USD"},
]

@router.get("/summary")
async def get_indices_summary():
    cache_key = "indices_summary_v12"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached:
        return cached

    yahoo_symbols = [item["symbol"] for item in INDICES_CONFIG if not item["symbol"].endswith("USDT")]
    raw_data = await asyncio.to_thread(yahoo_service.get_real_time_bulk, yahoo_symbols)
    data_map = {item["symbol"]: item for item in raw_data} if raw_data else {}
    
    crypto_symbols = [item["symbol"] for item in INDICES_CONFIG if item["symbol"].endswith("USDT")]
    for c_sym in crypto_symbols:
        c_price = await asyncio.to_thread(binance_service.get_crypto_price, c_sym)
        if c_price and c_price.get("price"):
            data_map[c_sym] = {
                "symbol": c_sym,
                "price": c_price.get("price"),
                "change": c_price.get("change"),
                "percent_change": c_price.get("percent_change") or c_price.get("changesPercentage"),
                "volume": c_price.get("volume")
            }

    final_results = []
    for config in INDICES_CONFIG:
        sym = config["symbol"]
        market_data = data_map.get(sym, {})
        final_results.append({
            "name": config["name"],
            "symbol": sym,
            "price": float(market_data.get("price") or market_data.get("close") or 0.0),
            "change": float(market_data.get("change") or 0.0),
            "percent_change": float(market_data.get("percent_change") or market_data.get("changesPercentage") or 0.0),
            "currency": config["currency"]
        })

    if any(x["price"] > 0 for x in final_results):
        await redis_service.redis_client.set_cache(cache_key, final_results, 10)
    
    return final_results

@router.get("/market-mood")
async def get_market_mood():
    cache_key = "stellar_mmi_v12"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached:
        return cached

    try:
        tasks = {
            "nifty": asyncio.to_thread(yahoo_service.get_historical_data, "^NSEI", "1D"),
            "vix": asyncio.to_thread(yahoo_service.get_live_price, "^INDIAVIX")
        }
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        raw = dict(zip(tasks.keys(), results))
        
        nifty_data = raw.get("nifty")
        vix_data = raw.get("vix")

        mmi = 50.0
        status = "Neutral"

        if nifty_data and len(nifty_data) > 30 and vix_data:
            vix = float(vix_data.get("price", 15.0))
            vix_score = max(0, min(100, 100 - ((vix - 10) / 15) * 100))

            df = pd.DataFrame(nifty_data)
            techs = technical_service.calculate_technical_indicators(df)
            mas = technical_service.calculate_moving_averages(df)
            
            rsi = float(techs.get("rsi", 50))
            price = float(nifty_data[-1]["close"])
            sma50 = float(mas.get("50", price))
            diff = (price - sma50) / sma50 if sma50 else 0
            trend_score = max(0, min(100, 50 + (diff * 10) * 100))

            mmi = (vix_score * 0.40) + (rsi * 0.40) + (trend_score * 0.20)

        if mmi <= 30: status, color, desc = "Extreme Fear", "#10B981", "suggests a good time to open fresh positions."
        elif mmi <= 50: status, color, desc = "Fear", "#34D399", "suggests investors are fearful."
        elif mmi <= 70: status, color, desc = "Greed", "#F59E0B", "suggests investors are acting greedily."
        else: status, color, desc = "Extreme Greed", "#EF4444", "suggests caution as markets are overbought."

        res = {"mmi": round(mmi, 2), "status": status, "description": desc, "color": color}
        await redis_service.redis_client.set_cache(cache_key, res, 300)
        return res
    except Exception:
        return {"mmi": 50.0, "status": "Neutral", "description": "Analyzing market data...", "color": "#EDBB5A"}

@router.get("/{index_symbol:path}/details")
async def get_index_details(index_symbol: str):
    is_crypto = binance_service.is_crypto_symbol(index_symbol)
    
    if is_crypto:
        sym = binance_service.format_symbol_for_binance(index_symbol)
        cache_key = f"crypto_idx_v12_{sym}"
        cached = await redis_service.redis_client.get_cache(cache_key)
        if cached:
            return cached

        quote = await asyncio.to_thread(binance_service.get_crypto_price, sym)
        chart_data = await asyncio.to_thread(binance_service.get_crypto_klines, sym, "1D")
        curr = "USD"
        base_name = sym.replace("USDT", "")
        name = f"{base_name} / Tether USD"
        tv_sym = f"BINANCE:{sym}"
    else:
        sym = yahoo_service.format_symbol_for_yahoo(index_symbol)
        cache_key = f"index_details_v12_{sym}"
        cached = await redis_service.redis_client.get_cache(cache_key)
        if cached:
            return cached

        tasks = {
            "chart": asyncio.to_thread(yahoo_service.get_historical_data, sym, "1D"),
            "quote": asyncio.to_thread(yahoo_service.get_live_price, sym)
        }
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        raw = dict(zip(tasks.keys(), results))
        
        chart_data = raw.get("chart", [])
        quote = raw.get("quote", {})
        config_match = next((i for i in INDICES_CONFIG if i["symbol"] == sym), None)
        name = config_match["name"] if config_match else index_symbol
        curr = config_match["currency"] if config_match else ("INR" if "^" in sym or ".NS" in sym else "USD")
        tv_sym = sym

    technicals, mas, pivots = {}, {}, {}
    if chart_data and len(chart_data) > 20:
        try:
            df = pd.DataFrame(chart_data)
            technicals = technical_service.calculate_technical_indicators(df)
            mas = technical_service.calculate_moving_averages(df)
            pivots = technical_service.calculate_pivot_points(df)
        except Exception:
            pass

    profile = {
        "companyName": name, 
        "symbol": sym, 
        "exchange": "BINANCE" if is_crypto else "INDEX",
        "description": f"Global Real-Time Feed for {name}.", 
        "sector": "Digital Asset" if is_crypto else "Market Index",
        "industry": "Cryptocurrency" if is_crypto else "Indices", 
        "image": "", 
        "currency": curr,
        "tradingview_symbol": tv_sym
    }

    final_data = {
        "profile": profile, 
        "quote": quote,
        "technical_indicators": technicals, 
        "moving_averages": mas, 
        "pivot_points": pivots,
        "analyst_ratings": [], 
        "keyStats": {}
    }
    
    await redis_service.redis_client.set_cache(cache_key, final_data, 60)
    return final_data
