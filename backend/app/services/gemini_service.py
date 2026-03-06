import os
import google.generativeai as genai
from dotenv import load_dotenv
import itertools

load_dotenv()

# --- ROBUST KEY ROTATION ---
try:
    GEMINI_API_KEYS_STR = os.getenv("GEMINI_API_KEYS")
    if not GEMINI_API_KEYS_STR:
        single_key = os.getenv("GEMINI_API_KEY") 
        if single_key: GEMINI_API_KEYS = [single_key]
        else: GEMINI_API_KEYS = []
    else:
        GEMINI_API_KEYS =[key.strip() for key in GEMINI_API_KEYS_STR.split(',')]
    key_cycler = itertools.cycle(GEMINI_API_KEYS)
except:
    GEMINI_API_KEYS =[]
    key_cycler = None

def configure_gemini_for_request():
    if key_cycler:
        try: genai.configure(api_key=next(key_cycler))
        except: pass

MODEL_NAME = 'gemini-1.5-flash'

# --- VISION AI ---
def identify_ticker_from_image(image_bytes: bytes):
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = """Identify the financial asset in this chart image. Return ONLY the ticker symbol.
        RULES:
        1. Indian Stocks: Return with .NS suffix (e.g. "RELIANCE" -> "RELIANCE.NS").
        2. Indices: Nifty 50 -> "NSEI.INDX", Bank Nifty -> "NSEBANK.INDX", Sensex -> "BSESN.INDX".
        3. US Stocks: Just the ticker (e.g. "AAPL").
        4. Crypto: Add -USD (e.g. "BTC" -> "BTC-USD").
        5. If unsure, return "NOT_FOUND".
        OUTPUT FORMAT: Just the string."""
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_bytes}])
        return response.text.strip().upper().replace("", "").replace(" ", "")
    except Exception as e:
        print(f"Vision Error: {e}")
        return "NOT_FOUND"

def analyze_pure_vision(image_bytes: bytes):
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = "Act as a Quant Analyst. Analyze this chart based purely on geometry. Output VERDICT, MARKET STRUCTURE, GEOMETRIC SIGNALS, and TRADE SETUP."
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_bytes}])
        return response.text.strip()
    except Exception as e:
        return f"**VERDICT:** ERROR\n**ANALYSIS:** {str(e)}"

# --- TEXT GENERATION ---
def get_ticker_from_query(query: str):
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel(MODEL_NAME)
        return model.generate_content(f"Identify stock ticker for: {query}. Return ONLY the ticker (e.g. RELIANCE.NS).").text.strip().replace("", "").upper()
    except: return "ERROR"

def generate_swot_analysis(company_name: str, description: str, news_headlines: list):
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"Generate a SWOT analysis for {company_name}. Output headers: **Strengths**, **Weaknesses**, **Opportunities**, **Threats**."
        return model.generate_content(prompt).text.strip()
    except: return "SWOT Analysis temporarily unavailable."

def generate_forecast_analysis(company_name: str, analyst_ratings: list, price_target: dict, key_stats: dict, news_headlines: list, currency: str = "USD"):
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"Write a 2-paragraph forecast summary for {company_name} using this data: Targets: {price_target}, Currency: {currency}."
        return model.generate_content(prompt).text.strip()
    except: return "Forecast analysis unavailable."

def generate_investment_philosophy_assessment(company_name: str, key_metrics: dict):
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"Analyze {company_name} using Greenblatt, Buffett, and Graham formulas. Metrics: {key_metrics}. Output a Markdown table (Formula | Assessment)."
        return model.generate_content(prompt).text.strip()
    except: return "Philosophy analysis unavailable."

def generate_canslim_assessment(company_name: str, quote: dict, quarterly_earnings: list, annual_earnings: list, institutional_holders: int):
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"Perform a CANSLIM check for {company_name}. Output a Markdown table: Criteria | Assessment | Result (Pass/Fail)."
        return model.generate_content(prompt).text.strip()
    except: return "CANSLIM analysis unavailable."

def generate_fundamental_conclusion(company_name: str, piotroski_data: dict, graham_data: dict, darvas_data: dict, key_stats: dict, news_headlines: list):
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"Act as a Portfolio Manager. Summarize {company_name}. Output format: GRADE: [A/B/C/D/F] \n THESIS: [text] \n TAKEAWAYS: [bullets]."
        return model.generate_content(prompt).text.strip()
    except: return "Conclusion unavailable."

def find_peer_tickers_by_industry(company_name: str, sector: str, industry: str, country: str):
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = f"List 5 major competitor tickers for {company_name} ({industry}, {country}). Comma separated only. Example: RELIANCE.NS, TCS.NS"
        return model.generate_content(prompt).text.strip()
    except: return ""

def generate_timeframe_analysis(symbol, timeframe, technicals, pivots, mas):
    return "Please use the local Quant Engine for technical analysis."
