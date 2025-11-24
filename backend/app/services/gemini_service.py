import os
import google.generativeai as genai
from dotenv import load_dotenv
import itertools

load_dotenv()

# --- THE API KEY ROTATOR ---
try:
    GEMINI_API_KEYS_STR = os.getenv("GEMINI_API_KEYS")
    if not GEMINI_API_KEYS_STR:
        raise ValueError("GEMINI_API_KEYS not found in .env file. Please add it as a comma-separated list.")
    
    GEMINI_API_KEYS = [key.strip() for key in GEMINI_API_KEYS_STR.split(',')]
    
    key_cycler = itertools.cycle(GEMINI_API_KEYS)
    print(f"Successfully loaded and initialized rotator for {len(GEMINI_API_KEYS)} Gemini API keys.")

except (ValueError, AttributeError) as e:
    print(f"CRITICAL ERROR: Could not load Gemini API keys. AI features will fail. Error: {e}")
    GEMINI_API_KEYS = []
    key_cycler = None

def configure_gemini_for_request():
    """Configures the genai library with the next available key from the pool."""
    if not key_cycler:
        raise ValueError("No Gemini API keys are configured or available.")
    
    api_key = next(key_cycler)
    genai.configure(api_key=api_key)


# --- All functions are now wrapped to use the rotator and accept **kwargs ---

def get_ticker_from_query(query: str):
    """Uses the Gemini model with a rotated API key to find a stock ticker."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""Analyze the following user query: "{query}". Return ONLY the official stock ticker symbol (e.g., "AAPL" for Apple, "RELIANCE.NS" for Reliance Industries). If a clear ticker cannot be found, return the text "NOT_FOUND"."""
        response = model.generate_content(prompt)
        return response.text.strip().replace("`", "").upper()
    except Exception as e:
        print(f"An error occurred in get_ticker_from_query: {e}")
        return "ERROR"

def generate_swot_analysis(company_name: str, description: str, news_headlines: list):
    """Generates a SWOT analysis with a rotated API key."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Robust Data Handling: Provide defaults if data is missing
        safe_desc = description if description else f"A publicly traded company named {company_name}."
        safe_news = "\n- ".join(news_headlines) if news_headlines else "No recent news headlines available."
        
        prompt = f"""
        Generate a professional SWOT analysis for {company_name}.
        
        **Context:**
        - Description: {safe_desc}
        - Recent News:
        {safe_news}

        **Strict Output Format:**
        You must provide 4 distinct sections. Use the exact headers below:
        **Strengths**
        - point 1
        - point 2
        **Weaknesses**
        - point 1
        - point 2
        **Opportunities**
        - point 1
        - point 2
        **Threats**
        - point 1
        - point 2
        
        Do not add introductory text. Just the headers and bullet points.
        """
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred in generate_swot_analysis: {e}")
        return f"**Strengths**\n- Data unavailable\n**Weaknesses**\n- Data unavailable\n**Opportunities**\n- Data unavailable\n**Threats**\n- Data unavailable"

def generate_forecast_analysis(**kwargs):
    """Generates a forecast analysis with a rotated API key, accepting kwargs."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        company_name = kwargs.get('companyName')
        analyst_ratings = kwargs.get('analystRatings', [])
        price_target = kwargs.get('priceTarget', {})
        key_stats = kwargs.get('keyStats', {})
        news_headlines = kwargs.get('newsHeadlines', [])
        
        ratings_summary = "\n".join([f"- {r.get('ratingStrongBuy', 0)} Strong Buy, {r.get('ratingBuy', 0)} Buy, {r.get('ratingHold', 0)} Hold" for r in analyst_ratings[:1]])
        news_string = "\n- ".join(news_headlines)
        prompt = f"""Act as a professional financial analyst. For {company_name}, write a two-paragraph summary of the analyst forecast based on the following data:\n- **Analyst Ratings:** {ratings_summary}\n- **Price Target:** High ${price_target.get('targetHigh')}, Average ${price_target.get('targetConsensus')}\n- **Key Financials:** P/E Ratio {key_stats.get('peRatio')}, EPS {key_stats.get('basicEPS')}\n- **Recent News:**\n- {news_string}"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred in generate_forecast_analysis: {e}")
        return "Could not generate AI forecast analysis."

def generate_investment_philosophy_assessment(**kwargs):
    """Generates a philosophy assessment with a rotated API key, accepting kwargs."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        company_name = kwargs.get('companyName')
        key_metrics = kwargs.get('keyMetrics', {})
        
        pe_ratio = key_metrics.get('peRatioTTM', 'N/A')
        earnings_yield = key_metrics.get('earningsYieldTTM', 'N/A')
        roc = key_metrics.get('returnOnCapitalEmployedTTM', 'N/A')

        data_summary = f"""- Price to Earnings (P/E) Ratio: {pe_ratio if isinstance(pe_ratio, str) else f'{pe_ratio:.2f}'}\n- Earnings Yield (E/P): {earnings_yield if isinstance(earnings_yield, str) else f'{earnings_yield:.4f}'}\n- Return on Capital (ROC): {roc if isinstance(roc, str) else f'{roc:.4f}'}"""
        
        prompt = f"""Act as an analyst. For {company_name}, assess it against 3 philosophies (Magic Formula, Warren Buffett, Coffee Can) based on these metrics:\n{data_summary}\nOutput a clean, 2-column Markdown table with headers "Formula" and "Assessment", naturally incorporating metric values in the text."""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred in generate_investment_philosophy_assessment: {e}")
        return "Could not generate AI assessment."

