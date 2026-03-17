import requests
from bs4 import BeautifulSoup

# --- CENTRALIZED SCREENER REGISTRY ---
SCREENERS = {
    "bullish_reversal": {
        "id": "bullish_reversal",
        "name": "Bullish Reversal",
        "description": "RSI Crossover + Stochastic Momentum + Volume Expansion",
        "url": "https://chartink.com/screener/copy-bullish-reversal-538",
        "scan_clause": "( {cash} (  daily slow stochastic %d( 14,3 ) <=  70 and  daily slow stochastic %k( 14,3 ) >  daily slow stochastic %d( 14,3 ) and  daily rsi( 14 ) >  1 day ago rsi( 14 ) and  1 day ago  rsi( 14 ) <=  2 day ago  rsi( 14 ) and  daily rsi( 14 ) <=  80 and  daily volume >  150000 and  daily slow stochastic %k( 14,3 ) >  1 day ago slow stochastic %k( 14,3 ) and  1 day ago slow stochastic %k( 14,3 ) <  2 days ago slow stochastic %k( 14,3 ) and  daily close >=  10 and  2 days ago slow stochastic %k( 14,3 ) <  3 days ago slow stochastic %k( 14,3 ) ) )"
    },
    "momentum_vidya": {
        "id": "momentum_vidya",
        "name": "Momentum Swing",
        "description": "Futures Segment: High momentum stocks surging from recent swing lows.",
        "url": "https://chartink.com/screener/momentum-stocks-vidya",
        "scan_clause": "( {33489} (  daily close >  30 and  daily sma(  daily volume , 50 ) >=  50000 and( {cash} (  daily close >=  5 days ago low *  1.2 or  daily close >=  30 days ago low *  1.3 or  daily close >=  90 days ago low *  1.3 ) ) ) )"
    },
    "longterm_value": {
        "id": "longterm_value",
        "name": "Longterm Value Buy",
        "description": "Nifty 200: High liquidity stocks with stabilizing RSI and trading above 50 SMA.",
        "url": "https://chartink.com/screener/longterm-value-buy",
        "scan_clause": "( {46553} (  daily close *  daily volume >  10000000 and  1 month ago rsi( 14 ) >  54 and  1 month ago rsi( 14 ) <  59 and  daily close >  daily sma( close,50 ) and  2 months ago rsi( 14 ) <  55 ) )"
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
                data = res.json().get('data', [])
                return data[:20] # Top 20 results for UI performance
                
        return[]
    except Exception as e:
        print(f"⚠️ Chartink Engine Error [{screener_key}]: {e}")
        return[]

def get_all_screener_configs():
    """Returns metadata for the React UI Tabs"""
    return [{"key": k, "name": v["name"], "description": v["description"]} for k, v in SCREENERS.items()]
