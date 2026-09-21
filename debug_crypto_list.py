import os
import requests
from dotenv import load_dotenv

# Load Env from Backend folder
load_dotenv("backend/.env")

KEY = os.getenv("EODHD_API_KEY")

print("\n" + "="*60)
print("🔍 EODHD RAW CRYPTO DATABASE SCANNER")
print("="*60)

if not KEY:
    print("❌ ERROR: EODHD_API_KEY is missing in backend/.env")
    exit()

# Fetch all symbols for the Crypto (CC) exchange
url = f"https://eodhd.com/api/exchange-symbol-list/CC?api_token={KEY}&fmt=json"
print("📡 Fetching Crypto database from EODHD (This may take a few seconds)...\n")

try:
    response = requests.get(url, timeout=20)
    if response.status_code != 200:
        print(f"❌ API ERROR: Status {response.status_code}")
        exit()
        
    data = response.json()
    print(f"✅ TOTAL Crypto Pairs available in EODHD: {len(data)}")
    
    # Filter to only show coins trading against the US Dollar (-USD) for clarity
    usd_coins =[coin for coin in data if isinstance(coin, dict) and coin.get('Code', '').endswith('-USD')]
    print(f"✅ TOTAL USD-Quoted Coins available: {len(usd_coins)}\n")
    
    print("🪙 --- TOP 50 USD CRYPTO COINS ---")
    # Print the first 50 to avoid crashing your terminal buffer
    for i, coin in enumerate(usd_coins[:50]):
        code = coin.get('Code', 'N/A')
        name = coin.get('Name', 'N/A')
        print(f"   {i+1:02d} | Ticker: {code:<15} | Name: {name}")
        
    print("\n" + "="*60)
    print("✅ DEBUG COMPLETE. Please paste this terminal output back to me!")

except Exception as e:
    print(f"❌ CONNECTION FAILED: {e}")
