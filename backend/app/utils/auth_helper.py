import os
import pyotp
import requests
import base64
from urllib.parse import urlparse, parse_qs
from fyers_apiv3 import fyersModel

def get_fresh_fyers_token():
    client_id = os.getenv("FYERS_CLIENT_ID")
    secret_key = os.getenv("FYERS_SECRET_KEY")
    redirect_uri = "https://trade.fyers.in/api-login/redirect-uri/index.html"
    user_id = os.getenv("FYERS_USER_ID")
    pin = os.getenv("FYERS_PIN")
    totp_key = os.getenv("FYERS_TOTP_KEY")

    if not all([client_id, secret_key, user_id, pin, totp_key]):
        print("❌ Missing Auto-Login Credentials")
        return None

    try:
        # 1. Login Flow (Simulated)
        session = requests.Session()
        res = session.post("https://api-t2.fyers.in/vagator/v1/send_login_otp", json={"fy_id": base64.b64encode(f"{user_id}".encode()).decode(), "app_id": "2"}).json()
        request_key = res["request_key"]

        otp = pyotp.TOTP(totp_key).now()
        res = session.post("https://api-t2.fyers.in/vagator/v1/verify_otp", json={"request_key": request_key, "otp": otp}).json()
        request_key_2 = res["request_key"]

        res = session.post("https://api-t2.fyers.in/vagator/v1/verify_pin_v2", json={"request_key": request_key_2, "identity_type": "pin", "identifier": base64.b64encode(f"{pin}".encode()).decode()}).json()
        bearer_token = res["data"]["access_token"]

        headers = {"Authorization": f"Bearer {bearer_token}", "Content-Type": "application/json"}
        auth_payload = {"fyers_id": user_id, "app_id": client_id[:-4] if client_id.endswith("-100") else client_id, "redirect_uri": redirect_uri, "response_type": "code", "state": "sample", "scope": "", "nonce": "", "create_cookie": True}
        
        res = session.post("https://api.fyers.in/api/v3/token", headers=headers, json=auth_payload).json()
        auth_code = parse_qs(urlparse(res["Url"]).query)["auth_code"][0]

        # 2. Get Token
        fs = fyersModel.SessionModel(client_id=client_id, secret_key=secret_key, redirect_uri=redirect_uri, response_type="code", grant_type="authorization_code")
        fs.set_token(auth_code)
        response = fs.generate_token()
        
        return response["access_token"]
    except Exception as e:
        print(f"❌ Auto-Login Failed: {e}")
        return None