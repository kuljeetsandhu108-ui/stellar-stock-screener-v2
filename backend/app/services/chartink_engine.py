import requests
from bs4 import BeautifulSoup
import asyncio

# --- CENTRALIZED SCREENER REGISTRY ---
# We will add Screener #2 and #3 here shortly.
SCREENERS = {
    "bullish_reversal": {
        "id": "bullish_reversal",
        "name": "Bullish Reversal",
        "description": "RSI Crossover + Stochastic Momentum + Volume Expansion",
        "url": "https://chartink.com/screener/copy-bullish-reversal-538",
        "scan_clause": "( {cash} ( Daily Slow Stochastic %D( 14,3 ) <= 70 and Daily Slow Stochastic %K( 14,3 ) > Daily Slow Stochastic %D( 14,3 ) and Daily Rsi( 14 ) crossed above 1 day ago Rsi( 14 ) and Daily Rsi( 14 ) <= 80 and Daily Volume > 150000 and Daily Slow Stochastic %K( 14,3 ) > 1 day ago Slow Stochastic %K( 14,3 ) and 1 day ago Slow Stochastic %K( 14,3 ) < 2 days ago Slow Stochastic %K( 14,3 ) and Daily Close >= 10 and 2 days ago Slow Stochastic %K( 14,3 ) < 3 days ago Slow Stochastic %K( 14,3 ) ) )"
    }
}

def fetch_screener(screener_key: str):
    """Stealth Scraping Engine: Mimics Chrome & Bypasses CSRF"""
    config = SCREENERS.get(screener_key)
    if not config: return[]
    
    try:
        with requests.Session() as s:
            # 1. Stealth Headers
            s.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            })
            
            # 2. Extract specific CSRF token from the exact URL
            r = s.get(config['url'], timeout=10)
            soup = BeautifulSoup(r.text, 'html.parser')
            meta = soup.select_one('meta[name="csrf-token"]')
            
            if not meta: return[]
                
            # 3. Post Payload with AJAX Headers
            s.headers.update({
                'X-CSRF-TOKEN': meta['content'],
                'X-Requested-With': 'XMLHttpRequest',
                'Origin': 'https://chartink.com',
                'Referer': config['url']
            })
            
            res = s.post('https://chartink.com/screener/process', data={'scan_clause': config['scan_clause']}, timeout=10)
            
            if res.status_code == 200:
                data = res.json().get('data',[])
                return data[:20] # Top 20 results for UI performance
                
        return[]
    except Exception as e:
        print(f"⚠️ Chartink Engine Error [{screener_key}]: {e}")
        return[]

def get_all_screener_configs():
    """Returns metadata for the React UI Tabs"""
    return [{"key": k, "name": v["name"], "description": v["description"]} for k, v in SCREENERS.items()]
