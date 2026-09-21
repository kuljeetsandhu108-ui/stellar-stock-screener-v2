import os
import requests
import threading
from dotenv import load_dotenv

load_dotenv()

class CryptoDatabase:
    """
    The 'Helping Hand' Shadow Registry (FMP Edition).
    Downloads all FMP cryptos into RAM to ensure 100% 1-to-1 data mapping.
    """
    def __init__(self):
        self.coins = set(["BTC", "ETH", "SOL", "XRP", "DOGE", "ADA", "MATIC", "BNB", "AVAX", "DOT", "LTC", "SHIB", "PEPE", "LINK", "UNI"])
        self.total_loaded = len(self.coins)
        
        thread = threading.Thread(target=self._fetch_data)
        thread.daemon = True
        thread.start()

    def _fetch_data(self):
        key = os.getenv("FMP_API_KEY")
        if not key:
            return
            
        try:
            url = f"https://financialmodelingprep.com/api/v3/symbol/available-cryptocurrencies?apikey={key}"
            res = requests.get(url, timeout=15)
            
            if res.status_code == 200:
                data = res.json()
                new_coins = set()
                
                # Extract FMP base tickers (e.g. 'BTC' from 'BTCUSD')
                for c in data:
                    sym = c.get('symbol', '')
                    if sym.endswith('USD'):
                        new_coins.add(sym.replace('USD', ''))
                        
                if new_coins:
                    self.coins = new_coins
                    self.total_loaded = len(self.coins)
                    print(f"🚀 [CRYPTO REGISTRY] Successfully synced {self.total_loaded} live FMP crypto assets into memory.")
        except Exception as e:
            print(f"⚠️[CRYPTO REGISTRY] Sync failed. Using default cache. Error: {e}")

    def is_crypto(self, symbol: str) -> bool:
        return symbol.upper() in self.coins

crypto_db = CryptoDatabase()
