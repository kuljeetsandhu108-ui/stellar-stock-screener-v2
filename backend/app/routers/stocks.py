import asyncio
from fastapi import APIRouter, HTTPException, Query, Body
from ..services import fmp_service, yahoo_service, news_service, gemini_service
from pydantic import BaseModel
from typing import List, Dict, Any

class SwotRequest(BaseModel):
    companyName: str
    description: str

class ForecastRequest(BaseModel):
    companyName: str
    analystRatings: List[Dict[str, Any]]
    priceTarget: Dict[str, Any]
    keyStats: Dict[str, Any]
    newsHeadlines: List[str]

router = APIRouter()

@router.get("/search")
async def search_stock_ticker(query: str = Query(..., min_length=2)):
    ticker = gemini_service.get_ticker_from_query(query)
    if ticker in ["NOT_FOUND", "ERROR"]:
        raise HTTPException(status_code=404, detail=f"Could not find a ticker for '{query}'")
    return {"symbol": ticker}

@router.post("/{symbol}/swot")
async def get_swot_analysis(symbol: str, request_data: SwotRequest = Body(...)):
    print(f"Received SWOT request for {symbol}...")
    news_articles = await asyncio.to_thread(news_service.get_company_news, request_data.companyName)
    news_headlines = [article.get('title', '') for article in news_articles[:10]]
    swot_analysis = await asyncio.to_thread(
        gemini_service.generate_swot_analysis,
        request_data.companyName,
        request_data.description,
        news_headlines
    )
    return {"swot_analysis": swot_analysis}

@router.post("/{symbol}/forecast-analysis")
async def get_forecast_analysis(symbol: str, request_data: ForecastRequest = Body(...)):
    print(f"Received AI Forecast Analysis request for {symbol}...")
    analysis = await asyncio.to_thread(
        gemini_service.generate_forecast_analysis,
        company_name=request_data.companyName,
        analyst_ratings=request_data.analystRatings,
        price_target=request_data.priceTarget,
        key_stats=request_data.keyStats,
        news_headlines=request_data.newsHeadlines
    )
    return {"analysis": analysis}


@router.get("/{symbol}/all")
async def get_all_stock_data(symbol: str):
    """
    DEFINITIVE VERSION: Uses yfinance as the primary source for robust forecast data.
    """
    # Define all the data fetching tasks we need to run.
    tasks = {
        # FMP is still our primary source for these items.
        "profile": asyncio.to_thread(fmp_service.get_company_profile, symbol),
        "quote": asyncio.to_thread(fmp_service.get_quote, symbol),
        "key_metrics": asyncio.to_thread(fmp_service.get_key_metrics, symbol, "annual", 1),
        "analyst_estimates": asyncio.to_thread(fmp_service.get_analyst_estimates, symbol),
        "shareholding": asyncio.to_thread(fmp_service.get_shareholding_data, symbol),
        "annual_revenue_and_profit": asyncio.to_thread(fmp_service.get_financial_statements, symbol, "income-statement", "annual", 5),
        "news": asyncio.to_thread(news_service.get_company_news, symbol),

        # --- YFINANCE IS NOW OUR RELIABLE SOURCE FOR FORECASTS ---
        "analyst_ratings": asyncio.to_thread(yahoo_service.get_analyst_recommendations, symbol),
        "price_target_consensus": asyncio.to_thread(yahoo_service.get_price_target_data, symbol),
    }

    # Run all tasks concurrently.
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    data = dict(zip(tasks.keys(), results))

    # --- Technical Indicator calculation is now 100% yfinance-based for reliability ---
    print(f"Calculating technical indicators for {symbol} via Yahoo Finance.")
    hist_df = await asyncio.to_thread(yahoo_service.get_historical_data, symbol, "1y")
    calculated_technicals = await asyncio.to_thread(yahoo_service.calculate_technical_indicators, hist_df)
    data['technical_indicators'] = calculated_technicals
    
    # Handle any errors that may have occurred during the async calls.
    for key, value in data.items():
        if isinstance(value, Exception):
            print(f"Error fetching '{key}' for {symbol}: {value}")
            data[key] = {} if isinstance(data[key], dict) else []
    
    # Clean up data that comes back as a list.
    data['profile'] = data['profile'][0] if isinstance(data['profile'], list) and data['profile'] else data.get('profile', {})
    data['quote'] = data['quote'][0] if isinstance(data['quote'], list) and data['quote'] else data.get('quote', {})
    data['key_metrics'] = data['key_metrics'][0] if isinstance(data['key_metrics'], list) and data['key_metrics'] else data.get('key_metrics', {})
    
    # Consolidate Key Stats into a single, clean object for the frontend.
    profile_data = data.get('profile', {})
    quote_data = data.get('quote', {})
    metrics_data = data.get('key_metrics', {})
    estimates_data = data.get('analyst_estimates', {})
    
    data['keyStats'] = {
        "marketCap": profile_data.get('mktCap'),
        "dividendYield": metrics_data.get('dividendYieldTTM'),
        "peRatio": metrics_data.get('peRatioTTM'),
        "basicEPS": metrics_data.get('epsTTM'),
        "netIncome": metrics_data.get('netIncomePerShareTTM'),
        "revenue": metrics_data.get('revenuePerShareTTM'),
        "sharesFloat": quote_data.get('sharesOutstanding'),
        "beta": profile_data.get('beta'),
        "employees": profile_data.get('fullTimeEmployees'),
        "nextReportDate": estimates_data.get('date'),
        "epsEstimate": estimates_data.get('estimatedEpsAvg'),
        "revenueEstimate": estimates_data.get('estimatedRevenueAvg'),
    }
    
    return data