def generate_canslim_assessment(company_name: str, quote: dict, quarterly_earnings: list, annual_earnings: list, institutional_holders: int):
    """Generates a CANSLIM assessment with robust math."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        c_growth = "N/A"
        # Check if we have data
        if quarterly_earnings and len(quarterly_earnings) >= 2:
            latest_q = quarterly_earnings[0].get('eps', 0)
            # Try Year-over-Year (4 quarters ago) first
            if len(quarterly_earnings) >= 5:
                prev_q = quarterly_earnings[4].get('eps', 0)
                period = "YoY"
            else:
                # Fallback to Quarter-over-Quarter if history is short
                prev_q = quarterly_earnings[1].get('eps', 0)
                period = "QoQ"
            
            if prev_q != 0 and latest_q is not None and prev_q is not None:
                c_growth_val = ((latest_q - prev_q) / abs(prev_q)) * 100
                c_growth = f"{c_growth_val:.2f}% ({period})"

        a_growth = "N/A"
        if annual_earnings and len(annual_earnings) >= 2:
            latest_y = annual_earnings[0].get('eps', 0)
            prev_y = annual_earnings[1].get('eps', 0)
            if prev_y != 0 and latest_y is not None and prev_y is not None:
                a_growth_val = ((latest_y - prev_y) / abs(prev_y)) * 100
                a_growth = f"{a_growth_val:.2f}%"

        price = quote.get('price'); year_high = quote.get('yearHigh')
        is_new_high = "No"
        if price and year_high:
            percent_from_high = ((price - year_high) / year_high) * 100
            if percent_from_high >= -15: is_new_high = f"Yes, within {abs(percent_from_high):.2f}% of 52-week high"

        volume = quote.get('volume'); avg_volume = quote.get('avgVolume')
        is_high_demand = "No"
        if volume and avg_volume and volume > avg_volume:
             is_high_demand = f"Yes, volume is {((volume - avg_volume) / avg_volume) * 100:.2f}% above average"

        i_sponsorship = f"{institutional_holders} institutions"

        prompt = f"""Act as an analyst applying CANSLIM to {company_name}. Based *only* on the data, create a 7-point checklist. Output a 3-column Markdown table: "Criteria", "Assessment", "Result" (Pass/Fail/Neutral). DATA: C={c_growth}, A={a_growth}, N={is_new_high}, S={is_high_demand}, L=Infer leadership, I={i_sponsorship}, M=Infer market direction."""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred in generate_canslim_assessment: {e}")
        return "Could not generate CANSLIM assessment."


def generate_fundamental_conclusion(
    company_name: str,
    piotroski_data: dict,
    graham_data: dict,
    darvas_data: dict,
    key_stats: dict, # <-- NEW: We pass raw stats instead of AI text
    news_headlines: list # <-- NEW: We pass news for sentiment context
):
    """
    Performs a meta-analysis based on Hard Scores and Key Metrics.
    Independent of other AI calls.
    """
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-2.5-flash')

        # 1. Prepare Scores
        p_score = piotroski_data.get('score', 'N/A')
        g_score = graham_data.get('score', 'N/A')
        d_status = darvas_data.get('status', 'N/A')

        # 2. Prepare Key Metrics (Safe Access)
        pe = key_stats.get('peRatio', 'N/A')
        roe = key_stats.get('returnOnCapital', 'N/A') # We mapped this earlier
        if roe == 'N/A': roe = key_stats.get('netIncome', 'N/A') # Fallback
        
        # 3. Prepare News
        news_str = "- " + "\n- ".join(news_headlines[:3]) if news_headlines else "No recent news."

        # 4. The New Master Prompt
        prompt = f"""
        Act as a Senior Portfolio Manager. Analyze {company_name} based on the following quantitative data.
        
        **The Hard Numbers:**
        1. **Financial Health (Piotroski F-Score):** {p_score}/9 (7-9 is strong, 0-3 is weak).
        2. **Value Assessment (Graham Scan):** Passed {g_score}/7 conservative value rules.
        3. **Momentum (Darvas Box):** Current Status: {d_status}.
        4. **Valuation:** P/E Ratio is {pe}.
        
        **Recent News Context:**
        {news_str}

        **Your Task:**
        Synthesize these specific data points into a final investment verdict.
        
        **Strict Output Format:**
        GRADE: [A+, A, B, C, D, or F]
        THESIS: [One clear, professional sentence summarizing the investment case based on the scores.]
        TAKEAWAYS:
        - [Specific point about Financial Health based on F-Score]
        - [Specific point about Valuation/Momentum]
        - [Final verdict point]
        """

        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in fundamental conclusion: {e}")
        return "GRADE: N/A\nTHESIS: Analysis unavailable.\nTAKEAWAYS:\n- System error during analysis."

def find_peer_tickers_by_industry(company_name: str, sector: str, industry: str, country: str):
    """Uses Gemini AI to find a list of top 5 competitor tickers."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""For {company_name} in the "{industry}" industry ({country}), list the top 5 competitor tickers. Return a single, comma-separated list ONLY (e.g., AAPL,MSFT,GOOG). Use .NS for Indian stocks."""
        response = model.generate_content(prompt)
        peers_str = response.text.strip().replace(" ", "").upper()
        return peers_str.split(',')
    except Exception as e:
        print(f"An error occurred while finding peer tickers with AI: {e}")
        return []

