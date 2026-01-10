import os
import google.generativeai as genai
from dotenv import load_dotenv
import itertools

load_dotenv()

# --- 1. API KEY ROTATOR (CRITICAL FOR STABILITY) ---
try:
    GEMINI_API_KEYS_STR = os.getenv("GEMINI_API_KEYS")
    if not GEMINI_API_KEYS_STR:
        # Fallback to single key if list is not found
        single_key = os.getenv("GEMINI_API_KEY") 
        if single_key:
            GEMINI_API_KEYS = [single_key]
        else:
            raise ValueError("GEMINI_API_KEYS not found in .env file.")
    else:
        # Clean and split the keys
        GEMINI_API_KEYS = [key.strip() for key in GEMINI_API_KEYS_STR.split(',')]
    
    # Create a cycle iterator that loops forever
    key_cycler = itertools.cycle(GEMINI_API_KEYS)
    print(f"Successfully loaded and initialized rotator for {len(GEMINI_API_KEYS)} Gemini API keys.")

except Exception as e:
    print(f"CRITICAL ERROR: Could not load Gemini API keys. AI features will fail. Error: {e}")
    GEMINI_API_KEYS = []
    key_cycler = None

def configure_gemini_for_request():
    """Configures the genai library with the next available key from the pool."""
    if not key_cycler:
        raise ValueError("No Gemini API keys are configured or available.")
    
    # Rotate to the next key
    api_key = next(key_cycler)
    genai.configure(api_key=api_key)


# --- 2. TEXT ANALYSIS FUNCTIONS ---

