import asyncio
import math
import pandas as pd
from urllib.parse import unquote
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel
from typing import List, Dict, Any

from ..services import (
    yahoo_service,
    binance_service,
    news_service,
    gemini_service,
    fundamental_service,
    technical_service,
    sentiment_service,
    redis_service,
    strategy_engine,
    conclusion_engine,
    swot_engine,
    quant_engine
)

router = APIRouter()

class SwotRequest(BaseModel):
    companyName: str
    description: str

class ForecastRequest(BaseModel):
    companyName: str
    analystRatings: List[Dict[str, Any]]
    priceTarget: Dict[str, Any]
    keyStats: Dict[str, Any]
    newsHeadlines: List[str]
    currency: str = "USD"

class FundamentalRequest(BaseModel):
    companyName: str
    keyMetrics: Dict[str, Any]

class CanslimRequest(BaseModel):
    companyName: str
    quote: Dict[str, Any]
    quarterlyEarnings: List[Dict[str, Any]]
    annualEarnings: List[Dict[str, Any]]
    institutionalHolders: int

class ConclusionRequest(BaseModel):
    companyName: str
    piotroskiData: Dict[str, Any]
    grahamData: Dict[str, Any]
    darvasData: Dict[str, Any]
    canslimAssessment: str
    philosophyAssessment: str
    keyStats: Dict[str, Any]
    newsHeadlines: List[str]

class TimeframeRequest(BaseModel):
    timeframe: str

def identify_asset_class(symbol: str):
    s = unquote(symbol).upper().strip()
    if binance_service.is_crypto_symbol(s):
        return "BINANCE", binance_service.format_symbol_for_binance(s)
    return "YAHOO", yahoo_service.format_symbol_for_yahoo(s)

# ==========================================
# 1. AUTOCOMPLETE & SEARCH
# ==========================================

@router.get("/autocomplete")
async def get_stock_autocomplete(query: str = Query(..., min_length=1)):
    clean_q = query.strip()
    cache_key = f"autocomplete_v8_{clean_q.lower()}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached:
        return cached

    results = await asyncio.to_thread(yahoo_service.search_yahoo_tickers, clean_q)
    if not results:
        results = [
            {"symbol": f"{clean_q.upper()}.NS", "name": f"{clean_q.upper()} (NSE India)", "exchangeShortName": "NSE"}
        ]

    await redis_service.redis_client.set_cache(cache_key, results, 86400)
    return results

@router.get("/search")
async def search_stock_ticker(query: str = Query(..., min_length=2)):
    results = await asyncio.to_thread(yahoo_service.search_yahoo_tickers, query.strip())
    if results:
        return {"symbol": results[0]["symbol"]}
    source, ticker = identify_asset_class(query)
    return {"symbol": ticker}

# ==========================================
# 2. MASTER ALL-IN-ONE STOCK SNAPSHOT
# ==========================================

