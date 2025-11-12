import os
import google.generativeai as genai
from dotenv import load_dotenv
import itertools

load_dotenv()

# --- THE API KEY ROTATOR ---
# This block initializes our load balancing system for the Gemini API.
try:
    # 1. Read the comma-separated string of keys from the .env file.
    GEMINI_API_KEYS_STR = os.getenv("GEMINI_API_KEYS")
    if not GEMINI_API_KEYS_STR:
        raise ValueError("GEMINI_API_KEYS not found in .env file. Please add it as a comma-separated list.")
    
    # 2. Split the string into a clean list of individual keys.
    GEMINI_API_KEYS = [key.strip() for key in GEMINI_API_KEYS_STR.split(',')]
    
    # 3. Create an infinitely looping iterator that cycles through our list of keys.
    # This is the core of the load balancer.
    key_cycler = itertools.cycle(GEMINI_API_KEYS)
    print(f"Successfully loaded and initialized rotator for {len(GEMINI_API_KEYS)} Gemini API keys.")

except (ValueError, AttributeError) as e:
    print(f"CRITICAL ERROR: Could not load Gemini API keys. AI features will fail. Error: {e}")
    GEMINI_API_KEYS = []
    key_cycler = None

def configure_gemini_for_request():
    """
    This function is called before every API request. It takes the next key
    from the pool and configures the genai library with it.
    """
    if not key_cycler:
        raise ValueError("No Gemini API keys are configured or available.")
    
    api_key = next(key_cycler)
    # print(f"Using API Key ending in: ...{api_key[-4:]}") # Optional: Uncomment for deep debugging
    genai.configure(api_key=api_key)


# --- All functions below are now wrapped to use the rotator ---

def get_ticker_from_query(query: str):
    """Uses the Gemini model with a rotated API key to find a stock ticker."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"""Analyze the following user query: "{query}". Return ONLY the official stock ticker symbol (e.g., "AAPL", "RELIANCE.NS"). If none is found, return "NOT_FOUND"."""
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
        news_string = "\n- ".join(news_headlines)
        prompt = f"""Generate a 4-section SWOT analysis for {company_name} based on this data:\nDescription: {description}\nRecent News:\n- {news_string}"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred in generate_swot_analysis: {e}")
        return "Could not generate SWOT analysis."

def generate_forecast_analysis(company_name: str, analyst_ratings: list, price_target: dict, key_stats: dict, news_headlines: list):
    """Generates a forecast analysis with a rotated API key."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-2.5-flash')
        ratings_summary = "\n".join([f"- {r.get('ratingStrongBuy', 0)} Strong Buy, {r.get('ratingBuy', 0)} Buy, {r.get('ratingHold', 0)} Hold" for r in analyst_ratings[:1]])
        news_string = "\n- ".join(news_headlines)
        prompt = f"""Act as a financial analyst. For {company_name}, write a two-paragraph summary of the analyst forecast based on this data:\n- Ratings: {ratings_summary}\n- Price Target: High ${price_target.get('targetHigh')}, Avg ${price_target.get('targetConsensus')}\n- Recent News:\n- {news_string}"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred in generate_forecast_analysis: {e}")
        return "Could not generate AI forecast analysis."

def generate_investment_philosophy_assessment(company_name: str, key_metrics: dict):
    """Generates a philosophy assessment with a rotated API key."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-2.5-flash')
        pe_ratio = key_metrics.get('peRatioTTM')
        earnings_yield = key_metrics.get('earningsYieldTTM')
        roc = key_metrics.get('returnOnCapitalEmployedTTM')
        if pe_ratio is None or earnings_yield is None or roc is None:
            return "Could not generate assessment due to missing P/E, ROC, or Earnings Yield."
        data_summary = f"- P/E Ratio: {pe_ratio:.2f}\n- Earnings Yield: {earnings_yield:.4f}\n- ROC: {roc:.4f}"
        prompt = f"""Act as an analyst. For {company_name}, assess it against 3 philosophies (Magic Formula, Buffett, Coffee Can) based on these metrics:\n{data_summary}\nOutput a clean, 2-column Markdown table: "Formula", "Assessment", incorporating the values naturally."""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred in generate_investment_philosophy_assessment: {e}")
        return "Could not generate AI assessment."

def generate_canslim_assessment(company_name: str, quote: dict, quarterly_earnings: list, annual_earnings: list, institutional_holders: int):
    """Generates a CANSLIM assessment with a rotated API key."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        c_growth, a_growth, is_new_high, is_high_demand = "N/A", "N/A", "No", "No"
        if len(quarterly_earnings) > 4:
            latest_q_eps = quarterly_earnings[0].get('eps', 0)
            previous_q_eps = quarterly_earnings[4].get('eps', 0)
            if previous_q_eps not in [0, None]:
                c_growth_val = ((latest_q_eps - previous_q_eps) / abs(previous_q_eps)) * 100
                c_growth = f"{c_growth_val:.2f}% (YoY)"
        if len(annual_earnings) >= 2:
            latest_y_eps = annual_earnings[0].get('eps', 0)
            previous_y_eps = annual_earnings[1].get('eps', 0)
            if previous_y_eps not in [0, None]:
                a_growth_val = ((latest_y_eps - previous_y_eps) / abs(previous_y_eps)) * 100
                a_growth = f"{a_growth_val:.2f}%"
        price, year_high = quote.get('price'), quote.get('yearHigh')
        if price and year_high:
            percent_from_high = ((price - year_high) / year_high) * 100
            if percent_from_high >= -15:
                is_new_high = f"Yes, within {abs(percent_from_high):.2f}% of 52-week high"
        volume, avg_volume = quote.get('volume'), quote.get('avgVolume')
        if volume and avg_volume and volume > avg_volume:
            volume_increase = ((volume - avg_volume) / avg_volume) * 100
            is_high_demand = f"Yes, volume is {volume_increase:.2f}% above average"
        i_sponsorship = f"{institutional_holders} institutions hold this stock."

        prompt = f"""Act as an analyst applying CANSLIM to {company_name}. Based *only* on the data, create a 7-point checklist. Output a 3-column Markdown table: "Criteria", "Assessment", "Result" (Pass/Fail/Neutral). DATA: C={c_growth}, A={a_growth}, N={is_new_high}, S={is_high_demand}, L=Infer leadership, I={i_sponsorship}, M=Infer market direction."""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"An error occurred in generate_canslim_assessment: {e}")
        return "Could not generate CANSLIM assessment."