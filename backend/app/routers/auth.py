import os
import requests
import hashlib
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel

router = APIRouter()

# Load Credentials
CLIENT_ID = os.getenv("FYERS_CLIENT_ID") 
SECRET_KEY = os.getenv("FYERS_SECRET_KEY")
# Ensure this matches your Fyers Dashboard EXACTLY
REDIRECT_URI = os.getenv("FRONTEND_URL", "http://localhost:3000") + "/auth-callback"

class AuthCodeRequest(BaseModel):
    auth_code: str

@router.get("/fyers/login-url")
def get_login_url():
    """
    Returns the official Fyers Login URL.
    """
    if not CLIENT_ID or not SECRET_KEY:
        raise HTTPException(status_code=500, detail="Server config missing (Client ID/Secret)")
        
    url = (
        f"https://api.fyers.in/api/v3/generate-authcode?"
        f"client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&"
        f"response_type=code&state=stellar_login"
    )
    return {"url": url}

@router.post("/fyers/validate")
async def validate_fyers_auth(data: AuthCodeRequest):
    """
    Exchanges the temporary Auth Code for a User Access Token.
    """
    try:
        # 1. Generate AppHash (SHA256 of AppID:Secret)
        app_id_clean = CLIENT_ID[:-4] if CLIENT_ID.endswith("-100") else CLIENT_ID
        app_hash_string = f"{CLIENT_ID}:{SECRET_KEY}"
        app_hash = hashlib.sha256(app_hash_string.encode()).hexdigest()
        
        # 2. Prepare Request
        payload = {
            "grant_type": "authorization_code",
            "appIdHash": app_hash,
            "code": data.auth_code,
        }
        
        # 3. Call Fyers API
        response = requests.post("https://api.fyers.in/api/v3/validate-authcode", json=payload)
        res_json = response.json()
        
        if res_json.get("s") == "ok":
            return {
                "access_token": res_json.get("access_token"),
                "user_name": res_json.get("name", "Trader"),
                "client_id": CLIENT_ID # Needed for frontend socket
            }
        else:
            print(f"Fyers Auth Failed: {res_json}")
            raise HTTPException(status_code=400, detail=res_json.get("message", "Login failed"))
            
    except Exception as e:
        print(f"Auth Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))