def get_ticker_from_query(query: str):
    """Identifies the stock ticker from a natural language query."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        prompt = f"""Analyze the following user query: "{query}". Return ONLY the official stock ticker symbol (e.g., "AAPL" for Apple, "RELIANCE.NS" for Reliance Industries). If a clear ticker cannot be found, return the text "NOT_FOUND"."""
        response = model.generate_content(prompt)
        return response.text.strip().replace("`", "").upper()
    except Exception as e:
        print(f"Error in get_ticker_from_query: {e}")
        return "ERROR"

def generate_swot_analysis(company_name: str, description: str, news_headlines: list):
    """Generates a SWOT analysis."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        news_string = "\n- ".join(news_headlines)
        prompt = f"""Generate a 4-section SWOT analysis for {company_name}. Use the following data for context. Structure the output with clear headers for Strengths, Weaknesses, Opportunities, and Threats, each followed by bullet points.\n\n**Company Description:**\n{description}\n\n**Recent News Headlines:**\n- {news_string}"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in generate_swot_analysis: {e}")
        return "Could not generate SWOT analysis."

def generate_forecast_analysis(company_name: str, analyst_ratings: list, price_target: dict, key_stats: dict, news_headlines: list, currency: str = "USD"):
    """Generates a summary of analyst forecasts with correct currency."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        ratings_summary = "\n".join([f"- {r.get('ratingStrongBuy', 0)} Strong Buy, {r.get('ratingBuy', 0)} Buy, {r.get('ratingHold', 0)} Hold, {r.get('ratingSell', 0)} Sell, {r.get('ratingStrongSell', 0)} Strong Sell" for r in analyst_ratings[:1]])
        news_string = "\n- ".join(news_headlines)
        
        # Determine symbol for prompt context
        curr_symbol = "₹" if currency == "INR" else "$" if currency == "USD" else currency

        prompt = f"""Act as a professional financial analyst. For {company_name} (Currency: {currency}), write a two-paragraph summary of the analyst forecast.
        
        **Instructions:**
        - STRICTLY use the currency symbol '{curr_symbol}' for ALL monetary values.
        - Do not use '$' if the currency is INR.
        
        **Data:**
        - **Analyst Ratings:** {ratings_summary}
        - **Price Target:** High {curr_symbol}{price_target.get('targetHigh')}, Average {curr_symbol}{price_target.get('targetConsensus')}, Low {curr_symbol}{price_target.get('targetLow')}
        - **Recent News:**\n- {news_string}"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in generate_forecast_analysis: {e}")
        return "Could not generate AI forecast analysis."

def generate_investment_philosophy_assessment(company_name: str, key_metrics: dict):
    """
    Generates assessment. 
    HYBRID MODE: Tries AI first. If AI fails (429/Quota), falls back to Algorithmic Logic.
    """
    # 1. Prepare Data Safe Variables
    pe = key_metrics.get('peRatioTTM')
    ey = key_metrics.get('earningsYieldTTM')
    roc = key_metrics.get('returnOnCapitalEmployedTTM')
    
    # Numeric values for math (Default to 0)
    pe_val = float(pe) if pe is not None else 0.0
    ey_val = float(ey) if ey is not None else 0.0
    roc_val = float(roc) if roc is not None else 0.0
    
    # String formatting for display
    pe_str = f"{pe_val:.2f}" if pe is not None else "N/A"
    ey_str = f"{ey_val:.2%}" if ey is not None else "N/A"
    roc_str = f"{roc_val:.2%}" if roc is not None else "N/A"

    try:
        # --- PLAN A: ASK AI ---
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        data_summary = (
            f"- Price to Earnings (P/E): {pe_str}\n"
            f"- Earnings Yield (Greenblatt): {ey_str}\n"
            f"- Return on Capital (ROC/ROE): {roc_str}"
        )
        
        prompt = f"""
        Act as a Value Investor. Analyze {company_name} based on:
        {data_summary}
        
        Evaluate against:
        1. Greenblatt's Magic Formula (High Yield + High ROC)
        2. Warren Buffett's Moat (High ROC)
        3. Ben Graham Value (Low P/E)
        
        Output a 2-column Markdown table with headers "Formula" and "Assessment".
        Assessment should be 1 short sentence.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print(f"Gemini 429/Error (Philosophy): {e}")
        
        # --- PLAN B: ALGORITHMIC FALLBACK (The Crash Fix) ---
        # We calculate the verdict manually so the user NEVER sees an error text.
        
        # 1. Magic Formula Logic
        if ey_val > 0.05 and roc_val > 0.15:
            magic_text = f"**Pass**. Attractive Yield ({ey_str}) and High Efficiency ({roc_str})."
        else:
            magic_text = f"**Fail**. Requires Earnings Yield > 5% and ROC > 15%."
            
        # 2. Buffett Moat Logic
        if roc_val > 0.15:
            buffett_text = f"**Wide Moat**. Consistent high ROC ({roc_str}) suggests competitive advantage."
        elif roc_val > 0.10:
            buffett_text = "**Narrow Moat**. Decent returns, but not exceptional."
        else:
            buffett_text = "**No Moat**. Low capital efficiency ({roc_str})."
            
        # 3. Graham Value Logic
        if pe_val > 0 and pe_val < 15:
            graham_text = f"**Undervalued**. P/E of {pe_str} is below defensive target of 15."
        elif pe_val < 25:
            graham_text = f"**Fair Value**. P/E of {pe_str} is reasonable."
        else:
            graham_text = f"**Expensive**. P/E of {pe_str} implies high growth expectations."

        # Return a perfectly formatted Markdown table that the Frontend can read
        return f"""
| Formula | Assessment |
|---|---|
| **Greenblatt Magic Formula** | {magic_text} |
| **Buffett Moat Indicator** | {buffett_text} |
| **Ben Graham Valuation** | {graham_text} |
| *System Status* | *AI Quota Limit. Showing smart algorithmic analysis.* |
"""       