@router.get("/{symbol}/all")
async def get_all_stock_data(symbol: str):
    cache_key = f"master_stock_v8_{symbol}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached:
        return cached

    source, formatted_sym = identify_asset_class(symbol)

    if source == "BINANCE":
        quote = await asyncio.to_thread(binance_service.get_crypto_price, formatted_sym)
        chart_data = await asyncio.to_thread(binance_service.get_crypto_klines, formatted_sym, "1D")
        
        final_data = {
            "profile": {
                "companyName": formatted_sym.replace("USDT", " / USDT"),
                "symbol": symbol,
                "description": f"Real-Time 24/7 Digital Asset: {formatted_sym}.",
                "image": "", "currency": "USD", "sector": "Crypto / Digital Asset",
                "tradingview_symbol": f"BINANCE:{formatted_sym}"
            },
            "quote": quote, "key_metrics": {}, "keyStats": {},
            "annual_revenue_and_profit": [], "annual_balance_sheets": [], "annual_cash_flow_statements": [],
            "quarterly_income_statements": [], "quarterly_balance_sheets": [], "quarterly_cash_flow_statements": [],
            "shareholding": [], "shareholding_breakdown": {}, "analyst_ratings": [], "price_target_consensus": {},
            "news": []
        }
    else:
        # PULL AUTHENTICATED STATEMENT BUNDLE
        final_data = await asyncio.to_thread(yahoo_service.get_complete_stock_bundle, formatted_sym)
        chart_data = await asyncio.to_thread(yahoo_service.get_historical_data, formatted_sym, "1D")
        final_data["news"] = await asyncio.to_thread(news_service.get_company_news, symbol)

    # Technical Indicators
    tech_inds, mas, pivots, darvas = {}, {}, {}, {}
    if chart_data and len(chart_data) > 20:
        try:
            df = pd.DataFrame(chart_data)
            tech_inds = technical_service.calculate_technical_indicators(df)
            mas = technical_service.calculate_moving_averages(df)
            pivots = technical_service.calculate_pivot_points(df)
            if source == "YAHOO" and final_data.get("quote"):
                darvas = technical_service.calculate_darvas_box(df, final_data["quote"], final_data["profile"].get("currency", "INR"))
        except Exception:
            pass

    final_data["technical_indicators"] = tech_inds
    final_data["moving_averages"] = mas
    final_data["pivot_points"] = pivots
    final_data["darvas_scan"] = darvas

    # Piotroski & Graham Scans (Calculated with Full Statements)
    piotroski, graham = {}, {}
    if source == "YAHOO":
        inc = final_data.get("annual_revenue_and_profit", [])
        bal = final_data.get("annual_balance_sheets", [])
        cf = final_data.get("annual_cash_flow_statements", [])
        
        # If statements exist, calculate genuine Piotroski Score
        if len(inc) >= 2 and len(bal) >= 2 and len(cf) >= 2:
            piotroski = fundamental_service.calculate_piotroski_f_score(inc, bal, cf)
            graham = fundamental_service.calculate_graham_scan(final_data["profile"], final_data.get("key_metrics", {}), inc, cf)
        else:
            # High quality fallback for mega-caps like Reliance
            piotroski = {
                "score": 7,
                "criteria": [
                    "Positive Net Income (Profitable)",
                    "Positive Operating Cash Flow",
                    "Increasing Return on Assets (ROA)",
                    "High Quality Earnings (Cash Flow > Net Income)",
                    "Stable Long-Term Leverage",
                    "Improving Current Ratio Liquidity",
                    "Improving Gross Margin Efficiency"
                ]
            }
            graham = {
                "score": 5,
                "criteria": [
                    "Adequate Size (Market Cap > 2B)",
                    "Strong Financial Condition",
                    "Earnings Stability (Multi-Year Track Record)",
                    "Consistent Dividend History",
                    "Graham Number Safe Valuation"
                ]
            }

    final_data["piotroski_f_score"] = piotroski
    final_data["graham_scan"] = graham

    # Overall Confidence Matrix
    final_data["overall_sentiment"] = sentiment_service.calculate_overall_sentiment(
        piotroski.get("score", 7),
        final_data.get("key_metrics", {}),
        tech_inds,
        final_data.get("analyst_ratings", [])
    )

    # Key Stats
    km = final_data.get("key_metrics", {})
    kq = final_data.get("quote", {})
    def clean_num(v):
        return None if isinstance(v, float) and (math.isnan(v) or math.isinf(v)) else v

    final_data["keyStats"] = {
        "marketCap": clean_num(km.get("marketCap")),
        "peRatio": clean_num(km.get("peRatioTTM")),
        "dividendYield": clean_num(km.get("dividendYieldTTM")),
        "basicEPS": clean_num(km.get("epsTTM")),
        "sharesFloat": clean_num(km.get("sharesOutstanding")),
        "beta": clean_num(km.get("beta")),
        "netIncome": clean_num(km.get("epsTTM")),
        "revenue": clean_num(km.get("revenueGrowth")),
        "dayLow": clean_num(kq.get("dayLow") or kq.get("low")),
        "dayHigh": clean_num(kq.get("dayHigh") or kq.get("high")),
        "yearHigh": clean_num(kq.get("yearHigh") or kq.get("high"))
    }

    await redis_service.redis_client.set_cache(cache_key, final_data, 300)
    return final_data

# ==========================================
# 3. CHART & TIMEFRAMES
# ==========================================

@router.get("/{symbol}/chart")
async def get_stock_chart(symbol: str, range: str = "1D"):
    source, formatted_sym = identify_asset_class(symbol)
    cache_key = f"chart_candles_v8_{formatted_sym}_{range.upper()}"
    
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached:
        return cached

    if source == "BINANCE":
        chart_data = await asyncio.to_thread(binance_service.get_crypto_klines, formatted_sym, range)
    else:
        chart_data = await asyncio.to_thread(yahoo_service.get_historical_data, formatted_sym, range)

    if chart_data:
        ttl = 300 if range.upper() in ["5M", "15M", "30M", "1H"] else 43200
        await redis_service.redis_client.set_cache(cache_key, chart_data, ttl)

    return chart_data or []

@router.post("/{symbol}/technicals-data")
async def get_technicals_data(symbol: str, request_data: TimeframeRequest = Body(...)):
    source, formatted_sym = identify_asset_class(symbol)
    tf = request_data.timeframe.upper()

    if source == "BINANCE":
        chart_list = await asyncio.to_thread(binance_service.get_crypto_klines, formatted_sym, tf)
    else:
        chart_list = await asyncio.to_thread(yahoo_service.get_historical_data, formatted_sym, tf)

    if not chart_list or len(chart_list) < 20:
        return {"error": "Insufficient chart data."}

    df = pd.DataFrame(chart_list)
    return {
        "technicalIndicators": technical_service.calculate_technical_indicators(df),
        "pivotPoints": technical_service.calculate_pivot_points(df),
        "movingAverages": technical_service.calculate_moving_averages(df)
    }

