import os
import requests
from dotenv import load_dotenv

load_dotenv("backend/.env")

EODHD_KEY = os.getenv("EODHD_API_KEY")
FMP_KEY = os.getenv("FMP_API_KEY")

print("\n" + "="*60)
print("🔍 DUAL API CRYPTO DATABASE SCANNER")
print("="*60)

# --- 1. EODHD SCAN ---
print("\n📡 Fetching EODHD Crypto List...")
eodhd_usd =[]
try:
    eodhd_url = f"https://eodhd.com/api/exchange-symbol-list/CC?api_token={EODHD_KEY}&fmt=json"
    res = requests.get(eodhd_url, timeout=10).json()
    eodhd_usd = [c['Code'].replace('-USD', '') for c in res if c.get('Code', '').endswith('-USD')]
    print(f"✅ EODHD Total USD Cryptos: {len(eodhd_usd)}")
except Exception as e:
    print(f"❌ EODHD Error: {e}")

# --- 2. FMP SCAN ---
print("\n📡 Fetching FMP (FinancialModelingPrep) Crypto List...")
fmp_usd =[]
try:
    fmp_url = f"https://financialmodelingprep.com/api/v3/symbol/available-cryptocurrencies?apikey={FMP_KEY}"
    res = requests.get(fmp_url, timeout=10).json()
    fmp_usd = [c['symbol'].replace('USD', '') for c in res if c.get('symbol', '').endswith('USD')]
    print(f"✅ FMP Total USD Cryptos: {len(fmp_usd)}")
except Exception as e:
    print(f"❌ FMP Error: {e}")

# --- 3. COMPARISON ---
print("\n⚖️ --- DATABASE COMPARISON ---")
common = set(eodhd_usd).intersection(set(fmp_usd))
print(f"🔗 Cryptos present in BOTH APIs: {len(common)}")

fmp_only = set(fmp_usd) - set(eodhd_usd)
print(f"💎 Cryptos ONLY in FMP: {len(fmp_only)} (e.g. {list(fmp_only)[:5]})")

print("\n" + "="*60)
print("✅ DEBUG COMPLETE. The backend is being routed to use FMP strictly for perfect mapping!")