def generate_canslim_assessment(company_name: str, quote: dict, quarterly_earnings: list, annual_earnings: list, institutional_holders: int):
    """Generates a CANSLIM checklist."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        c_growth, a_growth, is_new_high, is_high_demand = "N/A", "N/A", "No", "No"
        if len(quarterly_earnings) > 4:
            latest_q_eps = quarterly_earnings[0].get('eps', 0)
            previous_q_eps = quarterly_earnings[4].get('eps', 0)
            if previous_q_eps not in [0, None]: c_growth = f"{((latest_q_eps - previous_q_eps) / abs(previous_q_eps)) * 100:.2f}% (YoY)"
        if len(annual_earnings) >= 2:
            latest_y_eps = annual_earnings[0].get('eps', 0)
            previous_y_eps = annual_earnings[1].get('eps', 0)
            if previous_y_eps not in [0, None]: a_growth = f"{((latest_y_eps - previous_y_eps) / abs(previous_y_eps)) * 100:.2f}%"
        price = quote.get('price'); year_high = quote.get('yearHigh')
        if price and year_high:
            percent_from_high = ((price - year_high) / year_high) * 100
            if percent_from_high >= -15: is_new_high = f"Yes, within {abs(percent_from_high):.2f}% of 52-week high"
        volume = quote.get('volume'); avg_volume = quote.get('avgVolume')
        if volume and avg_volume and volume > avg_volume:
            is_high_demand = f"Yes, volume is {((volume - avg_volume) / avg_volume) * 100:.2f}% above average"
        i_sponsorship = f"{institutional_holders} institutions hold this stock."

        prompt = f"""Act as an analyst applying CANSLIM to {company_name}. Based *only* on the data, create a 7-point checklist. Output a 3-column Markdown table: "Criteria", "Assessment", "Result" (Pass/Fail/Neutral). DATA: C={c_growth}, A={a_growth}, N={is_new_high}, S={is_high_demand}, L=Infer leadership, I={i_sponsorship}, M=Infer market direction."""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in generate_canslim_assessment: {e}")
        return "Could not generate CANSLIM assessment."

def generate_fundamental_conclusion(company_name: str, piotroski_data: dict, graham_data: dict, darvas_data: dict, key_stats: dict, news_headlines: list):
    """Performs a meta-analysis summary."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        p_score = piotroski_data.get('score', 'N/A') if piotroski_data else 'N/A'
        g_score = graham_data.get('score', 'N/A') if graham_data else 'N/A'
        d_status = darvas_data.get('status', 'N/A') if darvas_data else 'N/A'
        pe = key_stats.get('peRatio', 'N/A')
        
        news_str = "- " + "\n- ".join(news_headlines[:3]) if news_headlines else "No recent news."

        prompt = f"""Act as a Senior Portfolio Manager. Analyze {company_name}.
        **Hard Numbers:** Piotroski: {p_score}/9, Graham Scan: {g_score}/7, Darvas Status: {d_status}, P/E: {pe}.
        **News Context:** {news_str}
        Synthesize into: GRADE: [A-F], THESIS: [Sentence], TAKEAWAYS: [3 bullets]."""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in fundamental conclusion: {e}")
        return "GRADE: N/A\nTHESIS: Analysis unavailable."

