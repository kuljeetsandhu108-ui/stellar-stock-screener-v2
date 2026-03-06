import os
import sys
import traceback

print("\n" + "="*50)
print("🤖 PURE AI CORE DIAGNOSTIC TOOL")
print("="*50 + "\n")

# 1. CHECK LIBRARIES
try:
    import google.generativeai as genai
    print("✅ google.generativeai library loaded.")
except ImportError:
    print("❌ ERROR: google.generativeai is NOT installed. Run: pip install google-generativeai")
    sys.exit(1)
    
try:
    from dotenv import load_dotenv
    print("✅ python-dotenv library loaded.")
except ImportError:
    print("❌ ERROR: python-dotenv is NOT installed.")
    sys.exit(1)

# 2. LOCATE .ENV FILE
env_paths =['backend/.env', '.env', '../backend/.env', 'backend/.env.txt']
found_env = False
for ep in env_paths:
    if os.path.exists(ep):
        load_dotenv(ep)
        print(f"✅ Loaded environment variables from: {ep}")
        found_env = True
        break
        
if not found_env:
    print("❌ ERROR: Could not locate .env file! The AI has no keys.")
    print("Current working directory:", os.getcwd())
    sys.exit(1)

# 3. VERIFY API KEY
key_str = os.getenv("GEMINI_API_KEYS") or os.getenv("GEMINI_API_KEY")
if not key_str:
    print("❌ ERROR: GEMINI_API_KEY is completely empty or missing inside the .env file.")
    sys.exit(1)
    
keys =[k.strip() for k in key_str.split(',') if k.strip()]
if not keys:
    print("❌ ERROR: Key format is invalid.")
    sys.exit(1)

first_key = keys[0]
print(f"🔑 Extracted Key: {first_key[:5]}...{first_key[-4:]}")

# 4. PING GOOGLE SERVERS DIRECTLY
print("\n📡 Pinging Google's Servers (Model: gemini-1.5-flash)...")
try:
    genai.configure(api_key=first_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Respond with exactly two words: 'SYSTEM ONLINE'")
    
    print(f"\n🎉 GOOGLE RAW RESPONSE: {response.text.strip()}")
    print("✅ THE AI CORE IS 100% HEALTHY!")
    
except Exception as e:
    print("\n❌ CRITICAL AI FAILURE DETECTED!")
    print("-" * 50)
    traceback.print_exc()
    print("-" * 50)
