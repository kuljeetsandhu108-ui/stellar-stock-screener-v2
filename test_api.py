import os
import requests
from dotenv import load_dotenv

# Load Env from Backend folder
load_dotenv("backend/.env")

KEY = os.getenv("EODHD_API_KEY")
SYMBOL = "RELIANCE.NSE" # EODHD format

print("-" * 30)
print("🔍 DIAGNOSTIC TEST")
print("-" * 30)

if not KEY:
    print("❌ ERROR: EODHD_API_KEY is missing or empty.")
    print("👉 Make sure 'backend/.env' exists and has EODHD_API_KEY=your_key")
else:
    print(f"✅ Key Found: {KEY[:5]}...{KEY[-4:]}")
    
    print(f"📡 Testing Connection for {SYMBOL}...")
    url = f"https://eodhd.com/api/real-time/{SYMBOL}?api_token={KEY}&fmt=json"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS! EODHD Response:")
            print(f"   Price: {data.get('close')}")
            print(f"   Code:  {data.get('code')}")
        else:
            print(f"❌ API ERROR: Status {response.status_code}")
            print(f"   Message: {response.text}")
    except Exception as e:
        print(f"❌ CONNECTION FAILED: {e}")

print("-" * 30)