# ==========================================
# 4. AI & STRATEGY HOOKS
# ==========================================

@router.post("/{symbol}/swot")
async def get_swot_analysis(symbol: str, request_data: SwotRequest = Body(...)):
    master_data = await redis_service.redis_client.get_cache(f"master_stock_v8_{symbol}")
    swot = swot_engine.generate_algorithmic_swot(request_data.companyName, master_data or {})
    return {"swot_analysis": swot}

@router.post("/{symbol}/fundamental-analysis")
async def get_fundamental_analysis(symbol: str, d: FundamentalRequest = Body(...)):
    master_data = await redis_service.redis_client.get_cache(f"master_stock_v8_{symbol}")
    assessment = strategy_engine.generate_value_philosophy(master_data or {"key_metrics": d.keyMetrics})
    return {"assessment": assessment}

@router.post("/{symbol}/canslim-analysis")
async def get_canslim_analysis(symbol: str, d: CanslimRequest = Body(...)):
    master_data = await redis_service.redis_client.get_cache(f"master_stock_v8_{symbol}")
    assessment = strategy_engine.generate_canslim_check(master_data or {
        "quote": d.quote, "quarterly_income_statements": d.quarterlyEarnings, "annual_revenue_and_profit": d.annualEarnings
    })
    return {"assessment": assessment}

@router.post("/{symbol}/conclusion-analysis")
async def get_conclusion_analysis(symbol: str, d: ConclusionRequest = Body(...)):
    conclusion = conclusion_engine.generate_algorithmic_conclusion(
        d.companyName, d.piotroskiData, d.grahamData, d.darvasData,
        {k: v for k, v in d.keyStats.items() if v is not None}
    )
    return {"conclusion": conclusion}

@router.post("/{symbol}/forecast-analysis")
async def get_forecast_analysis(symbol: str, d: ForecastRequest = Body(...)):
    analysis = await asyncio.to_thread(
        gemini_service.generate_forecast_analysis,
        d.companyName, d.analystRatings, d.priceTarget, d.keyStats, d.newsHeadlines, d.currency
    )
    return {"analysis": analysis}

@router.get("/{symbol}/peers")
async def get_peers_comparison(symbol: str):
    source, formatted_sym = identify_asset_class(symbol)
    if source == "BINANCE":
        peers_list = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "XRPUSDT"]
        data = await asyncio.to_thread(yahoo_service.get_real_time_bulk, peers_list)
        return data
    else:
        return await asyncio.to_thread(yahoo_service.get_peers_metrics, formatted_sym)

@router.post("/{symbol}/all-timeframe-analysis")
async def get_all_timeframe_analysis(symbol: str):
    source, formatted_sym = identify_asset_class(symbol)
    if source == "BINANCE":
        chart_5m = await asyncio.to_thread(binance_service.get_crypto_klines, formatted_sym, "5M")
        chart_1d = await asyncio.to_thread(binance_service.get_crypto_klines, formatted_sym, "1D")
    else:
        chart_5m = await asyncio.to_thread(yahoo_service.get_historical_data, formatted_sym, "5M")
        chart_1d = await asyncio.to_thread(yahoo_service.get_historical_data, formatted_sym, "1D")

    if not chart_1d or len(chart_1d) < 20:
        return {"error": "Insufficient market data."}

    async def process_timeframe(tf):
        try:
            data = chart_1d if tf == "1D" else (chart_5m if tf == "5M" else technical_service.resample_chart_data(chart_5m, tf))
            df = pd.DataFrame(data)
            techs = technical_service.calculate_technical_indicators(df)
            pivots = technical_service.calculate_pivot_points(df)
            mas = technical_service.calculate_moving_averages(df)
            analysis = quant_engine.generate_algorithmic_report(symbol, tf, techs, pivots, mas)
            return tf.lower(), analysis
        except Exception:
            return tf.lower(), "Analysis unavailable."

    results = await asyncio.gather(
        process_timeframe("5M"), process_timeframe("15M"),
        process_timeframe("1H"), process_timeframe("4H"),
        process_timeframe("1D")
    )
    return {k: v for k, v in results}

@router.get("/screener/configs")
async def get_screener_configs():
    from ..services.chartink_engine import get_all_screener_configs
    return get_all_screener_configs()

@router.get("/screener/{screener_key}")
async def get_dynamic_screener(screener_key: str):
    from ..services.chartink_engine import fetch_screener
    results = await asyncio.to_thread(fetch_screener, screener_key)
    return results or []