def identify_ticker_from_image(image_bytes: bytes):
    """Uses the Gemini Vision model to identify a ticker from a chart image."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-2.5-flash')
        image_part = {"mime_type": "image/jpeg", "data": image_bytes}
        prompt = "Analyze this chart. Return ONLY the Yahoo Finance ticker (e.g., AAPL, RELIANCE.NS). If none, return 'NOT_FOUND'."
        response = model.generate_content([prompt, image_part])
        return response.text.strip().upper()
    except Exception as e:
        print(f"An error occurred during AI ticker identification from image: {e}")
        return "NOT_FOUND"

def analyze_chart_technicals_from_image(image_bytes: bytes):
    """
    Uses Gemini Vision to generate a professional, actionable Trade Setup.
    """
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-2.5-flash')
        image_part = {"mime_type": "image/jpeg", "data": image_bytes}
        
        prompt = """
        Act as a Senior Technical Analyst at a top Hedge Fund. Analyze this chart image.
        Your goal is to identify high-probability trading opportunities.

        Output your analysis in this strict format:

        TREND: [Uptrend / Downtrend / Consolidation]
        TIMEFRAME: [Short-term / Medium-term / Long-term]
        PATTERNS: [List key patterns identified, e.g., Bull Flag, Double Bottom]
        MOMENTUM: [Analyze volume and indicator divergence]
        
        -- TRADE TICKET --
        ACTION: [BUY / SELL / WAIT]
        ENTRY_ZONE: [Specific price range]
        STOP_LOSS: [Specific price]
        TARGET_1: [Conservative target]
        TARGET_2: [Aggressive target]
        RISK_REWARD: [e.g., 1:3]
        CONFIDENCE: [High / Medium / Low]
        RATIONALE: [One sentence explaining the trade logic]
        """
        
        response = model.generate_content([prompt, image_part])
        return response.text.strip()
        
    except Exception as e:
        print(f"AI Analysis Error: {e}")
        return "TREND: Error\nACTION: WAIT\nRATIONALE: Server could not process image."