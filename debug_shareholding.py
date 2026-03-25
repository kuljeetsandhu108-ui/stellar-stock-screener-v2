import os
import requests
import json
from dotenv import load_dotenv

# Load Env from Backend folder
load_dotenv("backend/.env")

KEY = os.getenv("EODHD_API_KEY")
SYMBOL = "RELIANCE.NSE"

print("\n" + "="*50)
print(f"🔍 EODHD RAW SHAREHOLDING DEBUGGER")
print("="*50)

if not KEY:
    print("❌ ERROR: EODHD_API_KEY is missing in backend/.env")
    exit()

url = f"https://eodhd.com/api/fundamentals/{SYMBOL}?api_token={KEY}&fmt=json"
print(f"📡 Fetching raw payload for {SYMBOL} (This may take a few seconds)...\n")

try:
    response = requests.get(url, timeout=15)
    if response.status_code != 200:
        print(f"❌ API ERROR: Status {response.status_code}")
        exit()
        
    data = response.json()
    
    print("📊 --- 1. SHARES STATS ---")
    print(json.dumps(data.get("SharesStats", {}), indent=4))
    
    print("\n🏢 --- 2. HOLDERS DATA (Keys Available) ---")
    holders = data.get("Holders", {})
    for category, records in holders.items():
        print(f" -> {category}: {len(records)} records found.")
        if records and isinstance(records, dict):
            first_item = list(records.values())[0]
            print(f"    Sample Keys: {list(first_item.keys())}")
            
    print("\n👔 --- 3. INSIDER TRANSACTIONS ---")
    insiders = data.get("InsiderTransactions", {})
    if insiders:
        print(f" -> Found {len(insiders)} insider transaction records.")
        first_key = list(insiders.keys())[0]
        print(f"    Sample Keys: {list(insiders[first_key].keys())}")
    else:
        print(" -> No Insider Transactions found.")
        
    print("\n" + "="*50)
    print("✅ DEBUG COMPLETE. Paste this terminal output back to me!")

except Exception as e:
    print(f"❌ CONNECTION FAILED: {e}")
