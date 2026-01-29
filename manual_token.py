from fyers_apiv3 import fyersModel
import webbrowser

print("--- FYERS TOKEN GENERATOR ---")

# 1. INPUT CREDENTIALS
client_id = input("BV2MMI534L-100").strip()
secret_key = input("HHADUAK0CL").strip()
redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"

# 2. GENERATE URL
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type="code"
)

auth_link = session.generate_authcode()
print("\n3. Login via this link (Opening in browser...):")
print(auth_link)
webbrowser.open(auth_link)

# 3. PASTE CODE
auth_code = input("\n4. Paste the 'authorization_code' here: ").strip()

# 4. GENERATE
try:
    session.set_token(auth_code)
    response = session.generate_token()

    if "access_token" in response:
        print("\n✅ SUCCESS! HERE IS YOUR REAL TOKEN:")
        print("=======================================================")
        print(response["access_token"])
        print("=======================================================")
        print("👉 Copy this LONG string into Railway 'FYERS_ACCESS_TOKEN'")
    else:
        print("\n❌ FAILED. Response:")
        print(response)
except Exception as e:
    print(f"\n❌ CRITICAL ERROR: {e}")