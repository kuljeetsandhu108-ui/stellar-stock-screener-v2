from fyers_apiv3 import fyersModel
import webbrowser
import os
from dotenv import load_dotenv

# 1. SETUP - Load your local .env or hardcode here
load_dotenv("backend/.env") 

client_id = os.getenv("FYERS_CLIENT_ID")     # e.g., "SIHHVG8XH6-100"
secret_key = "HHADUAK0CL"               # <--- PASTE YOUR SECRET KEY HERE MANUALLY IF NOT IN ENV
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
response_type = "code"  
state = "sample_state"

# 2. GENERATE LOGIN LINK
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type
)

auth_link = session.generate_authcode()
print("\n🔹 Step 1: Login here if you haven't already:")
print(auth_link)
webbrowser.open(auth_link)

# 3. INPUT AUTH CODE
print("\n🔹 Step 2: Copy the 'authorization_code' from the website.")
auth_code = input("👉 Paste Auth Code here: ").strip()

# 4. EXCHANGE FOR ACCESS TOKEN
session.set_token(auth_code)
response = session.generate_token()

print("\n=======================================================")
if "access_token" in response:
    print("✅ SUCCESS! HERE IS YOUR REAL ACCESS TOKEN:")
    print("-------------------------------------------------------")
    print(response["access_token"])
    print("-------------------------------------------------------")
    print("👉 Copy the LONG string above and paste it into Railway 'FYERS_ACCESS_TOKEN'")
else:
    print("❌ FAILED. Response from Fyers:")
    print(response)
print("=======================================================")