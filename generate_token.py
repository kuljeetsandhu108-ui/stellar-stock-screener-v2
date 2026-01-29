from fyers_apiv3 import fyersModel
import webbrowser

# REPLACE THESE WITH YOUR EXACT CREDENTIALS FROM FYERS DASHBOARD
CLIENT_ID = "SIHHVG8XH6-100"  # This is what Railway is using (from your logs)
SECRET_KEY = "5YCW9I6EXY" # Look this up in Fyers Dashboard
REDIRECT_URI = "https://trade.fyers.in/api-login/redirect-uri/index.html" # Or whatever you set in Fyers

response_type = "code" 
state = "sample_state"

# 1. Generate Auth URL
session = fyersModel.SessionModel(
    client_id=CLIENT_ID,
    secret_key=SECRET_KEY,
    redirect_uri=REDIRECT_URI,
    response_type=response_type
)

auth_link = session.generate_authcode()
print("\n1. Click this link to login & authorize:")
print(auth_link)
webbrowser.open(auth_link)

# 2. Paste Auth Code
auth_code = input("\n2. Paste the Auth Code from the URL here: ")

# 3. Generate Token
session.set_token(auth_code)
response = session.generate_token()

print("\n---------------------------------------------------")
print("✅ YOUR NEW ACCESS TOKEN (Copy this to Railway):")
print(response['access_token'])
print("---------------------------------------------------")