def find_peer_tickers_by_industry(company_name: str, sector: str, industry: str, country: str):
    """Uses Gemini AI to find competitor tickers."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        prompt = f"""Act as an expert financial data analyst. The company is {company_name}, in the "{industry}" industry within the "{sector}" sector in {country}. Identify top 5 publicly traded competitors. Return comma-separated tickers ONLY. US: AAPL, MSFT. India: RELIANCE.NS, TCS.NS."""
        response = model.generate_content(prompt)
        peers_str = response.text.strip().replace(" ", "").upper()
        return peers_str.split(',')
    except Exception as e:
        print(f"Error finding peers: {e}")
        return []


# --- 3. CHART AI (IMAGE) ANALYSIS (OPTIMIZED) ---

def identify_ticker_from_image(image_bytes: bytes):
    """Identifies ticker from chart image, supports Stocks & Indices."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        prompt = """
        Analyze this financial chart image. Identify the symbol/ticker.
        
        RULES:
        1. If it's a specific company, return the Yahoo symbol (e.g., "RELIANCE.NS", "AAPL").
        2. If it's an INDEX, map it correctly:
           - Nifty 50 -> "^NSEI"
           - Bank Nifty -> "^NSEBANK"
           - Sensex -> "^BSESN"
           - S&P 500 -> "^GSPC"
           - Nasdaq -> "^IXIC"
           - Bitcoin -> "BTC-USD"
           - Gold -> "GC=F"
        3. If you are not 100% sure, return "NOT_FOUND".
        4. Return ONLY the symbol string. No text.
        """
        
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_bytes}])
        return response.text.strip().upper().replace("`", "")
    except Exception as e:
        print(f"Error identifying ticker: {e}")
        return "NOT_FOUND"


def analyze_chart_technicals_from_image(image_bytes: bytes):
    """
    Uses Gemini Vision to analyze chart images.
    Updated with STRICT PROMPTS to prevent verbose output in the Trade Ticket.
    """
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        image_part = {"mime_type": "image/jpeg", "data": image_bytes}
        
        prompt = """
        Act as an expert Chartered Market Technician. Analyze this stock chart image.
        Provide a professional technical analysis and a precision trade setup.

        STRICT RESPONSE FORMAT (Do not deviate):

        TREND: [Uptrend / Downtrend / Sideways]
        PATTERNS: [List key patterns like Head & Shoulders, Flags, or "None"]
        LEVELS: [List key Support and Resistance price levels]
        VOLUME: [Describe volume behavior: "High volume breakout", "Low volume pullback", etc.]
        INDICATORS: [Mention visible indicators like MA, RSI, MACD]
        CONCLUSION: [A professional 2-sentence summary]
        
        -- TRADE TICKET --
        ACTION: [BUY / SELL / WAIT]
        ENTRY_ZONE: [Price range ONLY. e.g., "150.00 - 152.50"]
        STOP_LOSS: [Price ONLY. e.g., "145.00"]
        TARGET_1: [Price ONLY. e.g., "160.00"]
        TARGET_2: [Price ONLY. e.g., "165.00"]
        RISK_REWARD: [Ratio. e.g., "1:3"]
        CONFIDENCE: [High / Medium / Low]
        RATIONALE: [One clear sentence explaining the strategy.]
        """
        
        response = model.generate_content([prompt, image_part])
        return response.text.strip()
        
    except Exception as e:
        print(f"AI Image Analysis Error: {e}")
        return "TREND: Error\nACTION: WAIT\nRATIONALE: Server could not process image."


# --- 4. CHART AI (TIMEFRAME) ANALYSIS (SAFE MATH & STRICT FORMAT) ---

def generate_timeframe_analysis(symbol: str, timeframe: str, technical_data: dict, pivots: dict, moving_averages: dict):
    """
    Generates a trade setup based on live calculated data.
    """
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')

        # Safe extraction of data with defaults
        rsi = technical_data.get('rsi', 'N/A')
        macd = technical_data.get('macd', 'N/A')
        stoch = technical_data.get('stochasticsk', 'N/A')
        adx = technical_data.get('adx', 'N/A')
        close = technical_data.get('price_action', {}).get('current_close', 'N/A')

        classic = pivots.get('classic', {})
        pivot_str = f"PP:{classic.get('pp', 'N/A')}, S1:{classic.get('s1', 'N/A')}, R1:{classic.get('r1', 'N/A')}"
        ma_str = f"SMA20:{moving_averages.get('20', 'N/A')}, SMA50:{moving_averages.get('50', 'N/A')}"

        # --- SAFETY BLOCK: PREVENT CRASHES ON MISSING PRICE ---
        try:
            # We try to calculate examples to guide the AI
            val = float(close)
            ex_entry = f"{val} - {val*1.002:.2f}"
            ex_stop = f"{val*0.99:.2f}"
            ex_tgt1 = f"{val*1.01:.2f}"
            ex_tgt2 = f"{val*1.02:.2f}"
        except:
            # Fallback values if price is 'N/A' or invalid
            ex_entry = "100.00 - 101.00"
            ex_stop = "99.00"
            ex_tgt1 = "102.00"
            ex_tgt2 = "103.00"

        # --- OPTIMIZED PROMPT ---
        prompt = f"""
        Act as an Algorithmic Trader. Analyze the following live technical data for {symbol} on the {timeframe} timeframe.
        
        **Live Data:**
        - Price: {close}
        - Momentum: RSI({rsi}), Stoch({stoch}), ADX({adx}), MACD({macd})
        - Levels: {pivot_str}
        - Trends: {ma_str}

        **Instructions:**
        1. Identify the Trend and Momentum.
        2. Define a Trade Setup based on Pivot Points and Moving Averages.
        3. KEEP THE TRADE TICKET VALUES CONCISE (Numbers Only). Do not write sentences in price fields.

        **STRICT OUTPUT FORMAT:**
        TREND: [Uptrend / Downtrend / Range]
        PATTERNS: [Name of formation e.g. "Bull Flag" or "Consolidation"]
        MOMENTUM: [Bullish / Bearish / Neutral]
        LEVELS: [Key Support/Resistance levels]
        INDICATORS: [Brief summary of indicator signals]
        CONCLUSION: [Brief professional summary]

        -- TRADE TICKET --
        ACTION: [BUY / SELL / WAIT]
        ENTRY_ZONE: [Price range ONLY. e.g., "{ex_entry}"]
        STOP_LOSS: [Price ONLY. e.g., "{ex_stop}"]
        TARGET_1: [Price ONLY. e.g., "{ex_tgt1}"]
        TARGET_2: [Price ONLY. e.g., "{ex_tgt2}"]
        RISK_REWARD: [Ratio. e.g., "1:2"]
        CONFIDENCE: [High / Medium / Low]
        RATIONALE: [One clear sentence explaining the trade logic.]
        """

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print(f"Error in timeframe analysis: {e}")
        # Return a soft error that the frontend can detect without crashing
        return "TREND: Error\nACTION: WAIT\nRATIONALE: AI Analysis Failed."