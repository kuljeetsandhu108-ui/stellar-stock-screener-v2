This file is a merged representation of a subset of the codebase, containing files not matching ignore patterns, combined into a single document by Repomix.

# File Summary

## Purpose
This file contains a packed representation of a subset of the repository's contents that is considered the most important context.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching these patterns are excluded: **/.env, **/venv/**, **/node_modules/**, **/build/**, **/package-lock.json, **/*fyersDataSocket*.txt
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.dockerignore
.gitignore
backend/app/__init__.py
backend/app/config.py
backend/app/main.py
backend/app/routers/__init__.py
backend/app/routers/auth.py
backend/app/routers/charts.py
backend/app/routers/indices.py
backend/app/routers/live.py
backend/app/routers/stocks.py
backend/app/routers/stream.py
backend/app/services/__init__.py
backend/app/services/eodhd_service.py
backend/app/services/fmp_service.py
backend/app/services/fundamental_service.py
backend/app/services/gemini_service.py
backend/app/services/indian_service.py
backend/app/services/news_service.py
backend/app/services/redis_service.py
backend/app/services/sentiment_service.py
backend/app/services/stream_hub.py
backend/app/services/technical_service.py
backend/app/utils/auth_helper.py
backend/requirements.txt
backend/worker.py
check_keys.py
Dockerfile
frontend/package.json
frontend/public/index.html
frontend/src/api/stockApi.js
frontend/src/App.js
frontend/src/components/Chart/CustomChart.js
frontend/src/components/Chart/TradingViewChart.js
frontend/src/components/common/Card.js
frontend/src/components/common/Loader.js
frontend/src/components/common/Tabs/NestedTabs.js
frontend/src/components/common/Tabs/Tabs.js
frontend/src/components/Financials/AboutCompany.js
frontend/src/components/Financials/BalanceSheet.js
frontend/src/components/Financials/Financials.js
frontend/src/components/Financials/FinancialStatements.js
frontend/src/components/Financials/KeyStats.js
frontend/src/components/Financials/RevenueChart.js
frontend/src/components/Financials/StatementTable.js
frontend/src/components/Forecasts/AnalystRating.js
frontend/src/components/Forecasts/Forecasts.js
frontend/src/components/Forecasts/PriceTarget.js
frontend/src/components/Fundamentals/BenjaminGrahamScan.js
frontend/src/components/Fundamentals/DarvasScan.js
frontend/src/components/Fundamentals/FundamentalConclusion.js
frontend/src/components/Fundamentals/Fundamentals.js
frontend/src/components/Header/ConnectBroker.js
frontend/src/components/Header/StockHeader.js
frontend/src/components/HomePage/ChartUploader.js
frontend/src/components/IndexDetailPage/IndexChartAnalysis.js
frontend/src/components/Indices/IndicesBanner.js
frontend/src/components/News/NewsList.js
frontend/src/components/Overview/PriceLevels.js
frontend/src/components/Peers/PeersComparison.js
frontend/src/components/Sentiment/OverallSentiment.js
frontend/src/components/Shareholding/DonutChart.js
frontend/src/components/Shareholding/OwnershipTrend.js
frontend/src/components/Shareholding/Shareholding.js
frontend/src/components/Shareholding/TrendChart.js
frontend/src/components/StockDetailPage/ChartAnalysis.js
frontend/src/components/SWOT/SwotAnalysis.js
frontend/src/components/Technicals/MovingAverages.js
frontend/src/components/Technicals/PivotLevels.js
frontend/src/components/Technicals/RatingDial.js
frontend/src/components/Technicals/TechnicalIndicatorsTable.js
frontend/src/components/Technicals/Technicals.js
frontend/src/index.js
frontend/src/pages/AuthCallback.js
frontend/src/pages/HomePage.js
frontend/src/pages/IndexDetailPage.js
frontend/src/pages/PureVisionPage.js
frontend/src/pages/StockDetailPage.js
frontend/src/styles/GlobalStyles.js
frontend/src/utils/FyersClientEngine.js
frontend/src/utils/smc_algorithms.js
generate_token.py
get_real_token.py
manual_token.py
nixpacks.toml
requirements.txt
test_api.py
```

# Files

## File: .dockerignore
```
# Git
.git
.gitignore

# Python
backend/venv
backend/__pycache__

# Node
frontend/node_modules
frontend/build

# Docker
Dockerfile
```

## File: .gitignore
```
# Python
/backend/venv/
/backend/__pycache__/
/backend/.env

# Node
/frontend/node_modules/
/frontend/build/
/frontend/.env

# IDE
.vscode/
```

## File: backend/app/__init__.py
```python

```

## File: backend/app/config.py
```python
import os
from dotenv import load_dotenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 1. Try loading from the current directory (Root)
load_dotenv()

# 2. Try loading from the backend directory (Explicit fallback)
env_path = BASE_DIR / ".env"
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)

print(f"🔧 CONFIG LOADED. EODHD Key found: {'YES' if os.getenv('EODHD_API_KEY') else 'NO'}")
```

## File: backend/app/routers/__init__.py
```python

```

## File: backend/app/routers/auth.py
```python
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
```

## File: backend/app/routers/live.py
```python
import asyncio
import json
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ..services import eodhd_service

router = APIRouter()

# Manager to handle active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    await manager.connect(websocket)
    
    # Identify Asset Class
    symbol = symbol.upper()
    is_crypto = "BTC" in symbol or "ETH" in symbol or ".CC" in symbol
    is_us = ".US" in symbol and not is_crypto
    is_nse = ".NSE" in symbol or ".BO" in symbol or "NIFTY" in symbol or "SENSEX" in symbol

    # Normalization for EODHD logic
    eod_symbol = eodhd_service.format_symbol_for_eodhd(symbol)

    try:
        while True:
            # 1. FETCH DATA (Fastest Method Available)
            data = await asyncio.to_thread(eodhd_service.get_live_price, eod_symbol)
            
            if data and data.get('price'):
                # 2. CONSTRUCT PAYLOAD
                payload = {
                    "price": data.get('price'),
                    "change": data.get('change'),
                    "percent_change": data.get('changesPercentage'),
                    "volume": data.get('volume'),
                    "timestamp": data.get('timestamp')
                }
                
                # 3. PUSH TO FRONTEND
                await manager.send_personal_message(json.dumps(payload), websocket)
            
            # 4. THROTTLE (The Heartbeat)
            # For Crypto: Ultra Fast (1s)
            # For NSE/Stocks: Standard Fast (2s) - To respect API limits while feeling "Live"
            sleep_time = 1 if is_crypto else 2
            await asyncio.sleep(sleep_time)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WS Error {symbol}: {e}")
        manager.disconnect(websocket)
```

## File: backend/app/services/__init__.py
```python

```

## File: backend/app/services/indian_service.py
```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# 1. Get the key
INDIAN_API_KEY = os.getenv("INDIAN_API_KEY")

# 2. Set your specific provider URL here (Example: A common RapidAPI endpoint)
# You will replace this URL with the specific one you subscribe to.
BASE_URL = "https://latest-stock-price.p.rapidapi.com" 

def get_indian_shareholding(symbol: str):
    """
    Fetches precise shareholding pattern for Indian stocks from a dedicated API.
    """
    if not INDIAN_API_KEY:
        return None

    # Clean the symbol: Remove .NS or .BO for many Indian APIs
    clean_symbol = symbol.replace('.NS', '').replace('.BO', '')

    headers = {
        "X-RapidAPI-Key": INDIAN_API_KEY,
        "X-RapidAPI-Host": "latest-stock-price.p.rapidapi.com" # Update this host to match your provider
    }

    try:
        # Example endpoint structure - Update based on your specific API documentation
        url = f"{BASE_URL}/shareholding-pattern?symbol={clean_symbol}"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # --- NORMALIZE DATA ---
        # Convert the specific API's response to our standard format
        # (This logic depends on the exact response format of the API you choose)
        
        return {
            "promoter": data.get('promoter', 0),
            "fii": data.get('fii', 0),
            "dii": data.get('dii', 0),
            "public": data.get('public', 0)
        }

    except Exception as e:
        print(f"Error fetching Indian shareholding for {symbol}: {e}")
        return None
```

## File: backend/app/services/news_service.py
```python
import os
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file in the `backend` directory
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

def get_company_news(query: str, page_size: int = 20):
    """
    Fetches recent news articles related to a specific company or query
    from the News API. It sorts by the most recently published.
    """
    if not NEWS_API_KEY:
        print("Error: NEWS_API_KEY not found in .env file.")
        return {"error": "News API key not configured."}
    
    # We add quotes around the query for more exact matches
    # e.g., searching for "Apple Inc" instead of just Apple
    params = {
        "q": f'"{query}"',
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        # We extract only the 'articles' list from the response
        return response.json().get("articles", [])
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching company news for '{query}': {e}")
        return []
```

## File: backend/app/utils/auth_helper.py
```python
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
```

## File: check_keys.py
```python
import os
from dotenv import load_dotenv

# Try loading from specific path to be sure
load_dotenv("backend/.env")

print("--- DIAGNOSTIC ---")
print(f"EODHD Key: {os.getenv('EODHD_API_KEY')}")
print(f"FMP Key:   {os.getenv('FMP_API_KEY')}")
print(f"Redis URL: {os.getenv('REDIS_URL')}")
print("------------------")
```

## File: frontend/src/api/stockApi.js
```javascript

```

## File: frontend/src/components/Chart/TradingViewChart.js
```javascript
import React, { useEffect, useRef, memo } from 'react';
import Card from '../common/Card';

const TradingViewChart = ({ symbol }) => {
  const container = useRef();

  useEffect(() => {
    // Ensure the TradingView script is loaded and the container ref is set
    if (window.TradingView && container.current) {
      // Clear the container before creating a new widget
      // This is crucial for preventing duplicate charts when the component re-renders
      container.current.innerHTML = '';

      // Create a new TradingView widget instance
      new window.TradingView.widget({
        autosize: true, // This makes the chart fill its container
        symbol: symbol,
        interval: "D", // Daily interval
        timezone: "Etc/UTC",
        theme: "dark", // Dark theme to match our app
        style: "1",
        locale: "en",
        enable_publishing: false,
        allow_symbol_change: true,
        withdateranges: true,
        hide_side_toolbar: false,
        studies: [
          "Volume@tv-basicstudies" // Add volume as a default study
        ],
        container_id: container.current.id,
      });
    }
  }, [symbol]); // Re-run the effect if the stock symbol changes

  return (
    <Card title="Advanced Chart">
      <div 
        ref={container} 
        id={`tradingview_${symbol}`} 
        style={{ height: "600px", width: "100%" }} 
      />
    </Card>
  );
};

// Use React.memo to prevent unnecessary re-renders of the chart
// The chart will only re-render if its 'symbol' prop changes.
export default memo(TradingViewChart);
```

## File: frontend/src/components/common/Loader.js
```javascript

```

## File: frontend/src/components/Financials/AboutCompany.js
```javascript
import React from 'react';
import styled from 'styled-components';

// --- Styled Components ---

const AboutContainer = styled.div`
  /* Styling for the container if needed in the future */
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--color-text-primary);
`;

const Description = styled.p`
  font-size: 1rem;
  color: var(--color-text-secondary);
  line-height: 1.7; /* Generous line spacing for readability */
`;


// --- The React Component ---

const AboutCompany = ({ profile }) => {
  // Defensive check: If there is no profile or description, render nothing.
  if (!profile || !profile.description) {
    return null;
  }

  return (
    <AboutContainer>
      <SectionTitle>About {profile.companyName}</SectionTitle>
      <Description>
        {profile.description}
      </Description>
    </AboutContainer>
  );
};

export default AboutCompany;
```

## File: frontend/src/components/Financials/BalanceSheet.js
```javascript
import React from 'react';
import styled from 'styled-components';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  CartesianGrid
} from 'recharts';

// --- Styled Components ---

const SectionContainer = styled.div`
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid var(--color-border);
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--color-text-primary);
`;

const ChartGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  height: 450px; /* Give a consistent height to the chart area */

  @media (max-width: 992px) {
    grid-template-columns: 1fr;
    height: auto;
    gap: 4rem;
  }
`;

const CustomTooltipContainer = styled.div`
  background-color: #2a3441;
  border: 1px solid var(--color-border);
  padding: 1rem;
  border-radius: 8px;
  color: var(--color-text-primary);
`;

const formatNumber = (num) => {
    if (num === null || num === undefined) return 'N/A';
    if (Math.abs(num) >= 1e9) return `${(num / 1e9).toFixed(2)}B`;
    if (Math.abs(num) >= 1e6) return `${(num / 1e6).toFixed(2)}M`;
    return num.toLocaleString();
};


// --- The React Component ---

const BalanceSheet = ({ balanceSheetData }) => {
  if (!balanceSheetData || !Array.isArray(balanceSheetData) || balanceSheetData.length === 0) {
    return (
      <SectionContainer>
        <SectionTitle>Balance Sheet</SectionTitle>
        <p>Balance sheet data is not available for this stock.</p>
      </SectionContainer>
    );
  }

  // Process the data for our stacked bar charts, reversing for chronological order
  const chartData = balanceSheetData.slice(0, 5).reverse().map(item => ({
    year: item.calendarYear,
    // Assets
    currentAssets: item.totalCurrentAssets,
    longTermAssets: item.totalNonCurrentAssets,
    // Liabilities & Equity
    currentLiabilities: item.totalCurrentLiabilities,
    longTermDebt: item.longTermDebt,
    equity: item.totalStockholdersEquity,
  }));
  
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <CustomTooltipContainer>
          <p style={{ fontWeight: 'bold' }}>Year: {label}</p>
          {payload.map(p => (
            <p key={p.dataKey} style={{ color: p.color }}>
              {`${p.name}: ${formatNumber(p.value)}`}
            </p>
          ))}
        </CustomTooltipContainer>
      );
    }
    return null;
  };

  return (
    <SectionContainer>
      <SectionTitle>Balance Sheet Composition (5-Year Trend)</SectionTitle>
      <ChartGrid>
        {/* --- Chart 1: Assets --- */}
        <div>
            <h4 style={{textAlign: 'center', marginBottom: '1rem', color: 'var(--color-text-secondary)'}}>Assets</h4>
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
                    <XAxis type="number" stroke="var(--color-text-secondary)" tickFormatter={formatNumber} />
                    <YAxis type="category" dataKey="year" stroke="var(--color-text-secondary)" />
                    <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(136, 132, 216, 0.1)' }} />
                    <Legend />
                    <Bar dataKey="currentAssets" name="Current Assets" stackId="a" fill="#8884d8" />
                    <Bar dataKey="longTermAssets" name="Long-Term Assets" stackId="a" fill="#82ca9d" />
                </BarChart>
            </ResponsiveContainer>
        </div>

        {/* --- Chart 2: Liabilities & Equity --- */}
        <div>
            <h4 style={{textAlign: 'center', marginBottom: '1rem', color: 'var(--color-text-secondary)'}}>Liabilities & Equity</h4>
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
                    <XAxis type="number" stroke="var(--color-text-secondary)" tickFormatter={formatNumber} />
                    <YAxis type="category" dataKey="year" stroke="var(--color-text-secondary)" />
                    <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(136, 132, 216, 0.1)' }} />
                    <Legend />
                    <Bar dataKey="currentLiabilities" name="Current Liabilities" stackId="b" fill="#FFCB77" />
                    <Bar dataKey="longTermDebt" name="Long-Term Debt" stackId="b" fill="#FE6D73" />
                    <Bar dataKey="equity" name="Equity" stackId="b" fill="#17C3B2" />
                </BarChart>
            </ResponsiveContainer>
        </div>
      </ChartGrid>
    </SectionContainer>
  );
};

export default BalanceSheet;
```

## File: frontend/src/components/Financials/FinancialStatements.js
```javascript
import React, { useState } from 'react';
import styled from 'styled-components';
import StatementTable from './StatementTable'; // We will create this next

// --- Styled Components ---

const SectionContainer = styled.div`
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid var(--color-border);
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--color-text-primary);
`;

const ToggleContainer = styled.div`
  display: flex;
  justify-content: flex-end;
  margin-bottom: 1.5rem;
`;

const ToggleButton = styled.button`
  padding: 0.5rem 1rem;
  border: 1px solid var(--color-border);
  background-color: ${({ active }) => (active ? 'var(--color-primary)' : 'var(--color-secondary)')};
  color: ${({ active }) => (active ? 'var(--color-background)' : 'var(--color-text-primary)')};
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;

  &:first-child {
    border-radius: 6px 0 0 6px;
  }
  &:last-child {
    border-radius: 0 6px 6px 0;
  }
  &:hover {
    background-color: var(--color-primary);
    color: var(--color-background);
  }
`;

const StatementsGrid = styled.div`
  display: flex;
  flex-direction: column;
  gap: 3rem;
`;

// --- The Main React Component ---

const FinancialStatements = ({
  currency,
  annualIncome, annualBalance, annualCashFlow,
  quarterlyIncome, quarterlyBalance, quarterlyCashFlow
}) => {
  const [period, setPeriod] = useState('annual'); // Default to 'annual'

  const isAnnual = period === 'annual';

  return (
    <SectionContainer>
      <SectionTitle>Financial Statements</SectionTitle>
      
      <ToggleContainer>
        <ToggleButton active={isAnnual} onClick={() => setPeriod('annual')}>
          Annual
        </ToggleButton>
        <ToggleButton active={!isAnnual} onClick={() => setPeriod('quarterly')}>
          Quarterly
        </ToggleButton>
      </ToggleContainer>

      <StatementsGrid>
        {/* We pass the correctly selected data and currency to our table component */}
        <StatementTable
          title="Income Statement"
          data={isAnnual ? annualIncome : quarterlyIncome}
          currency={currency}
        />
        <StatementTable
          title="Balance Sheet"
          data={isAnnual ? annualBalance : quarterlyBalance}
          currency={currency}
        />
        <StatementTable
          title="Cash Flow Statement"
          data={isAnnual ? annualCashFlow : quarterlyCashFlow}
          currency={currency}
        />
      </StatementsGrid>
    </SectionContainer>
  );
};

export default FinancialStatements;
```

## File: frontend/src/components/Financials/KeyStats.js
```javascript
import React from 'react';
import styled from 'styled-components';

// --- Styled Components ---

const StatsContainer = styled.div`
  padding-bottom: 2rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid var(--color-border);
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--color-text-primary);
`;

const StatsGrid = styled.div`
  display: grid;
  /* Create 4 equal columns on larger screens */
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem 1rem; /* Vertical and horizontal gap */

  /* On smaller screens, reduce to 2 columns */
  @media (max-width: 992px) {
    grid-template-columns: repeat(2, 1fr);
  }
`;

const StatItem = styled.div`
  display: flex;
  flex-direction: column;
`;

const StatLabel = styled.span`
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  margin-bottom: 0.25rem;
`;

const StatValue = styled.span`
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-text-primary);
`;

// --- Helper Functions to Format Data ---

const formatMarketCap = (num) => {
  if (num === null || num === undefined) return '--';
  if (num >= 1e12) return `$${(num / 1e12).toFixed(2)} T`;
  if (num >= 1e9) return `$${(num / 1e9).toFixed(2)} B`;
  if (num >= 1e6) return `$${(num / 1e6).toFixed(2)} M`;
  return `$${num}`;
};

const formatNumber = (num) => {
  if (num === null || num === undefined) return '--';
  return num.toFixed(2);
};

const formatDate = (dateStr) => {
    if (!dateStr) return '--';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
};


// --- The Main React Component ---

const KeyStats = ({ stats }) => {
  if (!stats) return null;

  return (
    <StatsContainer>
      {/* --- Upcoming Earnings Section --- */}
      <SectionTitle>Upcoming Earnings</SectionTitle>
      <StatsGrid>
        <StatItem>
          <StatLabel>Next Report Date</StatLabel>
          <StatValue>{formatDate(stats.nextReportDate)}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>EPS Estimate</StatLabel>
          <StatValue>{formatNumber(stats.epsEstimate)}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Revenue Estimate</StatLabel>
          <StatValue>{formatMarketCap(stats.revenueEstimate)}</StatValue>
        </StatItem>
      </StatsGrid>

      {/* --- Key Stats Section --- */}
      <SectionTitle style={{ marginTop: '2rem' }}>Key Stats</SectionTitle>
      <StatsGrid>
        <StatItem>
          <StatLabel>Market Capitalization</StatLabel>
          <StatValue>{formatMarketCap(stats.marketCap)}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Dividend Yield (TTM)</StatLabel>
          <StatValue>{stats.dividendYield ? `${(stats.dividendYield * 100).toFixed(2)}%` : '--'}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Price to Earnings (TTM)</StatLabel>
          <StatValue>{formatNumber(stats.peRatio)}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Basic EPS (TTM)</StatLabel>
          <StatValue>{formatNumber(stats.basicEPS)}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Net Income / Share</StatLabel>
          <StatValue>{formatNumber(stats.netIncome)}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Revenue / Share</StatLabel>
          <StatValue>{formatNumber(stats.revenue)}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Shares Float</StatLabel>
          <StatValue>{formatMarketCap(stats.sharesFloat)}</StatValue>
        </StatItem>
        <StatItem>
          <StatLabel>Beta (1Y)</StatLabel>
          <StatValue>{formatNumber(stats.beta)}</StatValue>
        </StatItem>
      </StatsGrid>
    </StatsContainer>
  );
};

export default KeyStats;
```

## File: frontend/src/components/Financials/RevenueChart.js
```javascript
import React from 'react';
import styled from 'styled-components';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
  CartesianGrid
} from 'recharts';

// --- Styled Components ---

const ChartContainer = styled.div`
  width: 100%;
  height: 400px; /* Give the chart a fixed height */
`;

// Custom Tooltip for a better look and feel
const CustomTooltipContainer = styled.div`
  background-color: #2a3441;
  border: 1px solid var(--color-border);
  padding: 1rem;
  border-radius: 8px;
  color: var(--color-text-primary);
`;

const TooltipLabel = styled.p`
  margin-bottom: 0.5rem;
  font-weight: bold;
`;

// --- Helper Functions ---

// Formats large numbers into Billions (B) or Millions (M) for the Y-axis
const formatYAxis = (tick) => {
  if (Math.abs(tick) >= 1e9) {
    return `${(tick / 1e9).toFixed(1)}B`;
  }
  if (Math.abs(tick) >= 1e6) {
    return `${(tick / 1e6).toFixed(1)}M`;
  }
  return tick;
};

// Formats large numbers with commas and adds a currency symbol
const formatCurrency = (value) => {
    return `$${new Intl.NumberFormat('en-US').format(value)}`;
};


// --- React Component ---

const RevenueChart = ({ data }) => {
  // The API sends data from newest to oldest, so we reverse it for the chart
  // and process it into a more usable format.
  const chartData = data.slice().reverse().map(item => ({
    year: new Date(item.date).getFullYear(),
    Revenue: item.revenue,
    'Net Profit': item.netIncome,
  }));

  // Custom Tooltip Component
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <CustomTooltipContainer>
          <TooltipLabel>{`Year: ${label}`}</TooltipLabel>
          <p style={{ color: '#8884d8' }}>{`Revenue: ${formatCurrency(payload[0].value)}`}</p>
          <p style={{ color: '#82ca9d' }}>{`Net Profit: ${formatCurrency(payload[1].value)}`}</p>
        </CustomTooltipContainer>
      );
    }
    return null;
  };

  return (
    <ChartContainer>
      {/* ResponsiveContainer makes the chart adapt to its parent's size */}
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={chartData}
          margin={{ top: 5, right: 20, left: 30, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke={ "var(--color-border)" } />
          <XAxis 
            dataKey="year" 
            stroke={ "var(--color-text-secondary)" }
            tick={{ fill: 'var(--color-text-secondary)', fontSize: 12 }} 
          />
          <YAxis 
            stroke={ "var(--color-text-secondary)" }
            tickFormatter={formatYAxis}
            tick={{ fill: 'var(--color-text-secondary)', fontSize: 12 }}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(136, 132, 216, 0.1)' }}/>
          <Legend wrapperStyle={{ fontSize: '14px', paddingTop: '20px' }} />
          <Bar dataKey="Revenue" fill="#8884d8" />
          <Bar dataKey="Net Profit" fill="#82ca9d" />
        </BarChart>
      </ResponsiveContainer>
    </ChartContainer>
  );
};

export default RevenueChart;
```

## File: frontend/src/components/Financials/StatementTable.js
```javascript
import React from 'react';
import styled from 'styled-components';

// --- Styled Components ---

const TableWrapper = styled.div`
  width: 100%;
  overflow-x: auto; /* The key to making the table horizontally scrollable */
`;

const StyledTable = styled.table`
  width: 100%;
  min-width: 800px; /* Ensures there's enough space for columns before scrolling */
  border-collapse: collapse;
  text-align: right;
`;

const TableHeader = styled.th`
  padding: 0.75rem 1rem;
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: 0.9rem;
  border-bottom: 1px solid var(--color-border);
  white-space: nowrap;

  &:first-child {
    text-align: left;
    position: sticky; /* Makes the first column "stick" to the left on scroll */
    left: 0;
    background-color: var(--color-secondary);
    z-index: 1;
  }
`;

const TableRow = styled.tr`
  &:nth-child(even) {
    background-color: rgba(0, 0, 0, 0.2);
  }
`;

const TableCell = styled.td`
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  font-family: 'Roboto Mono', monospace;
  white-space: nowrap;

  &:first-child {
    font-weight: 600;
    color: var(--color-text-primary);
    text-align: left;
    font-family: 'Inter', sans-serif;
    position: sticky;
    left: 0;
    background-color: var(--color-secondary);
    z-index: 1;
  }
`;

const Subtitle = styled.h4`
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: var(--color-text-primary);
`;

// --- Helper Functions ---

const getCurrencySymbol = (currencyCode) => {
    switch (currencyCode) {
        case 'INR': return '₹';
        case 'USD': return '$';
        case 'JPY': return '¥';
        default: return ''; // No symbol if currency is unknown
    }
};

const formatNumber = (num, currencySymbol) => {
    if (num === null || num === undefined || isNaN(num)) return 'N/A';
    // Format large numbers into Millions for readability, prepended with currency
    const value = Math.abs(num);
    const sign = num < 0 ? '-' : '';
    if (value >= 1e6) {
        return `${sign}${currencySymbol}${(value / 1e6).toFixed(2)}M`;
    }
    // For smaller numbers, just add commas
    return `${sign}${currencySymbol}${num.toLocaleString()}`;
};

// --- The Reusable React Component ---

const StatementTable = ({ title, data, currency }) => {
  if (!data || !Array.isArray(data) || data.length === 0) {
    return null; // Don't render if there's no data
  }

  // --- Intelligent Data Key Discovery ---
  // This is the "brain". It finds all the numerical data points available
  // in the first record, excluding known non-financial keys.
  const headers = data.map(item => item.calendarYear || item.date.substring(0, 4));
  const ignoredKeys = new Set(['date', 'symbol', 'reportedCurrency', 'cik', 'fillingDate', 'acceptedDate', 'calendarYear', 'period', 'link', 'finalLink']);
  const dataKeys = Object.keys(data[0]).filter(key => 
      !ignoredKeys.has(key) && typeof data[0][key] === 'number'
  );

  const currencySymbol = getCurrencySymbol(currency);

  return (
    <div>
      <Subtitle>{title}</Subtitle>
      <TableWrapper>
        <StyledTable>
          <thead>
            <tr>
              <TableHeader>Line Item</TableHeader>
              {headers.map((header, index) => (
                <TableHeader key={index}>{header}</TableHeader>
              ))}
            </tr>
          </thead>
          <tbody>
            {dataKeys.map(key => (
              <TableRow key={key}>
                {/* Format the key name to be more readable (e.g., "netIncome" -> "Net Income") */}
                <TableCell>{key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}</TableCell>
                {data.map((row, index) => (
                  <TableCell key={index}>{formatNumber(row[key], currencySymbol)}</TableCell>
                ))}
              </TableRow>
            ))}
          </tbody>
        </StyledTable>
      </TableWrapper>
    </div>
  );
};

export default StatementTable;
```

## File: frontend/src/components/Forecasts/AnalystRating.js
```javascript
import React, { useMemo } from 'react';
import styled from 'styled-components';
import GaugeChart from 'react-gauge-chart';

//...(Styled components are unchanged)...
const RatingContainer = styled.div`
  width: 100%;
`;
const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 2rem;
  color: var(--color-text-primary);
`;
const GaugeWrapper = styled.div`
  max-width: 450px;
  margin: 0 auto;
`;
const RatingText = styled.div`
  font-size: 1.8rem;
  font-weight: 700;
  text-align: center;
  margin-top: -40px;
  color: ${({ color }) => color};
`;
const BreakdownList = styled.div`
  margin-top: 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;
const BreakdownItem = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-between;
`;
const BreakdownLabel = styled.span`
  font-size: 1rem;
  color: var(--color-text-secondary);
  width: 100px;
`;
const BreakdownBarContainer = styled.div`
  flex-grow: 1;
  height: 8px;
  background-color: var(--color-border);
  border-radius: 4px;
  margin: 0 1rem;
`;
const BreakdownBar = styled.div`
  height: 100%;
  width: ${({ percent }) => percent}%;
  background-color: ${({ color }) => color};
  border-radius: 4px;
  transition: width 0.5s ease-out;
`;
const BreakdownValue = styled.span`
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-primary);
  width: 30px;
  text-align: right;
`;


const AnalystRating = ({ ratingsData }) => {
  const processedRatings = useMemo(() => {
    // MORE ROBUST CHECK: Ensure the array exists and has content.
    if (!ratingsData || !Array.isArray(ratingsData) || ratingsData.length === 0) {
      return null;
    }

    const ratingMap = {
      'strongSell': { count: 0, text: 'Strong Sell', color: '#F85149' },
      'sell': { count: 0, text: 'Sell', color: '#F88149' },
      'hold': { count: 0, text: 'Hold', color: '#EDBB5A' },
      'buy': { count: 0, text: 'Buy', color: '#3FB950' },
      'strongBuy': { count: 0, text: 'Strong Buy', color: '#17C3B2' },
    };

    let totalAnalysts = 0;

    // The FMP API gives the breakdown directly in the first object of the array
    const latestRatingData = ratingsData[0];
    
    ratingMap.strongSell.count = latestRatingData.ratingStrongSell || 0;
    ratingMap.sell.count = latestRatingData.ratingSell || 0;
    ratingMap.hold.count = latestRatingData.ratingHold || 0;
    ratingMap.buy.count = latestRatingData.ratingBuy || 0;
    ratingMap.strongBuy.count = latestRatingData.ratingStrongBuy || 0;

    totalAnalysts = Object.values(ratingMap).reduce((sum, item) => sum + item.count, 0);
    
    // FINAL GUARD: If after all that, we have no analysts, return null.
    if (totalAnalysts === 0) return null;

    let totalScore = 0;
    totalScore += ratingMap.strongSell.count * 1;
    totalScore += ratingMap.sell.count * 2;
    totalScore += ratingMap.hold.count * 3;
    totalScore += ratingMap.buy.count * 4;
    totalScore += ratingMap.strongBuy.count * 5;

    const averageScore = totalScore / totalAnalysts;
    const gaugePercent = (averageScore - 1) / 4;

    let consensusText = 'Hold';
    let consensusColor = ratingMap.hold.color;
    if (averageScore > 4.5) { consensusText = 'Strong Buy'; consensusColor = ratingMap.strongBuy.color; }
    else if (averageScore > 3.5) { consensusText = 'Buy'; consensusColor = ratingMap.buy.color; }
    else if (averageScore < 2.5) { consensusText = 'Sell'; consensusColor = ratingMap.sell.color; }
    else if (averageScore < 1.5) { consensusText = 'Strong Sell'; consensusColor = ratingMap.strongSell.color; }

    return {
      totalAnalysts,
      gaugePercent,
      consensusText,
      consensusColor,
      breakdown: Object.values(ratingMap).reverse(),
    };
  }, [ratingsData]);

  if (!processedRatings) {
    return (
      <RatingContainer>
        <SectionTitle>Analyst Rating</SectionTitle>
        <p>Analyst rating data is not available for this stock.</p>
      </RatingContainer>
    );
  }

  const { totalAnalysts, gaugePercent, consensusText, consensusColor, breakdown } = processedRatings;

  return (
    <RatingContainer>
      <SectionTitle>Analyst Rating</SectionTitle>
      <p style={{ color: 'var(--color-text-secondary)', marginTop: '-1.5rem', marginBottom: '2rem' }}>
          Based on {totalAnalysts} analysts giving stock ratings in the past 3 months.
      </p>

      <GaugeWrapper>
        <GaugeChart id="analyst-rating-gauge" nrOfLevels={5} arcsLength={[0.2, 0.15, 0.3, 0.15, 0.2]} colors={['#F85149', '#F88149', '#EDBB5A', '#3FB950', '#17C3B2']} percent={gaugePercent} arcPadding={0.02} cornerRadius={3} textColor={'transparent'} needleBaseColor={'#FFFFFF'} needleColor={'#C9D1D9'} />
        <RatingText color={consensusColor}>{consensusText}</RatingText>
      </GaugeWrapper>

      <BreakdownList>
        {breakdown.map(item => (
          <BreakdownItem key={item.text}>
            <BreakdownLabel>{item.text}</BreakdownLabel>
            <BreakdownBarContainer>
              <BreakdownBar percent={(item.count / totalAnalysts) * 100} color={item.color} />
            </BreakdownBarContainer>
            <BreakdownValue>{item.count}</BreakdownValue>
          </BreakdownItem>
        ))}
      </BreakdownList>
    </RatingContainer>
  );
};

export default AnalystRating;
```

## File: frontend/src/components/Fundamentals/BenjaminGrahamScan.js
```javascript
import React from 'react';
import styled from 'styled-components';

// --- Styled Components (reusing our professional styles) ---

const SectionContainer = styled.div`
  /* Main container for this scan */
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--color-text-primary);
`;

const ScanGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  align-items: center;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const ScoreCard = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-color: var(--color-background);
  border-radius: 50%;
  width: 180px;
  height: 180px;
  border: 4px solid ${({ scoreColor }) => scoreColor};
  margin: 0 auto;
`;

const ScoreValue = styled.span`
  font-size: 4rem;
  font-weight: 800;
  color: ${({ scoreColor }) => scoreColor};
`;

const ScoreLabel = styled.span`
  font-size: 1rem;
  font-weight: 500;
  color: var(--color-text-secondary);
`;

const CriteriaList = styled.ul`
  list-style-type: none;
  padding-left: 0;
`;

const CriteriaListItem = styled.li`
  margin-bottom: 0.75rem;
  color: var(--color-text-primary);
  display: flex;
  align-items: center;
  line-height: 1.6;

  &::before {
    content: '✓';
    color: var(--color-success);
    margin-right: 12px;
    font-size: 1.2rem;
    font-weight: bold;
  }
`;

// --- The React Component ---

const BenjaminGrahamScan = ({ scanData }) => {
  // If we don't have the data from the backend, show an informative message.
  if (!scanData || !scanData.criteria) {
    return (
      <SectionContainer>
        <SectionTitle>Benjamin Graham Scan</SectionTitle>
        <p>Graham scan data is not available or could not be calculated.</p>
      </SectionContainer>
    );
  }

  const { score, criteria } = scanData;

  // Determine the color based on the score (0-2 Red, 3-5 Yellow, 6-7 Green)
  const getScoreColor = () => {
    if (score >= 6) return 'var(--color-success)';
    if (score >= 3) return '#EDBB5A'; // Neutral Yellow
    return 'var(--color-danger)';
  };
  const scoreColor = getScoreColor();

  return (
    <SectionContainer>
      <SectionTitle>Benjamin Graham Scan</SectionTitle>
      <ScanGrid>
        <ScoreCard scoreColor={scoreColor}>
          <ScoreValue scoreColor={scoreColor}>{score}</ScoreValue>
          <ScoreLabel>/ 7 Tenets</ScoreLabel>
        </ScoreCard>
        <div>
          <p style={{ color: 'var(--color-text-secondary)', marginBottom: '1.5rem', lineHeight: 1.6 }}>
            A checklist for the "defensive investor" based on the principles of the father of value investing. A high score suggests a stable, reasonably priced company.
          </p>
          <CriteriaList>
            {criteria.map((item, index) => (
              <CriteriaListItem key={index}>{item}</CriteriaListItem>
            ))}
          </CriteriaList>
        </div>
      </ScanGrid>
    </SectionContainer>
  );
};

export default BenjaminGrahamScan;
```

## File: frontend/src/components/Header/ConnectBroker.js
```javascript
import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import axios from 'axios';
import { FaPlug, FaCheckCircle, FaSignOutAlt } from 'react-icons/fa';

const Button = styled.button`
  background: ${({ connected }) => (connected ? 'rgba(63, 185, 80, 0.15)' : 'linear-gradient(135deg, #58A6FF, #238636)')};
  border: 1px solid ${({ connected }) => (connected ? '#3FB950' : 'transparent')};
  color: ${({ connected }) => (connected ? '#3FB950' : '#ffffff')};
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
  white-space: nowrap;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  }
`;

const ConnectBroker = () => {
  const [token, setToken] = useState(localStorage.getItem('fyers_token'));

  const handleLogin = async () => {
    try {
      // 1. Get the login URL from backend
      // We use window.location.origin to dynamically pick localhost or 127.0.0.1
      const backendUrl = window.location.origin.replace('3000', '8000'); 
      const res = await axios.get(`${backendUrl}/api/auth/fyers/login-url`);
      
      if (res.data.url) {
        window.location.href = res.data.url;
      }
    } catch (e) {
      console.error("Login Error", e);
      // Detailed error message for debugging
      alert(`Could not connect to broker. Server says: ${e.message}`);
    }
  };

  const handleLogout = () => {
      localStorage.removeItem('fyers_token');
      localStorage.removeItem('fyers_client_id');
      setToken(null);
      window.location.reload(); // Refresh to reset sockets
  };

  if (token) {
    return (
      <Button connected onClick={handleLogout} title="Click to Disconnect">
        <FaCheckCircle /> Fyers Connected
      </Button>
    );
  }

  return (
    <Button onClick={handleLogin}>
      <FaPlug /> Connect Broker
    </Button>
  );
};

export default ConnectBroker;
```

## File: frontend/src/components/IndexDetailPage/IndexChartAnalysis.js
```javascript
import React, { useMemo } from 'react';
import styled, { keyframes } from 'styled-components';
import Card from '../common/Card';
import { 
  FaGlobeAmericas, FaChartLine, FaShieldAlt, FaBullseye, 
  FaExclamationTriangle, FaLayerGroup, FaArrowUp, FaArrowDown, FaExchangeAlt 
} from 'react-icons/fa';

// --- STYLED COMPONENTS (Gold/Macro Theme) ---

const fadeIn = keyframes`from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); }`;

const AnalysisContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  animation: ${fadeIn} 0.6s ease-out;
`;

const MacroVerdictCard = styled(Card)`
  text-align: center;
  border-left: 4px solid #EBCB8B; /* Gold Border */
  background: linear-gradient(145deg, rgba(235, 203, 139, 0.05), rgba(13, 17, 23, 1));
`;

const TrendDisplay = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: ${({ color }) => color};
  text-transform: uppercase;
  letter-spacing: 1px;
`;

const MacroText = styled.p`
  font-size: 1.1rem;
  color: var(--color-text-primary);
  line-height: 1.8;
  font-style: italic;
  max-width: 90%;
  margin: 0 auto;
`;

const GridSection = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const ZoneCard = styled.div`
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 1.5rem;
  position: relative;
  overflow: hidden;
`;

const ZoneTitle = styled.h4`
  color: #EBCB8B; /* Gold */
  font-size: 1rem;
  font-weight: 700;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const LevelList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const LevelItem = styled.li`
  color: var(--color-text-secondary);
  margin-bottom: 0.8rem;
  display: flex;
  align-items: start;
  gap: 10px;
  line-height: 1.5;

  svg { color: #EBCB8B; margin-top: 4px; }
`;

const StrategyBox = styled.div`
  background: linear-gradient(135deg, rgba(235, 203, 139, 0.1), rgba(13, 17, 23, 0.8));
  border: 1px solid #EBCB8B;
  border-radius: 12px;
  padding: 2rem;
  position: relative;
`;

const StrategyHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid rgba(235, 203, 139, 0.2);
  padding-bottom: 1rem;
`;

const DirectionBadge = styled.span`
  background: ${({ isBullish }) => isBullish ? '#3FB950' : '#F85149'};
  color: #000;
  padding: 5px 15px;
  border-radius: 50px;
  font-weight: 800;
  font-size: 1rem;
  text-transform: uppercase;
`;

const MetricRow = styled.div`
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  font-size: 1.1rem;
`;

const Label = styled.span` color: var(--color-text-secondary); font-size: 0.9rem; `;
const Value = styled.span` font-weight: 700; color: #EBCB8B; font-family: 'Roboto Mono'; `;

// --- COMPONENT ---

const IndexChartAnalysis = ({ analysisData }) => {
  
  // --- PARSER ---
  const parsed = useMemo(() => {
    if (!analysisData || typeof analysisData !== 'string') return null;
    
    const rawKeys = ['TREND', 'PATTERNS', 'LEVELS', 'VOLUME', 'MOMENTUM', 'INDICATORS', 'CONCLUSION', 'ACTION', 'ENTRY_ZONE', 'STOP_LOSS', 'TARGET_1', 'TARGET_2', 'RISK_REWARD', 'CONFIDENCE', 'RATIONALE'];
    const sections = {};
    let text = "\n" + analysisData.replace(/\*\*/g, '');

    rawKeys.forEach(key => {
      const regex = new RegExp(`(?:^|\\n)\\s*${key}\\s*:\\s*([\\s\\S]*?)(?=\\n\\s*[A-Z_]{3,}\\s*:|$)`, 'i');
      const match = text.match(regex);
      if (match) sections[key] = match[1].trim();
    });
    return sections;
  }, [analysisData]);

  if (!parsed) return null;

  // Visual Logic
  const isBullish = parsed.TREND?.toLowerCase().includes('uptrend') || parsed.TREND?.toLowerCase().includes('bullish');
  const isBearish = parsed.TREND?.toLowerCase().includes('downtrend') || parsed.TREND?.toLowerCase().includes('bearish');
  
  const TrendIcon = isBullish ? FaArrowUp : isBearish ? FaArrowDown : FaExchangeAlt;
  const trendColor = isBullish ? '#3FB950' : isBearish ? '#F85149' : '#EBCB8B';

  return (
    <AnalysisContainer>
      
      {/* 1. MACRO VERDICT */}
      <MacroVerdictCard>
        <div style={{color: '#EBCB8B', fontSize: '0.8rem', fontWeight: 600, marginBottom: '10px', textTransform: 'uppercase'}}>AI Macro Outlook</div>
        <TrendDisplay color={trendColor}>
           <TrendIcon /> {parsed.TREND || 'Consolidation'}
        </TrendDisplay>
        <MacroText>
          "{parsed.CONCLUSION || parsed.RATIONALE}"
        </MacroText>
      </MacroVerdictCard>

      {/* 2. STRATEGY ROOM */}
      <StrategyBox>
        <StrategyHeader>
           <div style={{display:'flex', flexDirection:'column'}}>
               <span style={{color:'#EBCB8B', fontSize:'0.8rem', fontWeight: 700}}>MARKET BIAS</span>
               <span style={{color:'white', fontSize:'1.4rem', fontWeight: 700}}>
                   {parsed.ACTION?.toUpperCase() || 'WAIT'}
               </span>
           </div>
           <DirectionBadge isBullish={isBullish || parsed.ACTION?.includes('BUY')}>
               {parsed.ACTION?.includes('BUY') ? 'LONG' : parsed.ACTION?.includes('SELL') ? 'SHORT' : 'NEUTRAL'}
           </DirectionBadge>
        </StrategyHeader>
        
        <MetricRow><Label>Entry Zone</Label><Value>{parsed.ENTRY_ZONE}</Value></MetricRow>
        <MetricRow><Label>Invalidation (SL)</Label><Value style={{color:'#F85149'}}>{parsed.STOP_LOSS}</Value></MetricRow>
        <MetricRow><Label>Objective 1</Label><Value style={{color:'#3FB950'}}>{parsed.TARGET_1}</Value></MetricRow>
        <MetricRow><Label>Objective 2</Label><Value style={{color:'#3FB950'}}>{parsed.TARGET_2}</Value></MetricRow>
      </StrategyBox>

      {/* 3. TECHNICAL DEEP DIVE */}
      <GridSection>
        <ZoneCard>
          <ZoneTitle><FaShieldAlt /> Key Levels</ZoneTitle>
          <LevelList>
             <LevelItem><FaChartLine /> {parsed.LEVELS}</LevelItem>
          </LevelList>
        </ZoneCard>

        <ZoneCard>
          <ZoneTitle><FaLayerGroup /> Market Structure</ZoneTitle>
          <LevelList>
             {parsed.PATTERNS && <LevelItem><FaGlobeAmericas /> {parsed.PATTERNS}</LevelItem>}
             {parsed.VOLUME && <LevelItem><FaChartLine /> {parsed.VOLUME}</LevelItem>}
             {parsed.INDICATORS && <LevelItem><FaBullseye /> {parsed.INDICATORS}</LevelItem>}
          </LevelList>
        </ZoneCard>
      </GridSection>

    </AnalysisContainer>
  );
};

export default IndexChartAnalysis;
```

## File: frontend/src/components/News/NewsList.js
```javascript
import React from 'react';
import styled from 'styled-components';
import Card from '../common/Card';

// --- Styled Components ---

const NewsListContainer = styled.ul`
  list-style-type: none;
  padding: 0;
  margin: 0;
  /* Allows the list to scroll if it's too long */
  max-height: 500px;
  overflow-y: auto;
`;

const NewsItem = styled.li`
  padding: 1rem 0.5rem;
  border-bottom: 1px solid var(--color-border);
  
  &:last-child {
    border-bottom: none; /* Remove border for the last item */
  }
`;

const NewsLink = styled.a`
  text-decoration: none;
  color: var(--color-text-primary);
  transition: color 0.2s ease;

  &:hover {
    color: var(--color-primary);
  }
`;

const NewsTitle = styled.h4`
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
`;

const NewsMeta = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.8rem;
  color: var(--color-text-secondary);
`;

// --- Helper Function ---

// Formats the ISO date string into a more readable format, e.g., "Nov 08, 2025"
const formatDate = (isoString) => {
  if (!isoString) return '';
  const date = new Date(isoString);
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: '2-digit',
    year: 'numeric',
  });
};


// --- React Component ---

const NewsList = ({ newsArticles }) => {

  // Defensive check: If there are no articles, show a message.
  if (!newsArticles || !Array.isArray(newsArticles) || newsArticles.length === 0) {
    return (
      <Card title="Latest News">
        <p>No recent news found for this company.</p>
      </Card>
    );
  }

  return (
    <Card title="Latest News">
      <NewsListContainer>
        {/* We'll show the top 15 articles */}
        {newsArticles.slice(0, 15).map((article, index) => (
          <NewsItem key={index}>
            <NewsLink href={article.url} target="_blank" rel="noopener noreferrer">
              <NewsTitle>{article.title}</NewsTitle>
              <NewsMeta>
                <span>{article.source.name}</span>
                <span>{formatDate(article.publishedAt)}</span>
              </NewsMeta>
            </NewsLink>
          </NewsItem>
        ))}
      </NewsListContainer>
    </Card>
  );
};

export default NewsList;
```

## File: frontend/src/components/Overview/PriceLevels.js
```javascript
import React from 'react';
import styled, { keyframes } from 'styled-components';
import Card from '../common/Card';
import { FaArrowUp, FaArrowDown, FaCrosshairs } from 'react-icons/fa';

// --- ANIMATIONS ---
const pulseGlow = keyframes`
  0% { box-shadow: 0 0 5px var(--color-primary), 0 0 10px var(--color-primary); }
  50% { box-shadow: 0 0 15px var(--color-primary), 0 0 25px var(--color-primary); }
  100% { box-shadow: 0 0 5px var(--color-primary), 0 0 10px var(--color-primary); }
`;

const slideIn = keyframes`
  from { width: 0; opacity: 0; }
  to { width: 100%; opacity: 1; }
`;

// --- STYLED COMPONENTS ---

const LadderContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  padding: 0.5rem;
`;

const HeaderRow = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
`;

const StatusBadge = styled.div`
  background: rgba(255, 255, 255, 0.05);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  color: ${({ color }) => color};
  border: 1px solid ${({ color }) => color}44;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
`;

const GraphicWrapper = styled.div`
  position: relative;
  height: 60px;
  width: 100%;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 8px;
  margin: 1rem 0;
  display: flex;
  align-items: center;
`;

const BarBackground = styled.div`
  position: absolute;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(to right, #F85149 0%, #EDBB5A 50%, #3FB950 100%);
  border-radius: 2px;
  opacity: 0.3;
`;

const CurrentPriceMarker = styled.div`
  position: absolute;
  left: ${({ percent }) => percent}%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 4px;
  height: 40px;
  background-color: var(--color-primary);
  border-radius: 2px;
  box-shadow: 0 0 15px var(--color-primary);
  animation: ${pulseGlow} 2s infinite;
  z-index: 10;
  transition: left 1s cubic-bezier(0.25, 0.8, 0.25, 1);

  &::after {
    content: '${({ price, currency }) => currency + price}';
    position: absolute;
    top: -25px;
    left: 50%;
    transform: translateX(-50%);
    background-color: var(--color-primary);
    color: #000;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 700;
    white-space: nowrap;
  }
`;

const LevelMarker = styled.div`
  position: absolute;
  left: ${({ percent }) => percent}%;
  top: 50%;
  transform: translate(-50%, -50%);
  height: 20px;
  width: 2px;
  background-color: ${({ color }) => color};
  opacity: 0.7;

  &::after {
    content: '${({ label }) => label}';
    position: absolute;
    bottom: -22px;
    left: 50%;
    transform: translateX(-50%);
    color: ${({ color }) => color};
    font-size: 0.7rem;
    font-weight: 600;
  }
`;

const LevelsGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-top: 0.5rem;
`;

const LevelCard = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  border-left: 3px solid ${({ color }) => color};
  animation: ${slideIn} 0.5s ease-out;
`;

const LevelLabel = styled.span`
  color: var(--color-text-secondary);
  font-size: 0.85rem;
  font-weight: 500;
`;

const LevelValue = styled.span`
  color: var(--color-text-primary);
  font-weight: 700;
  font-family: 'Roboto Mono', monospace;
`;

// --- HELPER FUNCTIONS ---
const getCurrencySymbol = (code) => (code === 'INR' ? '₹' : '$');

// **CRITICAL FIX**: Crash-proof number formatter
const safeFixed = (val, decimals = 2) => {
  if (val === undefined || val === null || isNaN(val)) return '--';
  return val.toFixed(decimals);
};

const PriceLevels = ({ pivotPoints, quote, profile }) => {
  // **CRITICAL FIX**: Stronger Guard Clause
  // We check if 'classic' exists AND if 'quote.price' is a valid number
  if (!pivotPoints || !pivotPoints.classic || !quote || typeof quote.price !== 'number') {
    return (
        <Card title="Key Levels">
            <p style={{color: 'var(--color-text-secondary)'}}>Levels data currently unavailable.</p>
        </Card>
    );
  }

  const { r2, r1, pp, s1, s2 } = pivotPoints.classic;
  const current = quote.price;
  const currency = getCurrencySymbol(profile?.currency);

  // Range Calculation logic (Safe)
  const rangeMin = s2 || (current * 0.95);
  const rangeMax = r2 || (current * 1.05);
  const totalRange = rangeMax - rangeMin;

  const getPercent = (val) => {
    if (!val || totalRange === 0) return 50;
    let pct = ((val - rangeMin) / totalRange) * 100;
    return Math.min(Math.max(pct, 5), 95); 
  };

  let status = "Consolidating";
  let statusColor = "#EDBB5A";
  let StatusIcon = FaCrosshairs;

  if (r1 && current > r1) {
    status = "Approaching Resistance";
    statusColor = "#F85149";
    StatusIcon = FaArrowUp;
  } else if (s1 && current < s1) {
    status = "Near Support Zone";
    statusColor = "#3FB950";
    StatusIcon = FaArrowDown;
  }

  return (
    <Card title="Key Levels (Classic Pivots)">
      <LadderContainer>
        <HeaderRow>
          <span style={{color: 'var(--color-text-secondary)', fontSize: '0.9rem'}}>Current Trend Position</span>
          <StatusBadge color={statusColor}>
            <StatusIcon /> {status}
          </StatusBadge>
        </HeaderRow>

        <GraphicWrapper>
          <BarBackground />
          {/* We safely check each level before rendering its marker */}
          {s1 && <LevelMarker percent={getPercent(s1)} color="#3FB950" label="S1" />}
          {pp && <LevelMarker percent={getPercent(pp)} color="#EDBB5A" label="PP" />}
          {r1 && <LevelMarker percent={getPercent(r1)} color="#F85149" label="R1" />}
          
          <CurrentPriceMarker 
            percent={getPercent(current)} 
            price={safeFixed(current, 1)} 
            currency={currency} 
          />
        </GraphicWrapper>

        <LevelsGrid>
          <LevelCard color="#F85149">
            <LevelLabel>Resistance 2</LevelLabel>
            <LevelValue>{currency}{safeFixed(r2)}</LevelValue>
          </LevelCard>
          <LevelCard color="#F85149">
            <LevelLabel>Resistance 1</LevelLabel>
            <LevelValue>{currency}{safeFixed(r1)}</LevelValue>
          </LevelCard>
          <LevelCard color="#EDBB5A">
            <LevelLabel>Pivot Point</LevelLabel>
            <LevelValue>{currency}{safeFixed(pp)}</LevelValue>
          </LevelCard>
          <LevelCard color="#3FB950">
            <LevelLabel>Support 1</LevelLabel>
            <LevelValue>{currency}{safeFixed(s1)}</LevelValue>
          </LevelCard>
          <LevelCard color="#3FB950">
            <LevelLabel>Support 2</LevelLabel>
            <LevelValue>{currency}{safeFixed(s2)}</LevelValue>
          </LevelCard>
        </LevelsGrid>

      </LadderContainer>
    </Card>
  );
};

export default PriceLevels;
```

## File: frontend/src/components/Shareholding/OwnershipTrend.js
```javascript
import React from 'react';
import styled from 'styled-components';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from 'recharts';

// --- Styled Components ---

const ChartContainer = styled.div`
  width: 100%;
  height: 400px;
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid var(--color-border);
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--color-text-primary);
`;

const CustomTooltipContainer = styled.div`
  background-color: #2a3441;
  border: 1px solid var(--color-border);
  padding: 1rem;
  border-radius: 8px;
  color: var(--color-text-primary);
`;


// --- The New, Smarter React Component ---

const OwnershipTrend = ({ historicalStatements }) => {
  // We now use the 'annual_revenue_and_profit' data (which is the income statements array)
  // as it contains the historical shares outstanding.
  if (!historicalStatements || !Array.isArray(historicalStatements) || historicalStatements.length < 2) {
    return (
      <ChartContainer>
        <SectionTitle>Shares Outstanding Trend</SectionTitle>
        <p>Historical shares data is not available for this stock.</p>
      </ChartContainer>
    );
  }

  // Helper function to format large numbers into Billions (B) or Millions (M)
  const formatLargeNumber = (num) => {
    if (!num || isNaN(num)) return 'N/A';
    if (Math.abs(num) >= 1e9) return `${(num / 1e9).toFixed(2)}B`;
    if (Math.abs(num) >= 1e6) return `${(num / 1e6).toFixed(2)}M`;
    return num.toLocaleString();
  };

  // Process the income statement data to extract the year and shares outstanding
  const chartData = historicalStatements
    .slice() // Create a copy to avoid mutating the original prop
    .reverse() // Reverse to show chronological order (oldest to newest)
    .map(item => ({
      year: item.calendarYear,
      'Shares Outstanding': item.weightedAverageShsOut,
    }));

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <CustomTooltipContainer>
          <p style={{ fontWeight: 'bold' }}>Year: {label}</p>
          <p style={{ color: 'var(--color-primary)' }}>
            Shares: {formatLargeNumber(payload[0].value)}
          </p>
        </CustomTooltipContainer>
      );
    }
    return null;
  };

  return (
    <ChartContainer>
      <SectionTitle>Shares Outstanding Trend</SectionTitle>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={chartData}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" />
          <XAxis 
            dataKey="year" 
            stroke="var(--color-text-secondary)" 
            tick={{ fill: 'var(--color-text-secondary)', fontSize: 12 }} 
          />
          <YAxis 
            stroke="var(--color-text-secondary)" 
            tickFormatter={formatLargeNumber}
            tick={{ fill: 'var(--color-text-secondary)', fontSize: 12 }}
            domain={['dataMin - 1000000', 'dataMax + 1000000']} // Add some padding
          />
          <Tooltip content={<CustomTooltip />} />
          <Area 
            type="monotone" 
            dataKey="Shares Outstanding" 
            stroke="var(--color-primary)" 
            fill="rgba(88, 166, 255, 0.2)" // A nice semi-transparent fill
            strokeWidth={2}
          />
        </AreaChart>
      </ResponsiveContainer>
    </ChartContainer>
  );
};

export default OwnershipTrend;
```

## File: frontend/src/components/Shareholding/TrendChart.js
```javascript
import React from 'react';
import styled from 'styled-components';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Cell
} from 'recharts';

// --- Styled Components ---

const ChartWrapper = styled.div`
  width: 100%;
  height: 350px;
`;

const ChartTitle = styled.h3`
  text-align: center;
  color: var(--color-text-secondary);
  font-weight: 500;
  margin-bottom: 2rem;
`;

// --- React Component ---

const TrendChart = () => {
  // --- Placeholder Data ---
  // The free API does not provide this historical data,
  // so we are using a realistic placeholder structure to build the UI.
  const placeholderData = [
    { name: 'Jun 2024', Holding: 13.27, Pledges: 0 },
    { name: 'Sep 2024', Holding: 13.25, Pledges: 0 },
    { name: 'Dec 2024', Holding: 13.25, Pledges: 0 },
    { name: 'Jun 2025', Holding: 11.74, Pledges: 0 },
    { name: 'Sep 2025', Holding: 11.73, Pledges: 0 },
  ];

  // Custom Tooltip for better styling
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div style={{
            backgroundColor: 'var(--color-secondary)',
            border: '1px solid var(--color-border)',
            padding: '10px',
            borderRadius: '5px'
        }}>
          <p>{label}</p>
          <p style={{ color: '#8884d8' }}>{`Holding: ${payload[0].value}%`}</p>
          <p style={{ color: '#82ca9d' }}>{`Pledged: ${payload[1] ? payload[1].value : '0'}%`}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <ChartWrapper>
      <ChartTitle>Promoter Holding Trend (%)</ChartTitle>
      <ResponsiveContainer>
        <BarChart
          data={placeholderData}
          margin={{ top: 5, right: 20, left: 0, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="var(--color-border)" vertical={false} />
          <XAxis 
            dataKey="name" 
            stroke="var(--color-text-secondary)" 
            tick={{ fill: 'var(--color-text-secondary)', fontSize: 12 }} 
          />
          <YAxis 
            stroke="var(--color-text-secondary)" 
            domain={[0, 15]} // Set a fixed domain for better visual consistency
            tick={{ fill: 'var(--color-text-secondary)', fontSize: 12 }} 
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(136, 132, 216, 0.1)' }} />
          
          {/* Bar for Promoter Holding */}
          <Bar dataKey="Holding" fill="#586994" barSize={30}>
            {placeholderData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.Holding < 12 ? '#FE6D73' : '#586994'} />
            ))}
          </Bar>
          
          {/* Bar for Pledged shares. It will stack on top of the Holding bar.
              Since our pledges are 0, it won't be visible, which is correct. */}
          <Bar dataKey="Pledges" stackId="a" fill="#3FB950" />
        </BarChart>
      </ResponsiveContainer>
    </ChartWrapper>
  );
};

export default TrendChart;
```

## File: frontend/src/index.js
```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Find the div with the id of 'root' in the index.html file
const rootElement = document.getElementById('root');

// Create a root for our React application to render into
const root = ReactDOM.createRoot(rootElement);

// Render the main App component
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

## File: frontend/src/pages/AuthCallback.js
```javascript
import React, { useEffect, useRef } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';
import { FaSpinner } from 'react-icons/fa';

const fadeIn = keyframes`from { opacity: 0; } to { opacity: 1; }`;

const Container = styled.div`
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: var(--color-background);
  color: var(--color-text-primary);
  animation: ${fadeIn} 0.5s ease-in;
`;

const Spinner = styled(FaSpinner)`
  font-size: 3rem;
  color: var(--color-primary);
  animation: spin 1s linear infinite;
  margin-bottom: 1.5rem;
  
  @keyframes spin { 100% { transform: rotate(360deg); } }
`;

const AuthCallback = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const processed = useRef(false);

  useEffect(() => {
    const code = searchParams.get('auth_code');
    
    if (code && !processed.current) {
        processed.current = true;
        
        // Exchange Code for Token
        axios.post('/api/auth/fyers/validate', { auth_code: code })
            .then(res => {
                const { access_token, client_id } = res.data;
                
                // Save to Local Storage (Persistent)
                localStorage.setItem('fyers_token', access_token);
                localStorage.setItem('fyers_client_id', client_id);
                
                // Redirect to Home
                setTimeout(() => navigate('/'), 1000);
            })
            .catch(err => {
                console.error("Auth Failed", err);
                alert("Login Failed. Please try again.");
                navigate('/');
            });
    } else if (!code) {
        navigate('/');
    }
  }, [searchParams, navigate]);

  return (
    <Container>
      <Spinner />
      <h2>Connecting to Fyers...</h2>
      <p style={{color: '#8B949E'}}>Securing your data feed.</p>
    </Container>
  );
};

export default AuthCallback;
```

## File: frontend/src/pages/PureVisionPage.js
```javascript
import React, { useState } from 'react';
import styled, { keyframes } from 'styled-components';
import { useLocation, useNavigate } from 'react-router-dom';
import Card from '../components/common/Card';
import { FaArrowLeft, FaRobot, FaBrain, FaDraftingCompass, FaChartArea } from 'react-icons/fa';

// --- STYLES ---
const fadeIn = keyframes`from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); }`;

const PageContainer = styled.div`
  padding: 2rem; max-width: 1400px; margin: 0 auto; animation: ${fadeIn} 0.5s ease-out;
`;

const BackBtn = styled.button`
  background: transparent; border: 1px solid var(--color-border); color: var(--color-text-secondary);
  padding: 8px 16px; border-radius: 20px; cursor: pointer; display: flex; align-items: center; gap: 8px;
  margin-bottom: 2rem; transition: all 0.2s;
  &:hover { border-color: var(--color-primary); color: #fff; }
`;

const Grid = styled.div`
  display: grid; grid-template-columns: 1fr 1fr; gap: 2rem;
  @media (max-width: 1024px) { grid-template-columns: 1fr; }
`;

const ImageCard = styled.div`
  background: var(--color-secondary); border: 1px solid var(--color-border); border-radius: 16px;
  padding: 1rem; display: flex; align-items: center; justify-content: center;
  img { max-width: 100%; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
`;

const AnalysisBox = styled.div`
  background: linear-gradient(145deg, #161B22, #0D1117); border: 1px solid var(--color-primary);
  border-radius: 16px; padding: 2rem; box-shadow: 0 0 30px rgba(88, 166, 255, 0.1);
  white-space: pre-line; line-height: 1.8; color: #C9D1D9; font-size: 1rem;
  
  strong { color: #58A6FF; font-weight: 700; }
  h1, h2, h3 { color: #fff; margin-top: 1.5rem; margin-bottom: 0.5rem; font-size: 1.2rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem; }
`;

const Header = styled.h1`
  font-size: 2rem; margin-bottom: 0.5rem; background: linear-gradient(90deg, #fff, #888); 
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
`;

const PureVisionPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { analysis, image } = location.state || {};

  if (!analysis) return <PageContainer>Loading...</PageContainer>;

  return (
    <PageContainer>
      <BackBtn onClick={() => navigate('/')}><FaArrowLeft /> Command Center</BackBtn>
      
      <div style={{marginBottom: '2rem'}}>
          <Header><FaBrain style={{color:'#58A6FF', marginRight:'10px'}}/> Quantum Vision Analysis</Header>
          <p style={{color:'var(--color-text-secondary)'}}>Pure Mathematical & Geometric Breakdown. Zero External Data.</p>
      </div>

      <Grid>
        {/* Left: The Image */}
        <ImageCard>
           {image && <img src={image} alt="Analyzed Chart" />}
        </ImageCard>

        {/* Right: The AI Brain */}
        <AnalysisBox>
            <div style={{display:'flex', alignItems:'center', gap:'10px', marginBottom:'1rem', color:'#58A6FF'}}>
                <FaDraftingCompass /> <span>GEOMETRIC ENGINE OUTPUT</span>
            </div>
            {/* Simple Markdown-like parser */}
            {analysis.split('**').map((part, i) => 
                i % 2 === 1 ? <strong key={i}>{part}</strong> : part
            )}
        </AnalysisBox>
      </Grid>
    </PageContainer>
  );
};

export default PureVisionPage;
```

## File: frontend/src/utils/FyersClientEngine.js
```javascript
export class FyersClientEngine {
    constructor(token, symbol, onTick) {
        this.token = token;
        this.symbol = symbol;
        this.onTick = onTick;
        this.socket = null;
        this.isConnected = false;
        this.lastPrice = null;
    }

    connect() {
        if (!window.FyersSocket || !this.token) return;

        this.socket = new window.FyersSocket(this.token);

        this.socket.onopen = () => {
            this.isConnected = true;
            this.subscribe();
        };

        this.socket.onmessage = (msg) => {
            try {
                const tick = msg.d?.[0] || msg[0]; 
                if (tick && tick.v && tick.v.lp) {
                    const price = parseFloat(tick.v.lp);
                    if (this.onTick) this.onTick({ price: price });
                }
            } catch (e) {}
        };

        this.socket.connect();
    }

    subscribe() {
        if (this.socket && this.isConnected) {
            this.socket.subscribe([this.symbol]); 
            this.socket.mode(this.socket.MODE_LTP);
        }
    }

    disconnect() {
        if (this.socket) {
            this.socket.close();
            this.socket = null;
        }
    }
}
```

## File: frontend/src/utils/smc_algorithms.js
```javascript
// --- SMART MONEY CONCEPTS ENGINE ---

export const calculateSMC = (data) => {
    const fvgs = [];
    const orderBlocks = [];
    const markers = [];
    const coloredCandles = []; // To override colors for FVG
    const priceLines = []; // To draw zones

    // We need at least 3 candles to find an FVG
    for (let i = 2; i < data.length; i++) {
        const curr = data[i];
        const prev = data[i-1];
        const prev2 = data[i-2];

        // --- 1. FAIR VALUE GAPS (FVG) ---
        
        // Bullish FVG: (High of Candle i-2) < (Low of Candle i)
        if (prev2.high < curr.low) {
            // Check for significant size (optional, keeps chart clean)
            const gapSize = curr.low - prev2.high;
            if (gapSize > (curr.close * 0.0005)) { // 0.05% filter
                fvgs.push({
                    type: 'Bullish FVG',
                    top: curr.low,
                    bottom: prev2.high,
                    index: i-1 // The middle candle is the FVG candle
                });
                // Color the middle candle Yellow (Imbalance)
                coloredCandles.push({ time: prev.time, color: '#FBBF24', wickColor: '#FBBF24', borderColor: '#FBBF24' });
            }
        }

        // Bearish FVG: (Low of Candle i-2) > (High of Candle i)
        if (prev2.low > curr.high) {
            const gapSize = prev2.low - curr.high;
            if (gapSize > (curr.close * 0.0005)) {
                fvgs.push({
                    type: 'Bearish FVG',
                    top: prev2.low,
                    bottom: curr.high,
                    index: i-1
                });
                // Color the middle candle Purple (Imbalance)
                coloredCandles.push({ time: prev.time, color: '#A855F7', wickColor: '#A855F7', borderColor: '#A855F7' });
            }
        }

        // --- 2. ORDER BLOCKS (Simplified) ---
        // Bullish OB: Lowest Down-candle before a strong Up-move that breaks structure
        // Logic: Current is Green, Previous was Red, Current Body engulfs Previous
        const isBullishEngulfing = curr.close > curr.open && prev.close < prev.open && curr.close > prev.open && curr.open < prev.close;
        
        if (isBullishEngulfing) {
            orderBlocks.push({ type: 'Bullish OB', price: prev.low, time: prev.time });
            markers.push({
                time: prev.time,
                position: 'belowBar',
                color: '#3FB950',
                shape: 'arrowUp',
                text: 'OB',
            });
        }

        // Bearish OB
        const isBearishEngulfing = curr.close < curr.open && prev.close > prev.open && curr.close < prev.open && curr.open > prev.close;
        
        if (isBearishEngulfing) {
            orderBlocks.push({ type: 'Bearish OB', price: prev.high, time: prev.time });
            markers.push({
                time: prev.time,
                position: 'aboveBar',
                color: '#F85149',
                shape: 'arrowDown',
                text: 'OB',
            });
        }
    }

    // --- 3. CALCULATE ACTIVE ZONES (For Price Lines) ---
    // We only take the last 2 valid FVGs to avoid clutter
    const recentFVGs = fvgs.slice(-2);
    
    recentFVGs.forEach(fvg => {
        if (fvg.type === 'Bullish FVG') {
            priceLines.push({ price: fvg.bottom, color: '#FBBF24', title: 'Demand Gap' });
        } else {
            priceLines.push({ price: fvg.top, color: '#A855F7', title: 'Supply Gap' });
        }
    });

    return { markers, coloredCandles, priceLines };
};
```

## File: generate_token.py
```python
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
```

## File: get_real_token.py
```python
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
```

## File: manual_token.py
```python
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
```

## File: requirements.txt
```

```

## File: test_api.py
```python
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
```

## File: frontend/public/index.html
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <script src="https://cdn.fyers.in/socket/v3/fyers-socket.js"></script>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      name="description"
      content="Stellar Stock Screener - AI-Powered Financial Analysis"
    />
    <link rel="apple-touch-icon" href="%PUBLIC_URL%/logo192.png" />
    <link rel="manifest" href="%PUBLIC_URL%/manifest.json" />
    
    <!-- This is where the TradingView library will be loaded from -->
    <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>

    <title>Stellar Stock Screener</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    
    <!-- THIS IS THE CRITICAL LINE -->
    <div id="root"></div>
    
  </body>
</html>
```

## File: frontend/src/components/common/Card.js
```javascript
import React from 'react';
import styled from 'styled-components';

// This is our master styled component for all content blocks.
const CardContainer = styled.div`
  background-color: var(--color-secondary);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  margin-bottom: 1.5rem; 
  width: 100%;
  
  /* Mobile: Tight padding */
  padding: 1rem; 

  /* Desktop: Luxurious padding */
  @media (min-width: 768px) {
    padding: 2rem;
    margin-bottom: 2rem;
    
  }
`;

const CardHeader = styled.div`
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border);
`;

const CardTitle = styled.h2`
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text-primary);
`;

const CardContent = styled.div`
  /* The content inside the card will be placed here */
`;

// This is a reusable React component that accepts a title and content.
const Card = ({ title, children }) => {
  return (
    <CardContainer>
      {/* The title is optional; if a title is provided, the header will render. */}
      {title && (
        <CardHeader>
          <CardTitle>{title}</CardTitle>
        </CardHeader>
      )}
      <CardContent>
        {/* 'children' is a special prop in React that lets us pass components inside other components.
            Whatever we place inside <Card>...</Card> will be rendered here. */}
        {children}
      </CardContent>
    </CardContainer>
  );
};

export default Card;
```

## File: frontend/src/components/common/Tabs/NestedTabs.js
```javascript
import React, { useState, useRef } from 'react';
import styled from 'styled-components';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa';

// --- Styled Components ---

const TabsContainer = styled.div`
  width: 100%;
  position: relative;
`;

const TabListWrapper = styled.div`
  position: relative;
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--color-border);
  margin-bottom: 2rem;
`;

const TabList = styled.div`
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
  width: 100%;
  
  &::-webkit-scrollbar {
    display: none;
  }
  -ms-overflow-style: none;
  scrollbar-width: none;
`;

const TabButton = styled.button`
  padding: 0.75rem 1.25rem;
  border: none;
  background-color: transparent;
  color: ${({ active }) => (active ? 'var(--color-primary)' : 'var(--color-text-secondary)')};
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  position: relative;
  transition: color 0.3s ease, background-color 0.3s ease;
  border-radius: 6px 6px 0 0;
  margin-bottom: -1px;
  border: 1px solid transparent;
  white-space: nowrap; /* Critical for scrolling */
  flex-shrink: 0;      /* Critical for scrolling */

  &:hover {
    background-color: var(--color-secondary);
  }

  ${({ active }) => active && `
    background-color: var(--color-secondary);
    border-color: var(--color-border) var(--color-border) transparent var(--color-border);
  `}
`;

// Reusing the same arrow logic for consistency
const ScrollButton = styled.button`
  position: absolute;
  top: 0;
  bottom: 0;
  width: 30px; /* Slightly smaller for nested tabs */
  border: none;
  cursor: pointer;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-secondary);
  font-size: 0.8rem;
  transition: opacity 0.2s;
  
  &.left {
    left: 0;
    background: linear-gradient(to right, var(--color-secondary) 40%, transparent 100%);
  }
  
  &.right {
    right: 0;
    background: linear-gradient(to left, var(--color-secondary) 40%, transparent 100%);
  }

  &:hover {
    color: var(--color-primary);
  }
`;

const TabContent = styled.div`
  padding: 1rem 0;
`;

// --- The Logic ---

const NestedTabs = ({ children }) => {
  const [activeTab, setActiveTab] = useState(children[0].props.label);
  const scrollRef = useRef(null);

  const handleClick = (e, newActiveTab) => {
    e.preventDefault();
    setActiveTab(newActiveTab);
    e.target.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
  };

  const scroll = (direction) => {
    if (scrollRef.current) {
      const { current } = scrollRef;
      const scrollAmount = 150;
      if (direction === 'left') {
        current.scrollLeft -= scrollAmount;
      } else {
        current.scrollLeft += scrollAmount;
      }
    }
  };

  return (
    <TabsContainer>
      <TabListWrapper>
        <ScrollButton className="left" onClick={() => scroll('left')}><FaChevronLeft /></ScrollButton>
        
        <TabList ref={scrollRef}>
          {children.map(child => (
            <TabButton
              key={child.props.label}
              active={activeTab === child.props.label}
              onClick={e => handleClick(e, child.props.label)}
            >
              {child.props.label}
            </TabButton>
          ))}
        </TabList>

        <ScrollButton className="right" onClick={() => scroll('right')}><FaChevronRight /></ScrollButton>
      </TabListWrapper>

      <TabContent>
        {children.map(child => {
          if (child.props.label === activeTab) {
            return <div key={child.props.label}>{child.props.children}</div>;
          }
          return null;
        })}
      </TabContent>
    </TabsContainer>
  );
};

const NestedTabPanel = ({ label, children }) => {
  return <div label={label}>{children}</div>;
};

export { NestedTabs, NestedTabPanel };
```

## File: frontend/src/components/Fundamentals/DarvasScan.js
```javascript
import React from 'react';
import styled from 'styled-components';

// --- Styled Components ---

const ScanContainer = styled.div`
  /* Main container for the Darvas Scan section */
`;

const StatusValue = styled.span`
  font-size: 2rem;
  font-weight: 700;
  /* Dynamically sets the color based on the scan result */
  color: ${({ result }) => {
    if (result === 'Pass') return 'var(--color-success)';
    if (result === 'Fail') return 'var(--color-danger)';
    return 'var(--color-primary)';
  }};
`;

const MessageText = styled.p`
  font-size: 1rem;
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin-top: 0.5rem;
`;

const BoxInfoGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-border);
`;

const BoxInfoItem = styled.div`
  background-color: var(--color-background);
  padding: 1rem;
  border-radius: 8px;
`;

const BoxLabel = styled.div`
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  margin-bottom: 0.5rem;
`;

const BoxValue = styled.div`
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text-primary);
`;

// --- Intelligent Currency Helper Function ---
const getCurrencySymbol = (currencyCode) => {
    switch (currencyCode) {
        case 'INR':
            return '₹';
        case 'USD':
            return '$';
        case 'JPY':
            return '¥';
        // Add more currencies as needed
        default:
            return '$'; // Default to dollar if currency is unknown
    }
};

// --- The Final, Corrected React Component ---

// It now accepts the 'currency' prop from its parent, Fundamentals.js
const DarvasScan = ({ scanData, currency }) => {

  // If the data from the backend is missing, show an informative message.
  if (!scanData || !scanData.status) {
    return (
      <ScanContainer>
        <p>Darvas Scan data is not available for this stock.</p>
      </ScanContainer>
    );
  }

  const { status, message, box_top, box_bottom, result } = scanData;
  
  // Get the correct currency symbol to display.
  const currencySymbol = getCurrencySymbol(currency);

  return (
    <ScanContainer>
      <StatusValue result={result}>{status}</StatusValue>
      <MessageText>{message}</MessageText>

      {/* Only show the Box Top/Bottom info if a valid box has been identified by the backend. */}
      {box_top && box_bottom && (
        <BoxInfoGrid>
          <BoxInfoItem>
            <BoxLabel>Box Top (Resistance)</BoxLabel>
            {/* --- UPDATED: Use the dynamic currency symbol --- */}
            <BoxValue>{currencySymbol}{box_top.toFixed(2)}</BoxValue>
          </BoxInfoItem>
          <BoxInfoItem>
            <BoxLabel>Box Bottom (Support)</BoxLabel>
            {/* --- UPDATED: Use the dynamic currency symbol --- */}
            <BoxValue>{currencySymbol}{box_bottom.toFixed(2)}</BoxValue>
          </BoxInfoItem>
        </BoxInfoGrid>
      )}
    </ScanContainer>
  );
};

export default DarvasScan;
```

## File: frontend/src/components/Peers/PeersComparison.js
```javascript
import React, { useState, useEffect, useMemo } from 'react';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';
import Card from '../common/Card';

// --- Styled Components ---

const fadeIn = keyframes`
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
`;

const Loader = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: var(--color-primary);
  animation: ${fadeIn} 0.5s ease-in;
`;

const TableContainer = styled.div`
  width: 100%;
  overflow-x: auto; /* Allows horizontal scrolling on small screens */
  animation: ${fadeIn} 0.5s ease-in;
`;

const StyledTable = styled.table`
  width: 100%;
  border-collapse: collapse;
  text-align: right;
`;

const TableHeader = styled.th`
  padding: 1rem;
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: 0.9rem;
  border-bottom: 1px solid var(--color-border);
  cursor: pointer;
  transition: color 0.2s ease;
  white-space: nowrap;

  &:first-child {
    text-align: left;
  }

  &:hover {
    color: var(--color-text-primary);
  }
`;

const TableRow = styled.tr`
  /* Highlight the row for the main symbol being analyzed */
background-color: ${({ $isMainSymbol }) => $isMainSymbol ? 'rgba(88, 166, 255, 0.1)' : 'transparent'};  
  &:not(:last-child) {
    border-bottom: 1px solid var(--color-border);
  }
`;

const TableCell = styled.td`
  padding: 1rem;
  font-size: 0.95rem;
  font-family: 'Roboto Mono', monospace; /* Use a monospaced font for numerical data */

  &:first-child {
    font-weight: 600;
    color: var(--color-text-primary);
    text-align: left;
    font-family: 'Inter', sans-serif; /* Use the standard font for the symbol name */
  }
`;

// --- Helper Functions to Format Data ---

const formatMarketCap = (num) => {
  if (num === null || num === undefined || isNaN(num)) return 'N/A';
  if (Math.abs(num) >= 1e12) return `${(num / 1e12).toFixed(2)}T`;
  if (Math.abs(num) >= 1e9) return `${(num / 1e9).toFixed(2)}B`;
  if (Math.abs(num) >= 1e6) return `${(num / 1e6).toFixed(2)}M`;
  return num.toLocaleString();
};

const formatPercent = (num) => {
  if (num === null || num === undefined || isNaN(num)) return 'N/A';
  return `${(num * 100).toFixed(2)}%`;
};

const formatNumber = (num) => {
  if (num === null || num === undefined || isNaN(num)) return 'N/A';
  return num.toFixed(2);
};

// --- The Definitive, Robust React Component ---

const PeersComparison = ({ symbol }) => {
  const [peersData, setPeersData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [sortConfig, setSortConfig] = useState({ key: 'marketCap', direction: 'descending' });

  useEffect(() => {
    const fetchPeersData = async () => {
      if (!symbol) {
        setIsLoading(false);
        return;
      }
      setIsLoading(true);
      try {
        const response = await axios.get(`/api/stocks/${symbol}/peers`);
        setPeersData(response.data);
      } catch (error) {
        console.error("Failed to fetch peers data:", error);
        setPeersData([]);
      } finally {
        setIsLoading(false);
      }
    };
    // Add a small delay to this lazy-loaded fetch.
    const timer = setTimeout(fetchPeersData, 300);
    return () => clearTimeout(timer);
  }, [symbol]);

  // This is the logic for sorting the table's columns.
  const sortedPeers = useMemo(() => {
    let sortableItems = [...peersData];
    if (sortConfig !== null) {
      sortableItems.sort((a, b) => {
        // This robust logic checks for both FMP's key and Yahoo's key.
        const aValue = a[sortConfig.key] || a[sortConfig.key.replace('TTM', '')] || 0;
        const bValue = b[sortConfig.key] || b[sortConfig.key.replace('TTM', '')] || 0;
        
        if (aValue < bValue) {
          return sortConfig.direction === 'ascending' ? -1 : 1;
        }
        if (aValue > bValue) {
          return sortConfig.direction === 'ascending' ? 1 : -1;
        }
        return 0;
      });
    }
    return sortableItems;
  }, [peersData, sortConfig]);

  const requestSort = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  // --- Render Logic ---

  if (isLoading) {
    return (
      <Card title="Peers Comparison">
        <Loader>Finding and analyzing peers with AI...</Loader>
      </Card>
    );
  }

  if (!peersData || peersData.length <= 1) {
    return (
      <Card title="Peers Comparison">
        <p>Peer comparison data is not available for this stock.</p>
      </Card>
    );
  }

  return (
    <Card title="Peers Comparison">
      <TableContainer>
        <StyledTable>
          <thead>
            <tr>
              <TableHeader onClick={() => requestSort('symbol')}>Symbol</TableHeader>
              <TableHeader onClick={() => requestSort('marketCap')}>Market Cap</TableHeader>
              <TableHeader onClick={() => requestSort('peRatioTTM')}>P/E Ratio (TTM)</TableHeader>
              <TableHeader onClick={() => requestSort('revenueGrowth')}>Revenue Growth</TableHeader>
              <TableHeader onClick={() => requestSort('grossMargins')}>Gross Margin</TableHeader>
            </tr>
          </thead>
          <tbody>
            {sortedPeers.map(peer => (
<TableRow key={peer.symbol} $isMainSymbol={peer.symbol === symbol}>
                <TableCell>{peer.symbol}</TableCell>
                {/* This is the ultimate robust display logic, checking for both FMP's key and Yahoo's key for every cell */}
                <TableCell>{formatMarketCap(peer.marketCapTTM || peer.marketCap)}</TableCell>
                <TableCell>{formatNumber(peer.peRatioTTM)}</TableCell>
                <TableCell>{formatPercent(peer.revenueGrowthTTM || peer.revenueGrowth)}</TableCell>
                <TableCell>{formatPercent(peer.grossProfitMarginTTM || peer.grossMargins)}</TableCell>
              </TableRow>
            ))}
          </tbody>
        </StyledTable>
      </TableContainer>
    </Card>
  );
};

export default PeersComparison;
```

## File: frontend/src/components/Technicals/MovingAverages.js
```javascript
import React from 'react';
import styled from 'styled-components';

// --- Styled Components ---

const TableContainer = styled.div`
  width: 100%;
  max-width: 300px; /* Constrain width for a compact, clean look */
  margin-left: auto; /* Push the table to the right within its grid container */
`;

const StyledTable = styled.table`
  width: 100%;
  border-collapse: collapse;
`;

const TableHeader = styled.th`
  padding: 10px;
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: 0.9rem;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
`;

const TableCell = styled.td`
  padding: 10px;
  font-size: 0.95rem;

  /* Style the period (e.g., "5 Days") cell */
  &:first-child {
    color: var(--color-text-secondary);
  }

  /* Style the calculated value cell */
  &:last-child {
    font-weight: 600;
    color: var(--color-text-primary);
    text-align: right;
    font-family: 'Roboto Mono', monospace; /* Use a monospaced font for numbers */
  }
`;

const TableRow = styled.tr`
  border-bottom: 1px solid var(--color-border);

  &:last-child {
    border-bottom: none; /* Remove the border for the last row */
  }
`;

// --- The New, Dynamic React Component ---

// The component now accepts 'maData' as a prop from its parent.
const MovingAverages = ({ maData }) => {
  // If the data is missing or empty, we show an informative message.
  if (!maData || Object.keys(maData).length === 0) {
    return (
      <TableContainer>
        <p>Moving average data is not available.</p>
      </TableContainer>
    );
  }

  // We create a structured array to ensure the rows are always in the correct order.
  const ma_periods = [
    { period: '5 Days', key: '5' },
    { period: '10 Days', key: '10' },
    { period: '20 Days', key: '20' },
    { period: '50 Days', key: '50' },
    { period: '100 Days', key: '100' },
    { period: '200 Days', key: '200' },
  ];

  return (
    <TableContainer>
      <StyledTable>
        <thead>
          <tr>
            <TableHeader>Period (SMA)</TableHeader>
            <TableHeader style={{ textAlign: 'right' }}>Value</TableHeader>
          </tr>
        </thead>
        <tbody>
          {ma_periods.map(item => {
            const value = maData[item.key];
            return (
              <TableRow key={item.period}>
                <TableCell>{item.period}</TableCell>
                {/* We check if the value is a valid number before displaying */}
                <TableCell>{typeof value === 'number' ? value.toFixed(2) : 'N/A'}</TableCell>
              </TableRow>
            );
          })}
        </tbody>
      </StyledTable>
    </TableContainer>
  );
};

export default MovingAverages;
```

## File: frontend/src/components/Technicals/PivotLevels.js
```javascript
import React from 'react';
import styled from 'styled-components';

// --- Styled Components ---

const TableContainer = styled.div`
  width: 100%;
  overflow-x: auto; /* Allows horizontal scrolling on small screens if needed */
`;

const StyledTable = styled.table`
  width: 100%;
  border-collapse: collapse;
  text-align: center;
`;

const TableHeader = styled.th`
  padding: 12px;
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: 0.9rem;
  border-bottom: 1px solid var(--color-border);
  white-space: nowrap; /* Prevents headers from wrapping */
`;

const TableCell = styled.td`
  padding: 12px;
  font-size: 0.95rem;
  font-family: 'Roboto Mono', monospace; /* Use a monospaced font for numbers */
  border-bottom: 1px solid var(--color-border);

  /* Style the 'Type' column differently */
  &:first-child {
    font-weight: 600;
    color: var(--color-text-primary);
    text-align: left;
    font-family: 'Inter', sans-serif;
  }
`;

const TableRow = styled.tr`
  /* A subtle hover effect for better user experience */
  &:hover {
    background-color: rgba(48, 54, 61, 0.5);
  }

  /* Remove bottom border for the very last row */
  &:last-child > td {
      border-bottom: none;
  }
`;

// --- The New, Dynamic React Component ---

// The component now accepts 'pivotData' as a prop from its parent.
const PivotLevels = ({ pivotData }) => {
  // If the data is missing or empty, we show an informative message.
  if (!pivotData || Object.keys(pivotData).length === 0) {
    return (
      <TableContainer>
        <p>Pivot point data is not available.</p>
      </TableContainer>
    );
  }

  // We dynamically create our rows from the keys in the 'pivotData' object
  // that our new backend provides (e.g., "classic", "fibonacci", "camarilla").
  const pivotRows = [
    { type: 'Classic', data: pivotData.classic },
    { type: 'Fibonacci', data: pivotData.fibonacci },
    { type: 'Camarilla', data: pivotData.camarilla },
  ];

  return (
    <TableContainer>
      <StyledTable>
        <thead>
          <tr>
            <TableHeader>Type</TableHeader>
            <TableHeader>R3</TableHeader>
            <TableHeader>R2</TableHeader>
            <TableHeader>R1</TableHeader>
            <TableHeader>Pivot Point (PP)</TableHeader>
            <TableHeader>S1</TableHeader>
            <TableHeader>S2</TableHeader>
            <TableHeader>S3</TableHeader>
          </tr>
        </thead>
        <tbody>
          {pivotRows.map(row => {
            const { type, data } = row;
            // A safety check: Don't render a row if its specific data is missing
            if (!data) return null;
            
            return (
              <TableRow key={type}>
                <TableCell>{type}</TableCell>
                {/* We use optional chaining (?.) and the nullish coalescing operator (??) 
                    for maximum safety. This prevents crashes if a value is null or undefined. */}
                <TableCell>{data.r3?.toFixed(2) ?? 'N/A'}</TableCell>
                <TableCell>{data.r2?.toFixed(2) ?? 'N/A'}</TableCell>
                <TableCell>{data.r1?.toFixed(2) ?? 'N/A'}</TableCell>
                <TableCell>{data.pp?.toFixed(2) ?? 'N/A'}</TableCell>
                <TableCell>{data.s1?.toFixed(2) ?? 'N/A'}</TableCell>
                <TableCell>{data.s2?.toFixed(2) ?? 'N/A'}</TableCell>
                <TableCell>{data.s3?.toFixed(2) ?? 'N/A'}</TableCell>
              </TableRow>
            );
          })}
        </tbody>
      </StyledTable>
    </TableContainer>
  );
};

export default PivotLevels;
```

## File: frontend/src/components/Technicals/TechnicalIndicatorsTable.js
```javascript
import React from 'react';
import styled, { keyframes } from 'styled-components';

// --- Styled Components & Animations ---

const fadeInRow = keyframes`
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const TableContainer = styled.div`
  width: 100%;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--color-border);
`;

const StyledTable = styled.table`
  width: 100%;
  border-collapse: collapse;
`;

const TableHeader = styled.th`
  padding: 12px;
  color: var(--color-text-secondary);
  font-weight: 500;
  font-size: 0.9rem;
  text-align: left;
  
  &:nth-child(2) {
    text-align: right;
  }
  &:last-child {
    text-align: right;
  }
`;

const TableRow = styled.tr`
  opacity: 0; /* Start hidden for animation */
  animation: ${fadeInRow} 0.5s ease-out forwards;
  /* Stagger the animation for each row for a beautiful effect */
  animation-delay: ${({ delay }) => delay * 0.05}s;
  
  &:not(:last-child) {
    border-bottom: 1px solid var(--color-border);
  }
`;

const TableCell = styled.td`
  padding: 14px 12px;
  font-size: 0.95rem;
  font-weight: 500;
  white-space: pre-wrap; /* Allows the multiline content for Bollinger Bands */

  &:first-child {
    font-weight: 600;
    color: var(--color-text-primary);
  }
  
  &:nth-child(2) {
    text-align: right;
    font-family: 'Roboto Mono', monospace;
  }

  &:last-child {
    text-align: right;
    font-weight: 700;
  }
`;

const Indication = styled.span`
  color: ${({ type }) => {
    switch (type) {
      case 'Bullish':
      case 'Oversold':
        return 'var(--color-success)';
      case 'Bearish':
      case 'Overbought':
        return 'var(--color-danger)';
      default:
        return 'var(--color-text-secondary)';
    }
  }};
`;

// --- The Corrected React Component ---

const TechnicalIndicatorsTable = ({ indicators }) => {
  if (!indicators || Object.keys(indicators).length === 0) {
    return (
      <TableContainer>
        <p>Technical indicator data is not available.</p>
      </TableContainer>
    );
  }

  // --- THIS IS THE CRITICAL FIX FOR BOLLINGER BANDS ---
  // We now safely access the nested 'bollingerBands' object, providing an empty object as a fallback.
  const bb = indicators.bollingerBands || {};

  const indicatorList = [
    { name: 'RSI(14)', level: indicators.rsi, indication: indicators.rsi < 30 ? 'Oversold' : indicators.rsi > 70 ? 'Overbought' : (indicators.rsi < 50 ? 'Bearish' : 'Bullish') },
    { name: 'MACD(12,26,9)', level: indicators.macd, indication: indicators.macd > indicators.macdsignal ? 'Bullish' : 'Bearish' },
    { name: 'Stochastic(14,3)', level: indicators.stochasticsk, indication: indicators.stochasticsk < 20 ? 'Oversold' : indicators.stochasticsk > 80 ? 'Overbought' : 'Neutral' },
    { name: 'ADX(14)', level: indicators.adx, indication: indicators.adx > 25 ? 'Strong Trend' : 'Weak Trend' },
    { name: 'Williams %R(14)', level: indicators.williamsr, indication: indicators.williamsr < -80 ? 'Oversold' : indicators.williamsr > -20 ? 'Overbought' : 'Neutral' },
    { name: 'ATR(14)', level: indicators.atr, indication: 'Volatility' },
    // We now correctly and safely access the properties from our 'bb' object.
    { name: 'Bollinger Band(20,2)', level: `UB: ${bb.upperBand?.toFixed(2) ?? 'N/A'}\nLB: ${bb.lowerBand?.toFixed(2) ?? 'N/A'}\nSMA: ${bb.middleBand?.toFixed(2) ?? 'N/A'}`, indication: '--' },
  ];
  
  return (
    <TableContainer>
      <StyledTable>
        <thead>
          <tr>
            <TableHeader>Indicator</TableHeader>
            <TableHeader>Level</TableHeader>
            <TableHeader>Indication</TableHeader>
          </tr>
        </thead>
        <tbody>
          {indicatorList.map((item, index) => (
            <TableRow key={item.name} delay={index}>
              <TableCell>{item.name}</TableCell>
              <TableCell>{typeof item.level === 'number' ? item.level.toFixed(2) : item.level}</TableCell>
              <TableCell>
                <Indication type={item.indication}>
                  {item.indication}
                </Indication>
              </TableCell>
            </TableRow>
          ))}
        </tbody>
      </StyledTable>
    </TableContainer>
  );
};

export default TechnicalIndicatorsTable;
```

## File: frontend/src/styles/GlobalStyles.js
```javascript
import { createGlobalStyle } from 'styled-components';

export const GlobalStyles = createGlobalStyle`
  /* CSS Variables for our color palette */
  :root {
    --color-background: #0D1117;       /* Deep, dark blue-grey (like GitHub) */
    --color-primary: #58A6FF;          /* A vibrant, accessible blue */
    --color-secondary: #161B22;       /* Slightly lighter background for cards/containers */
    --color-text-primary: #C9D1D9;     /* Light grey for primary text */
    --color-text-secondary: #8B949E;   /* Darker grey for secondary text/labels */
    --color-border: #30363D;          /* Border color */
    --color-success: #3FB950;          /* Green for positive changes */
    --color-danger: #F85149;           /* Red for negative changes */
    --font-family-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  }

  /* Resetting default styles */
  *,
  *::before,
  *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  html {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    /* Mobile First: Slightly smaller base size */
    font-size: 14px; 
    
    /* Tablet & Desktop: Scale up */
    @media (min-width: 768px) {
      font-size: 16px;
    }
  }

  body {
    background-color: var(--color-background);
    color: var(--color-text-primary);
    font-family: var(--font-family-sans);
    line-height: 1.5;
  }

  h1, h2, h3, h4, h5, h6 {
    color: var(--color-text-primary);
    font-weight: 600;
  }

  a {
    color: var(--color-primary);
    text-decoration: none;
  }

  /* Custom scrollbar for a more modern look */
  ::-webkit-scrollbar {
    width: 8px;
  }
  ::-webkit-scrollbar-track {
    background: var(--color-secondary);
  }
  ::-webkit-scrollbar-thumb {
    background: #4A5568; /* A neutral grey */
    border-radius: 4px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: #718096;
  }
`;
```

## File: backend/app/services/sentiment_service.py
```python
def calculate_technical_sentiment(technicals: dict):
    """
    Helper function to calculate technical score (0-100) and label
    based on RSI and MACD.
    """
    # --- CRASH GUARD 1: Input Validation ---
    if not technicals or not isinstance(technicals, dict):
        return {"score": 50, "label": "Neutral"}

    rsi = technicals.get('rsi')
    macd = technicals.get('macd')
    macd_signal = technicals.get('macdsignal')
    
    # --- RSI Score (Momentum) ---
    rsi_score = 50
    if rsi is not None:
        if rsi > 70: rsi_score = 85      # Overbought (Strong Momentum)
        elif rsi > 60: rsi_score = 75    # Bullish
        elif rsi > 50: rsi_score = 60    # Mild Bullish
        elif rsi < 30: rsi_score = 35    # Oversold (Weak)
        elif rsi < 40: rsi_score = 40    # Bearish
        else: rsi_score = 45             # Neutral/Weak
        
    # --- MACD Score (Trend) ---
    macd_score = 50
    if macd is not None and macd_signal is not None:
        if macd > macd_signal: 
            macd_score = 80 # Bullish Trend
        else: 
            macd_score = 20 # Bearish Trend
        
    # Combine (Equal Weight)
    t_score = (rsi_score + macd_score) / 2
    
    # Determine Label
    label = "Neutral"
    if t_score >= 60: label = "Bullish"
    elif t_score <= 40: label = "Bearish"
    
    return {"score": t_score, "label": label}


def calculate_overall_sentiment(piotroski_score: int, key_metrics: dict, technicals: dict, analyst_ratings: list):
    """
    Calculates unified sentiment.
    
    CRITICAL FIX: This function now strictly enforces input types.
    If 'key_metrics' comes in as a list (which happens for Commodities/Crypto), 
    it is converted to an empty dict to prevent 'AttributeError'.
    """
    scores = {}
    breakdown = {}

    # --- CRASH GUARD 2: Type Sanitization ---
    # This prevents the specific crash you saw in the screenshot.
    if not isinstance(key_metrics, dict):
        key_metrics = {}
    
    if not isinstance(technicals, dict):
        technicals = {}
        
    if not isinstance(analyst_ratings, list):
        analyst_ratings = []

    # --- 1. FUNDAMENTAL HEALTH (Piotroski) ---
    f_score = 50 # Default neutral
    if piotroski_score is not None:
        # Map 0-9 scale to 0-100
        f_score = (piotroski_score / 9) * 100
    
    scores['fundamental'] = f_score
    breakdown['fundamental'] = {
        "score": f_score,
        "label": "Strong" if f_score > 70 else "Weak" if f_score < 40 else "Stable"
    }

    # --- 2. FINANCIAL PERFORMANCE (Valuation & Efficiency) ---
    # Safe .get() calls on the now-guaranteed dictionary
    pe = key_metrics.get('peRatioTTM')
    roe = key_metrics.get('returnOnCapitalEmployedTTM')

    # Valuation Score
    val_score = 50
    if pe is not None and pe > 0:
        if pe < 15: val_score = 100  # Undervalued
        elif pe < 25: val_score = 75 # Fair
        elif pe < 40: val_score = 40 # Expensive
        else: val_score = 20         # Very Expensive
    
    # Efficiency Score
    eff_score = 50
    if roe is not None:
        if roe > 0.20: eff_score = 100 # Excellent
        elif roe > 0.12: eff_score = 75 # Good
        elif roe > 0.05: eff_score = 50 # Average
        else: eff_score = 25 # Poor

    # Weighted Score (only if data exists)
    fin_score = 50
    if pe is not None or roe is not None:
        fin_score = (val_score * 0.6) + (eff_score * 0.4)
    
    scores['financial'] = fin_score
    breakdown['financial'] = {
        "score": fin_score,
        "label": "Undervalued" if val_score > 70 else "Overvalued" if val_score < 40 else "Fair Value"
    }

    # --- 3. ANALYST CONSENSUS ---
    a_score = 50
    if analyst_ratings and len(analyst_ratings) > 0:
        latest = analyst_ratings[0]
        # Ensure 'latest' is a dict before accessing
        if isinstance(latest, dict):
            total_votes = (
                latest.get('ratingStrongBuy', 0) + 
                latest.get('ratingBuy', 0) + 
                latest.get('ratingHold', 0) + 
                latest.get('ratingSell', 0) + 
                latest.get('ratingStrongSell', 0)
            )
            
            if total_votes > 0:
                weighted_sum = (
                    (latest.get('ratingStrongBuy', 0) * 100) + 
                    (latest.get('ratingBuy', 0) * 75) + 
                    (latest.get('ratingHold', 0) * 50) + 
                    (latest.get('ratingSell', 0) * 25)
                )
                a_score = weighted_sum / total_votes
            
    scores['analyst'] = a_score
    breakdown['analyst'] = {
        "score": a_score,
        "label": "Buy" if a_score > 60 else "Sell" if a_score < 40 else "Hold"
    }

    # --- 4. TECHNICAL MOMENTUM ---
    tech_data = calculate_technical_sentiment(technicals)
    scores['technical'] = tech_data['score']
    breakdown['technical'] = tech_data

    # --- FINAL CALCULATION ---
    total_score = (scores['fundamental'] + scores['financial'] + scores['analyst'] + scores['technical']) / 4

    verdict = "Neutral"
    if total_score >= 75: verdict = "Strong Buy"
    elif total_score >= 60: verdict = "Buy"
    elif total_score <= 25: verdict = "Strong Sell"
    elif total_score <= 40: verdict = "Sell"

    return {
        "score": total_score, 
        "verdict": verdict,
        "breakdown": breakdown
    }
```

## File: backend/worker.py
```python
import asyncio
import os
import sys
import logging
from dotenv import load_dotenv

# Ensure import path is correct
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load Env
load_dotenv()

# Force Unbuffered Output (So logs appear in Railway instantly)
os.environ["PYTHONUNBUFFERED"] = "1"

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Worker")

# Import Services
from backend.app.services.stream_hub import producer
from backend.app.services.redis_service import redis_client

async def run_worker():
    print("==================================================")
    print("👷 TICKER WORKER STARTING (High-Speed Mode)")
    print("==================================================")
    
    # 1. Test Redis Connection Explicitly
    print("🔍 Testing Redis Connection...")
    try:
        # We assume redis_client handles the connection logic
        # Just triggering a dummy publish to verify connectivity
        await redis_client.publish_update("HEARTBEAT", {"status": "alive"})
        print("✅ Redis Pub/Sub is ACTIVE.")
    except Exception as e:
        print(f"❌ Redis Connection FAILED: {e}")
        return # Exit if Redis is dead

    # 2. Start the Data Producer
    print("🚀 Launching Data Producer Engine...")
    await producer.start()

    # 3. Keep Alive Loop
    counter = 0
    while True:
        await asyncio.sleep(10)
        counter += 10
        if counter % 60 == 0:
            print(f"💓 Worker is alive and processing ({counter}s uptime)...")

if __name__ == "__main__":
    try:
        asyncio.run(run_worker())
    except KeyboardInterrupt:
        print("🛑 Worker shutting down.")
    except Exception as e:
        print(f"❌ Worker Fatal Error: {e}")
```

## File: frontend/src/components/Forecasts/PriceTarget.js
```javascript
import React from 'react';
import styled from 'styled-components';
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine, Label
} from 'recharts';

const PriceTargetContainer = styled.div`
  width: 100%;
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--color-text-primary);
`;

const PriceDisplay = styled.div`
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
`;

const PriceChange = styled.div`
  font-size: 1rem;
  font-weight: 500;
  color: ${({ isPositive }) => (isPositive ? 'var(--color-success)' : 'var(--color-danger)')};
  margin-bottom: 1rem;
`;

const SummaryText = styled.p`
  color: var(--color-text-secondary);
  line-height: 1.6;
  max-width: 400px;
  margin-bottom: 2rem;
`;

const ChartWrapper = styled.div`
  height: 400px;
  width: 100%;
`;

const getCurrencySymbol = (currencyCode) => {
    switch (currencyCode) {
        case 'INR': return '₹';
        case 'USD': return '$';
        case 'JPY': return '¥';
        default: return '$'; 
    }
};

// **CRITICAL FIX**: Crash-proof number formatter
const safeFixed = (val, decimals = 2) => {
  if (val === undefined || val === null || isNaN(val)) return 'N/A';
  return val.toFixed(decimals);
};

const PriceTarget = ({ consensus, quote, currency }) => {

  // **CRITICAL FIX**: Validate numeric data before rendering
  if (!consensus || !quote || typeof consensus.targetConsensus !== 'number' || typeof quote.price !== 'number') {
    return (
      <PriceTargetContainer>
        <SectionTitle>Price Target</SectionTitle>
        <p style={{color: 'var(--color-text-secondary)'}}>Price target data is not available for this stock.</p>
      </PriceTargetContainer>
    );
  }
  
  const currencySymbol = getCurrencySymbol(currency);
  const { targetHigh, targetLow, targetConsensus } = consensus;
  const currentPrice = quote.price;

  const change = targetConsensus - currentPrice;
  const changePercent = (change / currentPrice) * 100;
  const isPositive = change >= 0;

  const chartData = [
    { name: 'Current', value: currentPrice },
    { name: '1Y Forecast', value: targetConsensus },
  ];
  
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div style={{
          backgroundColor: 'var(--color-secondary)',
          border: '1px solid var(--color-border)',
          padding: '1rem',
          borderRadius: '8px'
        }}>
          <p>{`${label}: ${currencySymbol}${safeFixed(payload[0].value)}`}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <PriceTargetContainer>
      <SectionTitle>Price Target</SectionTitle>
      
      <PriceDisplay>{currencySymbol}{safeFixed(targetConsensus)}</PriceDisplay>
      <PriceChange isPositive={isPositive}>
          {isPositive ? '+' : ''}{currencySymbol}{safeFixed(change)} ({isPositive ? '+' : ''}{safeFixed(changePercent)}%)
      </PriceChange>
      <SummaryText>
        The analysts offering 1-year price forecasts have a max estimate of {currencySymbol}{safeFixed(targetHigh)} and a min estimate of {currencySymbol}{safeFixed(targetLow)}.
      </SummaryText>

      <ChartWrapper>
        <ResponsiveContainer>
          <LineChart data={chartData} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
            <XAxis dataKey="name" stroke="var(--color-text-secondary)" tick={{ fill: 'var(--color-text-secondary)' }} />
            <YAxis 
                stroke="var(--color-text-secondary)" 
                domain={['auto', 'auto']}
                tick={{ fill: 'var(--color-text-secondary)' }}
                tickFormatter={(tick) => `${currencySymbol}${tick}`}
            />
            <Tooltip content={<CustomTooltip />} />
            
            <Line type="monotone" dataKey="value" stroke="var(--color-primary)" strokeWidth={2} dot={{ r: 4 }} />

            {/* Only render lines if data exists */}
            {targetHigh && (
                <ReferenceLine y={targetHigh} stroke="var(--color-success)" strokeDasharray="3 3">
                    <Label value={`Max: ${currencySymbol}${safeFixed(targetHigh)}`} position="right" fill="var(--color-success)" />
                </ReferenceLine>
            )}
            {targetLow && (
                <ReferenceLine y={targetLow} stroke="var(--color-danger)" strokeDasharray="3 3">
                    <Label value={`Min: ${currencySymbol}${safeFixed(targetLow)}`} position="right" fill="var(--color-danger)" />
                </ReferenceLine>
            )}
            <ReferenceLine y={targetConsensus} stroke="var(--color-primary)" strokeDasharray="3 3">
                <Label value={`Avg: ${currencySymbol}${safeFixed(targetConsensus)}`} position="right" fill="var(--color-primary)" />
            </ReferenceLine>
            <ReferenceLine y={currentPrice} stroke="#fff" strokeDasharray="1 1">
                <Label value={`Current: ${currencySymbol}${safeFixed(currentPrice)}`} position="left" fill="#fff" />
            </ReferenceLine>
            
          </LineChart>
        </ResponsiveContainer>
      </ChartWrapper>
    </PriceTargetContainer>
  );
};

export default PriceTarget;
```

## File: frontend/src/components/Sentiment/OverallSentiment.js
```javascript
import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import GaugeChart from 'react-gauge-chart';
import Card from '../common/Card';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { FaClock, FaSync } from 'react-icons/fa';

// --- STYLED COMPONENTS ---

const DashboardContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const MainMeterWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
`;

const SubMetersGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr; /* Stack vertically on mobile */
    gap: 1.5rem;
  }
`;

const SubMeterItem = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: var(--color-background);
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid var(--color-border);
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  transition: transform 0.2s ease, border-color 0.2s ease;
  position: relative;
  overflow: hidden; /* Contains the loading overlay */

  &:hover {
    transform: translateY(-2px);
    border-color: var(--color-primary);
  }
`;

const MeterHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 0.5rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid rgba(255,255,255,0.05);
`;

const MeterTitle = styled.h4`
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0;
`;

// --- NEW DROPDOWN STYLE ---
const TimeframeSelect = styled.select`
  background: rgba(255,255,255,0.1);
  border: 1px solid transparent;
  border-radius: 4px;
  color: var(--color-text-primary);
  font-size: 0.7rem;
  padding: 2px 6px;
  cursor: pointer;
  outline: none;
  font-weight: 600;
  transition: all 0.2s;

  &:hover {
    background: var(--color-primary);
    color: white;
  }
  
  &:focus {
    border-color: var(--color-primary);
  }

  option {
    background: #1C2128;
    color: white;
  }
`;

const VerdictText = styled.div`
  font-size: 1.8rem;
  font-weight: 800;
  text-align: center;
  margin-top: -30px;
  color: ${({ color }) => color};
  text-shadow: 0 0 15px ${({ color }) => color}44;
`;

const SubVerdictText = styled.div`
  font-size: 1.1rem;
  font-weight: 700;
  text-align: center;
  margin-top: -15px;
  color: ${({ color }) => color};
`;

const ScoreText = styled.div`
  font-size: 0.85rem;
  font-weight: 500;
  text-align: center;
  color: var(--color-text-secondary);
  margin-top: 5px;
`;

const LoadingOverlay = styled.div`
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(13, 17, 23, 0.85);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  z-index: 10;
  color: var(--color-primary);
  font-size: 1.5rem;
  backdrop-filter: blur(2px);
  animation: fadeIn 0.2s ease-in;

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  svg {
    animation: spin 1s linear infinite;
    margin-bottom: 0.5rem;
  }
  
  span {
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--color-text-primary);
  }
`;

// --- Helper for Colors ---
const getColor = (score) => {
  if (score >= 75) return 'var(--color-success)'; // Strong Buy
  if (score >= 60) return '#34D399'; // Buy
  if (score <= 25) return 'var(--color-danger)'; // Strong Sell
  if (score <= 40) return '#F87171'; // Sell
  return '#EDBB5A'; // Neutral
};

// --- Reusable Gauge Component ---
const CustomGauge = ({ id, score, label, size = "small" }) => {
  const color = getColor(score);
  const percent = Math.min(Math.max(score / 100, 0), 1); // Clamp 0-1
  
  return (
    <div style={{ width: '100%', maxWidth: size === 'large' ? '350px' : '200px' }}>
      <GaugeChart
        id={id}
        nrOfLevels={20}
        colors={['#F85149', '#F88149', '#EDBB5A', '#3FB950', '#17C3B2']}
        percent={percent}
        arcPadding={0.02}
        cornerRadius={3}
        textColor={'transparent'}
        needleBaseColor={'#FFFFFF'}
        needleColor={'#C9D1D9'}
        animate={true}
        animDelay={300}
        style={{ width: '100%' }}
      />
      {size === 'large' ? (
        <VerdictText color={color}>{label}</VerdictText>
      ) : (
        <SubVerdictText color={color}>{label}</SubVerdictText>
      )}
      <ScoreText>{score.toFixed(0)} / 100</ScoreText>
    </div>
  );
};

// --- MAIN COMPONENT ---

const OverallSentiment = ({ sentimentData }) => {
  const { symbol } = useParams();
  
  // Local state for Interactive Technical Meter
  const [techTimeframe, setTechTimeframe] = useState('1d'); // Default to Daily to match main load
  const [techData, setTechData] = useState(null);
  const [isUpdating, setIsUpdating] = useState(false);

  // Initialize techData from the main sentimentData prop when it loads
  useEffect(() => {
    if (sentimentData?.breakdown?.technical) {
      setTechData(sentimentData.breakdown.technical);
    }
  }, [sentimentData]);

  // Handler for Timeframe Change
  const handleTimeframeChange = async (e) => {
    const newTf = e.target.value;
    setTechTimeframe(newTf);
    setIsUpdating(true);

    try {
      // Call the specific endpoint for technical scoring
      const response = await axios.post(`/api/stocks/${symbol}/technical-score`, {
        timeframe: newTf
      });
      setTechData(response.data);
    } catch (err) {
      console.error("Failed to update technical score", err);
    } finally {
      setIsUpdating(false);
    }
  };

  if (!sentimentData) {
    return (
      <Card title="Confidence Matrix">
        <p style={{color: 'var(--color-text-secondary)', padding: '1rem', textAlign: 'center'}}>
            Calculating market sentiment...
        </p>
      </Card>
    );
  }

  const { score, verdict, breakdown } = sentimentData;
  
  // Fallback defaults if breakdown is missing
  const bd = breakdown || {
      fundamental: { score: 50, label: '--' },
      financial: { score: 50, label: '--' },
      technical: { score: 50, label: '--' }
  };

  // Determine which Technical Data to show (Live vs Prop)
  const currentTech = techData || bd.technical;

  return (
    <Card title="Confidence Matrix">
      <DashboardContainer>
        
        {/* --- TOP: MAIN OVERALL METER --- */}
        <MainMeterWrapper>
          <MeterTitle style={{fontSize: '1rem', marginBottom: '1rem', opacity: 0.8}}>
            Overall Health Score
          </MeterTitle>
          <CustomGauge 
            id="overall-gauge" 
            score={score} 
            label={verdict} 
            size="large" 
          />
        </MainMeterWrapper>

        {/* --- BOTTOM: 3 SUB-METERS GRID --- */}
        <SubMetersGrid>
          
          {/* 1. TECHNICAL METER (Interactive) */}
          <SubMeterItem>
            {isUpdating && (
                <LoadingOverlay>
                    <FaSync />
                    <span>Analyzing...</span>
                </LoadingOverlay>
            )}
            <MeterHeader>
                <MeterTitle>Technical</MeterTitle>
                <TimeframeSelect value={techTimeframe} onChange={handleTimeframeChange}>
                    <option value="15m">15M</option>
                    <option value="1h">1H</option>
                    <option value="4h">4H</option>
                    <option value="1d">1D</option>
                    <option value="1wk">1W</option>
                </TimeframeSelect>
            </MeterHeader>
            <CustomGauge 
                id="tech-gauge" 
                score={currentTech.score} 
                label={currentTech.label} 
            />
          </SubMeterItem>

          {/* 2. FINANCIAL METER (Static) */}
          <SubMeterItem>
            <MeterHeader>
                <MeterTitle>Financial</MeterTitle>
            </MeterHeader>
            <CustomGauge 
                id="fin-gauge" 
                score={bd.financial.score} 
                label={bd.financial.label} 
            />
          </SubMeterItem>

          {/* 3. FUNDAMENTAL METER (Static) */}
          <SubMeterItem>
            <MeterHeader>
                <MeterTitle>Fundamental</MeterTitle>
            </MeterHeader>
            <CustomGauge 
                id="fund-gauge" 
                score={bd.fundamental.score} 
                label={bd.fundamental.label} 
            />
          </SubMeterItem>

        </SubMetersGrid>

      </DashboardContainer>
    </Card>
  );
};

export default OverallSentiment;
```

## File: frontend/src/components/Shareholding/Shareholding.js
```javascript
import React from 'react';
import styled from 'styled-components';
import Card from '../common/Card';
import DonutChart from './DonutChart';
import TrendChart from './TrendChart';
import OwnershipTrend from './OwnershipTrend';

// --- Styled Components ---

const GridContainer = styled.div`
  display: grid;
  /* Create two columns of equal width */
  grid-template-columns: 1fr 1fr; 
  gap: 2rem; /* Space between the two charts */
  align-items: center; /* Vertically align the content */
  
  /* On smaller screens, stack the charts on top of each other */
  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
  }
`;

const ChartContainer = styled.div`
  width: 100%;
`;

const SectionTitle = styled.h3`
    font-size: 1.2rem;
    font-weight: 500;
    color: var(--color-text-secondary);
    text-align: center;
    margin-bottom: 2rem;
`;

// --- The Upgraded React Component ---

// It now accepts 'historicalStatements' instead of 'historicalOwnership'
const Shareholding = ({ shareholdingData, historicalStatements, shareholdingBreakdown }) => {

  // Defensive check: If there's no current shareholding data, show a message.
  if (!shareholdingData || !Array.isArray(shareholdingData) || shareholdingData.length === 0) {
    return (
      <Card title="Shareholding">
        <p>Shareholding data is not available for this stock.</p>
      </Card>
    );
  }

  return (
    <Card title="Shareholding">
      {/* --- This top section for summary charts is unchanged --- */}
      <GridContainer>
        <ChartContainer>
          <SectionTitle>Summary</SectionTitle>
          <DonutChart breakdown={shareholdingBreakdown} />

        </ChartContainer>
        <ChartContainer>
           <TrendChart />
        </ChartContainer>
      </GridContainer>

      {/* --- THIS IS THE UPDATED PART --- */}
      {/* We now pass the 'historicalStatements' prop to our new OwnershipTrend component. */}
      {/* This component will now render the Shares Outstanding trend chart. */}
      <OwnershipTrend historicalStatements={historicalStatements} />

    </Card>
  );
};

export default Shareholding;
```

## File: frontend/src/components/Technicals/RatingDial.js
```javascript
import React from 'react';
import styled from 'styled-components';
import GaugeChart from 'react-gauge-chart';

// --- Styled Components (No changes here) ---

const DialContainer = styled.div`
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
`;

const RatingText = styled.div`
  font-size: 2rem;
  font-weight: 700;
  text-align: center;
  margin-top: -30px;
  color: ${({ $ratingColor }) => $ratingColor};
`;

// --- The React Component (Logic is now more robust) ---

const RatingDial = ({ rating }) => {
  const getRatingDetails = () => {
    // --- THIS IS THE CRITICAL FIX ---
    // We add a "guard clause". If the rating prop is missing or not a string,
    // we default to a Neutral state immediately. This prevents the .toLowerCase() error.
    if (!rating || typeof rating !== 'string') {
      return { percent: 0.5, color: 'var(--color-text-secondary)', text: 'Neutral' };
    }

    // The rest of the logic remains the same
    switch (rating.toLowerCase()) {
      case 'strong buy':
      case 'bullish':
      case 'very bullish':
        return { percent: 0.9, color: 'var(--color-success)', text: 'Strong Buy' };
      case 'buy':
      case 'outperform':
        return { percent: 0.7, color: 'var(--color-success)', text: 'Buy' };
      case 'hold':
      case 'neutral':
        return { percent: 0.5, color: '#EDBB5A', text: 'Hold' };
      case 'sell':
      case 'underperform':
        return { percent: 0.3, color: 'var(--color-danger)', text: 'Sell' };
      case 'strong sell':
      case 'bearish':
        return { percent: 0.1, color: 'var(--color-danger)', text: 'Strong Sell' };
      default:
        return { percent: 0.5, color: 'var(--color-text-secondary)', text: 'Neutral' };
    }
  };

  const { percent, color, text } = getRatingDetails();

  return (
    <DialContainer>
      <GaugeChart
        id="technical-rating-gauge"
        nrOfLevels={30}
        colors={['#F85149', '#EDBB5A', '#3FB950']}
        arcWidth={0.3}
        percent={percent}
        textColor={'transparent'}
        needleBaseColor={'#FFFFFF'}
        needleColor={'#C9D1D9'}
        animate={true}
        animDelay={500}
      />
        <RatingText $ratingColor={color}>
        {text}
      </RatingText>
    </DialContainer>
  );
};

export default RatingDial;
```

## File: backend/app/services/fundamental_service.py
```python
import pandas as pd

def calculate_piotroski_f_score(income_statements, balance_sheets, cash_flow_statements):
    """
    Calculates the Piotroski F-Score (0-9) to assess financial strength.
    Uses Pandas to ensure chronological accuracy.
    """
    score = 0
    criteria_met = []

    # 1. Validation: We need at least 2 years of data to compare trends
    if not income_statements or not balance_sheets or not cash_flow_statements:
        return {"score": 0, "criteria": ["Insufficient Data"]}
    
    if len(income_statements) < 2 or len(balance_sheets) < 2 or len(cash_flow_statements) < 2:
        return {"score": 0, "criteria": ["Insufficient Historical Data (Need 2+ years)"]}

    try:
        # 2. Data Preparation: Convert to DataFrames and Sort Chronologically
        # EODHD/FMP usually send Newest First. We sort by date ASCENDING.
        # Index -1 = Current Year, Index -2 = Previous Year
        inc_df = pd.DataFrame(income_statements).sort_values('date')
        bal_df = pd.DataFrame(balance_sheets).sort_values('date')
        cf_df = pd.DataFrame(cash_flow_statements).sort_values('date')

        # Align lengths (take the minimum common length to avoid index errors)
        min_len = min(len(inc_df), len(bal_df), len(cf_df))
        inc_df = inc_df.tail(min_len)
        bal_df = bal_df.tail(min_len)
        cf_df = cf_df.tail(min_len)

        cy = -1 # Current Year Index
        py = -2 # Previous Year Index

        # --- PROFITABILITY (4 Points) ---

        # 1. Return on Assets (ROA) > 0
        # Net Income / Total Assets
        net_income = float(inc_df.iloc[cy].get('netIncome', 0))
        total_assets = float(bal_df.iloc[cy].get('totalAssets', 1)) # Avoid div/0
        roa_current = net_income / total_assets
        if net_income > 0:
            score += 1
            criteria_met.append("Positive Net Income")

        # 2. Operating Cash Flow > 0
        ocf = float(cf_df.iloc[cy].get('operatingCashFlow', 0))
        if ocf > 0:
            score += 1
            criteria_met.append("Positive Operating Cash Flow")

        # 3. Change in ROA (Current > Previous)
        net_income_prev = float(inc_df.iloc[py].get('netIncome', 0))
        total_assets_prev = float(bal_df.iloc[py].get('totalAssets', 1))
        roa_prev = net_income_prev / total_assets_prev
        
        if roa_current > roa_prev:
            score += 1
            criteria_met.append("Increasing Return on Assets (ROA)")

        # 4. Quality of Earnings (Accruals): OCF > Net Income
        if ocf > net_income:
            score += 1
            criteria_met.append("High Quality Earnings (Cash Flow > Net Income)")

        # --- LEVERAGE, LIQUIDITY, SOURCE OF FUNDS (3 Points) ---

        # 5. Change in Leverage (Long Term Debt)
        # Current LTD should be <= Previous LTD
        ltd_curr = float(bal_df.iloc[cy].get('longTermDebt', 0))
        ltd_prev = float(bal_df.iloc[py].get('longTermDebt', 0))
        
        # We give points if debt decreased OR if debt is zero
        if ltd_curr <= ltd_prev:
            score += 1
            criteria_met.append("Lower or Stable Long-Term Debt")

        # 6. Change in Current Ratio (Current > Previous)
        # Current Assets / Current Liabilities
        ca_curr = float(bal_df.iloc[cy].get('totalCurrentAssets', 0))
        cl_curr = float(bal_df.iloc[cy].get('totalCurrentLiabilities', 1))
        current_ratio_curr = ca_curr / cl_curr if cl_curr else 0

        ca_prev = float(bal_df.iloc[py].get('totalCurrentAssets', 0))
        cl_prev = float(bal_df.iloc[py].get('totalCurrentLiabilities', 1))
        current_ratio_prev = ca_prev / cl_prev if cl_prev else 0

        if current_ratio_curr > current_ratio_prev:
            score += 1
            criteria_met.append("Improving Liquidity (Current Ratio)")

        # 7. Change in Shares Outstanding (No Dilution)
        # Current Shares <= Previous Shares
        shares_curr = float(inc_df.iloc[cy].get('weightedAverageShsOut', 0))
        shares_prev = float(inc_df.iloc[py].get('weightedAverageShsOut', 0))
        
        # Allow a tiny margin for rounding errors (e.g. 0.1%)
        if shares_curr <= shares_prev * 1.001:
            score += 1
            criteria_met.append("No Share Dilution")

        # --- OPERATING EFFICIENCY (2 Points) ---

        # 8. Change in Gross Margin
        # (Gross Profit / Revenue)
        rev_curr = float(inc_df.iloc[cy].get('revenue', 1))
        gp_curr = float(inc_df.iloc[cy].get('grossProfit', 0))
        gm_curr = gp_curr / rev_curr if rev_curr else 0

        rev_prev = float(inc_df.iloc[py].get('revenue', 1))
        gp_prev = float(inc_df.iloc[py].get('grossProfit', 0))
        gm_prev = gp_prev / rev_prev if rev_prev else 0

        if gm_curr > gm_prev:
            score += 1
            criteria_met.append("Improving Gross Margin")

        # 9. Change in Asset Turnover
        # (Revenue / Total Assets)
        at_curr = rev_curr / total_assets if total_assets else 0
        at_prev = rev_prev / total_assets_prev if total_assets_prev else 0

        if at_curr > at_prev:
            score += 1
            criteria_met.append("Improving Asset Turnover efficiency")

    except Exception as e:
        print(f"Piotroski Calculation Error: {e}")
        return {"score": score, "criteria": criteria_met + ["Calculation Error"]}

    return {"score": score, "criteria": criteria_met}


def calculate_graham_scan(profile: dict, key_metrics: dict, income_statements: list, cash_flow_statements: list = []):
    """
    Benjamin Graham 'Defensive Investor' Checklist (7 Tenets).
    Includes specific logic for Indian/Global markets.
    """
    score = 0
    criteria_met = []

    if not profile or not key_metrics or len(income_statements) < 3:
        return {"score": 0, "criteria": ["Insufficient Data for Graham Analysis."]}

    try:
        # --- 1. Adequate Size ---
        # Rule: Exclude small companies to avoid volatility.
        # Heuristic: Market Cap > 2 Billion USD (or approx 15,000 Cr INR)
        # Since API returns raw numbers, we check raw magnitude.
        mcap = float(key_metrics.get('marketCap') or profile.get('mktCap') or 0)
        
        # We assume 'Adequate' is > 2 Billion units of base currency (roughly works for USD and large INR caps)
        if mcap > 2_000_000_000: 
            score += 1
            criteria_met.append(f"Adequate Size (Market Cap > 2B)")

        # --- 2. Strong Financial Condition ---
        # Rule: Current Ratio >= 2.0
        current_ratio = key_metrics.get('currentRatioTTM')
        if current_ratio and current_ratio >= 2.0:
            score += 1
            criteria_met.append(f"Strong Financials (Current Ratio {current_ratio:.2f} >= 2.0)")
        elif current_ratio and current_ratio >= 1.5:
            # Partial credit/mention for decent companies
            pass 

        # --- 3. Earnings Stability ---
        # Rule: Positive earnings for the last 5-10 years.
        # We check whatever history we have (usually 5 years from API).
        earnings_history = [float(s.get('netIncome', 0)) for s in income_statements]
        if earnings_history and all(e > 0 for e in earnings_history):
            score += 1
            criteria_met.append(f"Earnings Stability ({len(earnings_history)} years of positive profit)")

        # --- 4. Dividend Record ---
        # Rule: Uninterrupted payments for 20 years (We check 5 years available).
        # We look at Cash Flow 'dividendsPaid'. Note: These are usually negative numbers (outflows).
        dividends = []
        if cash_flow_statements:
            dividends = [float(s.get('dividendsPaid', 0)) for s in cash_flow_statements]
        elif income_statements:
            # Fallback to income statement if specific CF field missing
            dividends = [float(s.get('dividendsPaid', 0)) for s in income_statements]
            
        # Check if any dividends were paid (non-zero) consistently
        # We allow one missed year in 5 years for strictness flexibility, but let's be strict here:
        if dividends and all(d != 0 for d in dividends):
            score += 1
            criteria_met.append("Consistent Dividend History")

        # --- 5. Earnings Growth ---
        # Rule: At least 33% growth in EPS over the last 10 years (We check 5).
        # List is typically Newest -> Oldest
        if len(income_statements) >= 3:
            # Safely get EPS
            def get_eps(item):
                if item.get('eps'): return float(item['eps'])
                if item.get('netIncome') and item.get('weightedAverageShsOut'):
                    return float(item['netIncome']) / float(item['weightedAverageShsOut'])
                return 0.0

            current_eps = get_eps(income_statements[0])
            past_eps = get_eps(income_statements[-1])
            
            if past_eps > 0 and current_eps > past_eps:
                growth = ((current_eps - past_eps) / past_eps) * 100
                if growth > 15: # Adjusted for shorter timeframe (5y)
                    score += 1
                    criteria_met.append(f"Earnings Growth (EPS grew {growth:.1f}%)")

        # --- 6. Moderate P/E Ratio ---
        # Rule: Current price should not be more than 15 times average earnings.
        pe = float(key_metrics.get('peRatioTTM') or 0)
        if 0 < pe < 15:
            score += 1
            criteria_met.append(f"Attractive Valuation (P/E {pe:.2f} < 15)")

        # --- 7. Moderate Price to Assets (Graham Number) ---
        # Rule: P/E * P/B should not exceed 22.5
        # OR Price to Book < 1.5
        pb = float(key_metrics.get('priceToBookRatioTTM') or 0)
        
        passed_valuation = False
        
        if 0 < pb < 1.5: 
            passed_valuation = True
            criteria_met.append(f"Assets Undervalued (P/B {pb:.2f} < 1.5)")
        elif pe > 0 and pb > 0 and (pe * pb) < 22.5:
            passed_valuation = True
            criteria_met.append(f"Graham Number Safe (P/E * P/B = {(pe*pb):.1f} < 22.5)")
            
        if passed_valuation:
            score += 1

    except Exception as e:
        print(f"Graham Scan Error: {e}")
        criteria_met.append("Analysis interrupted by missing data")

    return {"score": score, "criteria": criteria_met}
```

## File: backend/app/services/redis_service.py
```python
import os
import json
import asyncio
import time
import redis.asyncio as redis
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

# ==========================================
# 1. IN-MEMORY ENGINE (Zero-Latency Localhost)
# ==========================================
class MemoryPubSub:
    """
    Simulates Redis Pub/Sub AND Locking using Python Asyncio.
    Used when Redis is unavailable or for local testing.
    """
    def __init__(self):
        self.queues = set()
        self.locks = {} # Local simulation of distributed locks

    async def subscribe(self, channel):
        # In local mode, we listen to everything implicitly
        pass

    async def listen(self):
        """Yields messages to the WebSocket consumer."""
        q = asyncio.Queue()
        self.queues.add(q)
        try:
            while True:
                msg = await q.get()
                yield {"type": "message", "data": msg}
        except asyncio.CancelledError:
            self.queues.discard(q)

    async def publish(self, message):
        """Push data to all active local listeners."""
        for q in list(self.queues):
            try: 
                q.put_nowait(message)
            except: 
                pass

    # --- LOCAL LOCKING SIMULATION ---
    async def acquire_lock(self, key, ttl):
        """Simulates Redis SET NX EX"""
        now = time.time()
        # If lock exists and hasn't expired, return False
        if key in self.locks and now < self.locks[key]:
            return False
        
        # Take lock
        self.locks[key] = now + ttl
        return True

    async def extend_lock(self, key, ttl):
        """Simulates Redis EXPIRE"""
        now = time.time()
        # Only extend if we actually have it (simplified for local)
        if key in self.locks:
            self.locks[key] = now + ttl
            return True
        return False

# Global Memory State
memory_bus = MemoryPubSub()
local_storage = {
    "cache": {},
    "active": set(),
    "heartbeats": {}
}

# ==========================================
# 2. ROBUST REDIS MANAGER (With Locking)
# ==========================================
class RedisManager:
    def __init__(self):
        self.redis = None
        self.use_redis = False
        self._checked = False
        self._pool = None

    async def _get_connection(self):
        if self._checked:
            return self.redis if self.use_redis else None

        # DEBUG LOGGING
        print(f"🔍 DEBUG: Checking Redis Connection...")
        print(f"   -> REDIS_URL exists? {'YES' if REDIS_URL else 'NO'}")
        if REDIS_URL:
            # Mask password for logs
            masked = REDIS_URL.split('@')[-1] if '@' in REDIS_URL else 'HIDDEN'
            print(f"   -> Target: {masked}")

        if not REDIS_URL:
            print("⚡ Redis: No URL found. Using Local Memory.")
            self.use_redis = False
            self._checked = True
            return None

        try:
            # Try connecting
            pool = redis.ConnectionPool.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=2)
            r = redis.Redis(connection_pool=pool)
            await r.ping()
            
            print("✅ Redis: CONNECTED SUCCESSFULLY!")
            self.redis = r
            self.use_redis = True
        except Exception as e:
            print(f"❌ Redis Connection FAILED: {e}")
            print("   -> Switching to Local Memory Mode.")
            self.use_redis = False
        
        self._checked = True
        return self.redis if self.use_redis else None

    # --- DISTRIBUTED LOCKING (CRITICAL FOR FYERS) ---
    async def acquire_lock(self, key: str, ttl: int = 15):
        """
        Tries to become the 'Master' worker.
        Returns True if lock acquired, False if someone else has it.
        """
        r = await self._get_connection()
        if r:
            # Redis 'SET ... NX' (Only set if Not Exists)
            return await r.set(key, "LOCKED", nx=True, ex=ttl)
        else:
            return await memory_bus.acquire_lock(key, ttl)

    async def extend_lock(self, key: str, ttl: int = 15):
        """
        Keep the lock alive (Heartbeat for Master).
        """
        r = await self._get_connection()
        if r:
            return await r.expire(key, ttl)
        else:
            return await memory_bus.extend_lock(key, ttl)

    # --- WATCHLIST LOGIC ---
    async def add_active_symbol(self, symbol: str):
        r = await self._get_connection()
        if r:
            try:
                await r.sadd("active_symbols_v2", symbol)
                await r.setex(f"heartbeat:{symbol}", 15, "alive")
            except: pass
        else:
            # Local Mode
            local_storage["active"].add(symbol)
            local_storage["heartbeats"][symbol] = time.time() + 15

    async def get_active_symbols(self):
        r = await self._get_connection()
        if r:
            try:
                candidates = await r.smembers("active_symbols_v2")
                active = []
                for sym in candidates:
                    if await r.exists(f"heartbeat:{sym}"): active.append(sym)
                    else: await r.srem("active_symbols_v2", sym)
                return active
            except: return []
        else:
            # Local Mode: Check heartbeats
            now = time.time()
            alive = []
            for sym in list(local_storage["active"]):
                if sym in local_storage["heartbeats"] and now < local_storage["heartbeats"][sym]:
                    alive.append(sym)
                else:
                    local_storage["active"].discard(sym)
            return alive

    # --- PUB/SUB LOGIC ---
    async def publish_update(self, symbol: str, data: dict):
        try:
            msg = json.dumps({"symbol": symbol, "data": data}, default=str)
            r = await self._get_connection()
            if r:
                await r.publish("market_feed", msg)
            else:
                await memory_bus.publish(msg)
        except: pass

    def get_subscriber(self):
        # Note: This is synchronous, so we check the flag directly
        if self.use_redis and self.redis:
            return self.redis.pubsub()
        return memory_bus

    # --- CACHE LOGIC ---
    async def get_cache(self, key: str):
        r = await self._get_connection()
        if r:
            try:
                data = await r.get(key)
                return json.loads(data) if data else None
            except: return None
        # Local Mode: Simple Dict Get
        return local_storage["cache"].get(key)

    async def set_cache(self, key: str, data: any, ttl: int = 60):
        r = await self._get_connection()
        if r:
            try: await r.set(key, json.dumps(data, default=str), ex=ttl)
            except: pass
        else:
            # Local Mode: Simple Dict Set (No TTL for simplicity in dev)
            local_storage["cache"][key] = data

# Singleton Export
redis_client = RedisManager()
```

## File: frontend/src/App.js
```javascript
import React from 'react';
import PureVisionPage from './pages/PureVisionPage';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { GlobalStyles } from './styles/GlobalStyles';
import HomePage from './pages/HomePage';
import StockDetailPage from './pages/StockDetailPage';
// --- NEW: Import our new Index Detail Page ---
import IndexDetailPage from './pages/IndexDetailPage';
import AuthCallback from './pages/AuthCallback'; // Import this


function App() {
  return (
    <>
      {/* This component injects our beautiful dark theme styles into the entire app */}
      <GlobalStyles />

      {/* The Router handles all page navigation */}
      <Router>
        <Routes>
          {/* Route for the main landing/search page */}
          <Route path="/" element={<HomePage />} />

          {/* Route for the detailed stock analysis page */}
          <Route path="/stock/:symbol" element={<StockDetailPage />} />

          {/* --- NEW ROUTE ADDED HERE --- */}
          {/* Route for the detailed index analysis page. 
              The ":encodedSymbol" will hold the URL-safe version of the index symbol. */}
          <Route path="/index/:encodedSymbol" element={<IndexDetailPage />} />
          <Route path="/vision-result" element={<PureVisionPage />} />
          <Route path="/auth-callback" element={<AuthCallback />} />


        </Routes>
      </Router>
    </>
  );
}

export default App;
```

## File: frontend/src/components/common/Tabs/Tabs.js
```javascript
import React, { useState, useRef, Children, isValidElement } from 'react';
import styled from 'styled-components';
import { FaChevronLeft, FaChevronRight } from 'react-icons/fa';

// --- Styled Components ---

const TabsContainer = styled.div`
  width: 100%;
  position: relative; /* Needed for absolute positioning of arrows */
`;

const TabListWrapper = styled.div`
  position: relative;
  display: flex;
  align-items: center;
  border-bottom: 2px solid var(--color-border);
`;

const TabList = styled.div`
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
  width: 100%;
  
  /* Hide scrollbar for a clean, native-app feel */
  &::-webkit-scrollbar {
    display: none;
  }
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
`;

const TabButton = styled.button`
  padding: 1rem 1.5rem;
  border: none;
  background-color: transparent;
  color: ${({ active }) => (active ? 'var(--color-text-primary)' : 'var(--color-text-secondary)')};
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  position: relative;
  transition: color 0.3s ease;
  white-space: nowrap; /* Critical: prevents text from wrapping */
  flex-shrink: 0; /* Critical: prevents buttons from squishing */

  &:hover {
    color: var(--color-text-primary);
  }

  &::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 100%;
    height: 2px;
    background-color: var(--color-primary);
    transform: ${({ active }) => (active ? 'scaleX(1)' : 'scaleX(0)')};
    transform-origin: bottom;
    transition: transform 0.3s ease-out;
  }
`;

// --- The Scroll Arrow Buttons ---
const ScrollButton = styled.button`
  position: absolute;
  top: 0;
  bottom: 0;
  width: 40px;
  border: none;
  cursor: pointer;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-primary);
  font-size: 1rem;
  transition: opacity 0.2s;
  
  /* High-end gradient effect to fade content behind the arrow */
  &.left {
    left: 0;
    background: linear-gradient(to right, var(--color-background) 40%, transparent 100%);
  }
  
  &.right {
    right: 0;
    background: linear-gradient(to left, var(--color-background) 40%, transparent 100%);
  }

  &:hover {
    color: var(--color-text-primary);
  }

  /* Only show arrows on devices where scrolling might be needed */
  @media (min-width: 768px) {
     /* Optional: You can hide them on large desktop if you prefer, 
        but keeping them ensures usability everywhere */
  }
`;

const TabContentContainer = styled.div`
  padding: 2rem 0;
`;

const TabPanelWrapper = styled.div`
  display: ${({ active }) => (active ? 'block' : 'none')};
`;


// --- The Logic ---

const Tabs = ({ children }) => {
  const validChildren = Children.toArray(children).filter(isValidElement);
  const [activeTab, setActiveTab] = useState(validChildren[0]?.props.label);
  const scrollRef = useRef(null);

  const handleClick = (e, newActiveTab) => {
    e.preventDefault();
    setActiveTab(newActiveTab);
    
    // Optional: Auto-scroll the active tab into view
    e.target.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
  };

  const scroll = (direction) => {
    if (scrollRef.current) {
      const { current } = scrollRef;
      const scrollAmount = 200; // Adjust scroll speed
      if (direction === 'left') {
        current.scrollLeft -= scrollAmount;
      } else {
        current.scrollLeft += scrollAmount;
      }
    }
  };

  return (
    <TabsContainer>
      <TabListWrapper>
        {/* Left Arrow */}
        <ScrollButton className="left" onClick={() => scroll('left')} aria-label="Scroll Left">
          <FaChevronLeft />
        </ScrollButton>

        <TabList ref={scrollRef}>
          {validChildren.map(child => (
            <TabButton
              key={child.props.label}
              active={activeTab === child.props.label}
              onClick={e => handleClick(e, child.props.label)}
            >
              {child.props.label}
            </TabButton>
          ))}
        </TabList>

        {/* Right Arrow */}
        <ScrollButton className="right" onClick={() => scroll('right')} aria-label="Scroll Right">
          <FaChevronRight />
        </ScrollButton>
      </TabListWrapper>

      <TabContentContainer>
        {validChildren.map(child => (
          <TabPanelWrapper
            key={child.props.label}
            active={activeTab === child.props.label}
          >
            {child.props.children}
          </TabPanelWrapper>
        ))}
      </TabContentContainer>
    </TabsContainer>
  );
};

const TabPanel = ({ label, children }) => {
  return <div label={label}>{children}</div>;
};

export { Tabs, TabPanel };
```

## File: frontend/src/components/Financials/Financials.js
```javascript
import React from 'react';
import styled from 'styled-components';

// --- Import all our components ---
import Card from '../common/Card';
import RevenueChart from './RevenueChart';
import KeyStats from './KeyStats';
import AboutCompany from './AboutCompany';
import BalanceSheet from './BalanceSheet';
// --- NEW: Import our new Financial Statements viewer ---
import FinancialStatements from './FinancialStatements';

// --- Styled Components ---

const FinancialsContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem; /* Adds space between each section */
`;

// --- The Final, Upgraded React Component ---

const Financials = ({
  profile,
  keyStats,
  financialData,
  balanceSheetData,
  // --- NEW: Accepting all the new data props ---
  annualCashFlow,
  quarterlyIncome,
  quarterlyBalance,
  quarterlyCashFlow
}) => {
  // Defensive check: If we don't have the core profile data, show a generic message.
  if (!profile) {
    return (
      <Card>
        <p>Financial data is not available for this stock.</p>
      </Card>
    );
  }

  return (
    <Card>
      <FinancialsContainer>

        {/* --- Section 1: Key Stats (Unchanged) --- */}
        <KeyStats stats={keyStats} />
        
        {/* --- Section 2: Balance Sheet Charts (Unchanged) --- */}
        <BalanceSheet balanceSheetData={balanceSheetData} />

        {/* --- Section 3: Income Statement Chart (Unchanged) --- */}
        <div>
            <h3 style={{ fontSize: '1.5rem', fontWeight: 600, marginBottom: '1.5rem' }}>Income Statement (5-Year Trend)</h3>
            <RevenueChart data={financialData} />
        </div>

        {/* --- Section 4: Detailed Financial Statements Viewer (NEW!) --- */}
        {/* We add our new component here, passing all the necessary annual and quarterly data down to it. */}
        <FinancialStatements
          currency={profile.currency}
          annualIncome={financialData}
          annualBalance={balanceSheetData}
          annualCashFlow={annualCashFlow}
          quarterlyIncome={quarterlyIncome}
          quarterlyBalance={quarterlyBalance}
          quarterlyCashFlow={quarterlyCashFlow}
        />

        {/* --- Section 5: About the Company (Unchanged) --- */}
        <AboutCompany profile={profile} />

      </FinancialsContainer>
    </Card>
  );
};

export default Financials;
```

## File: frontend/src/components/Indices/IndicesBanner.js
```javascript
import React, { useState, useEffect, useRef } from 'react';
import styled, { keyframes, css } from 'styled-components';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

// ==========================================
// 1. HIGH-END ANIMATIONS
// ==========================================

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
`;

const flashGreen = keyframes`
  0% { color: var(--color-text-primary); transform: scale(1); }
  10% { color: #3FB950; text-shadow: 0 0 15px rgba(63, 185, 80, 0.6); transform: scale(1.05); }
  100% { color: var(--color-text-primary); transform: scale(1); }
`;

const flashRed = keyframes`
  0% { color: var(--color-text-primary); transform: scale(1); }
  10% { color: #F85149; text-shadow: 0 0 15px rgba(248, 81, 73, 0.6); transform: scale(1.05); }
  100% { color: var(--color-text-primary); transform: scale(1); }
`;

// ==========================================
// 2. STYLED COMPONENTS
// ==========================================

const BannerContainer = styled.div`
  width: 100%;
  padding: 1rem 0;
  margin-bottom: 2rem;
  overflow: hidden;
`;

const CardScroller = styled.div`
  display: flex;
  gap: 1rem;
  overflow-x: auto;
  padding: 0.5rem;
  
  /* Hide scrollbar for sleek look */
  &::-webkit-scrollbar { display: none; }
  -ms-overflow-style: none;
  scrollbar-width: none;
`;

const IndexCard = styled.div`
  flex-shrink: 0;
  width: 220px;
  padding: 1.2rem;
  background-color: var(--color-secondary);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
  animation: ${fadeIn} 0.5s ease-out;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    border-color: var(--color-primary);
  }
`;

const IndexHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
`;

const IndexName = styled.h3`
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--color-text-secondary);
  white-space: nowrap;
  margin: 0;
  letter-spacing: 0.5px;
`;

const CurrencyBadge = styled.span`
  font-size: 0.65rem;
  background: rgba(255, 255, 255, 0.08);
  padding: 2px 6px;
  border-radius: 4px;
  color: var(--color-text-secondary);
  font-weight: 700;
`;

const IndexPrice = styled.div`
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 0.4rem;
  font-family: 'Roboto Mono', monospace;
  
  /* Dynamic Flashing Logic */
  ${({ flash }) => flash === 'up' && css`animation: ${flashGreen} 0.5s ease-out;`}
  ${({ flash }) => flash === 'down' && css`animation: ${flashRed} 0.5s ease-out;`}
`;

const IndexChange = styled.div`
  font-size: 0.85rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  color: ${({ isPositive }) => (isPositive ? 'var(--color-success)' : 'var(--color-danger)')};
`;

const ConnectionDot = styled.div`
  position: absolute;
  top: 10px;
  right: 10px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: ${({ active }) => active ? '#3FB950' : 'transparent'};
  box-shadow: ${({ active }) => active ? '0 0 5px #3FB950' : 'none'};
  transition: background-color 0.3s ease;
`;

// ==========================================
// 3. LOGIC & COMPONENT
// ==========================================

const getCurrencySymbol = (code) => {
    switch (code) { 
        case 'INR': return '₹'; 
        case 'USD': return '$'; 
        case 'JPY': return '¥'; 
        case 'EUR': return '€'; 
        default: return '$'; 
    }
};

const IndicesBanner = () => {
  const [indices, setIndices] = useState([]);
  const [flashStates, setFlashStates] = useState({});
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef(null);
  const navigate = useNavigate();
  const isMounted = useRef(true);

  // --- 1. INITIAL LOAD (REST API) ---
  useEffect(() => {
    isMounted.current = true;
    const loadInitial = async () => {
        try {
            // Use Environment Variable for Flexibility (Vercel vs Local)
            const baseUrl = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
            const res = await axios.get(`${baseUrl}/api/indices/summary`);
            
            if (res.data && Array.isArray(res.data) && isMounted.current) {
                setIndices(res.data);
            }
        } catch(e) {
            console.error("Initial load failed", e);
        }
    };
    loadInitial();
    
    return () => { isMounted.current = false; };
  }, []);

  // --- 2. LIVE WEBSOCKET ENGINE ---
  useEffect(() => {
    // Dynamic URL Construction (Works on Vercel & Localhost)
    const getWsUrl = () => {
        const apiUrl = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
        const wsProtocol = apiUrl.includes('https') ? 'wss://' : 'ws://';
        const host = apiUrl.replace(/^https?:\/\//, '');
        // Connect to the specific channel for homepage ticker
        return `${wsProtocol}${host}/ws/live/MARKET_OVERVIEW`;
    };

    const wsUrl = getWsUrl();
    let pingInterval = null;

    const connect = () => {
        if (wsRef.current?.readyState === WebSocket.OPEN) return;

        const ws = new WebSocket(wsUrl);
        wsRef.current = ws;

        ws.onopen = () => {
            if (!isMounted.current) return;
            setIsConnected(true);
            
            // Heartbeat: Keep connection alive on Railway
            pingInterval = setInterval(() => {
                if (ws.readyState === WebSocket.OPEN) {
                    ws.send("ping");
                }
            }, 10000); 
        };

        ws.onmessage = (event) => {
            if (!isMounted.current) return;
            try {
                const update = JSON.parse(event.data);
                const symbol = update.symbol; 
                
                if (!symbol) return;

                setIndices(prevIndices => {
                    return prevIndices.map(idx => {
                        // Match incoming update to existing card
                        if (idx.symbol === symbol) {
                            
                            // Visual Flash Logic
                            if (update.price !== idx.price) {
                                const dir = update.price > idx.price ? 'up' : 'down';
                                
                                setFlashStates(prev => ({ ...prev, [symbol]: dir }));
                                
                                // Clear flash after animation
                                setTimeout(() => {
                                    if (isMounted.current) {
                                        setFlashStates(prev => {
                                            const next = { ...prev };
                                            delete next[symbol];
                                            return next;
                                        });
                                    }
                                }, 600);
                            }
                            
                            // Return Updated Card Data
                            return {
                                ...idx,
                                price: update.price,
                                change: update.change,
                                percent_change: update.percent_change
                            };
                        }
                        return idx; // No change for this card
                    });
                });
            } catch(e) {
                // Silent fail for keep-alive packets
            }
        };
        
        ws.onclose = () => {
            if (isMounted.current) setIsConnected(false);
            if (pingInterval) clearInterval(pingInterval);
            // Auto-Reconnect after 3 seconds if connection drops
            if (isMounted.current) setTimeout(connect, 3000);
        };
    };

    connect();

    // Cleanup on Unmount
    return () => { 
        if (pingInterval) clearInterval(pingInterval);
        if(wsRef.current) wsRef.current.close(); 
    };
  }, []);

  const handleCardClick = (symbol) => {
    navigate(`/index/${encodeURIComponent(symbol)}`);
  };

  // Render nothing until data loads (prevents empty flashes)
  if (indices.length === 0) return null;

  return (
    <BannerContainer>
      <CardScroller>
        {indices.map(index => {
          // Safe Number Conversion (Fixes .toFixed crash)
          const safePrice = Number(index.price) || 0;
          const safeChange = Number(index.change) || 0;
          const safePct = Number(index.percent_change) || 0;
          
          const isPositive = safeChange >= 0;
          const symbol = getCurrencySymbol(index.currency);
          const flash = flashStates[index.symbol];
          
          return (
            <IndexCard key={index.symbol} onClick={() => handleCardClick(index.symbol)}>
              <ConnectionDot active={isConnected} />
              <IndexHeader>
                <IndexName>{index.name}</IndexName>
                <CurrencyBadge>{index.currency}</CurrencyBadge>
              </IndexHeader>
              
              <IndexPrice flash={flash}>
                {symbol}{safePrice.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
              </IndexPrice>
              
              <IndexChange isPositive={isPositive}>
                {isPositive ? '▲' : '▼'} 
                {Math.abs(safeChange).toFixed(2)} ({safePct.toFixed(2)}%)
              </IndexChange>
            </IndexCard>
          );
        })}
      </CardScroller>
    </BannerContainer>
  );
};

export default IndicesBanner;
```

## File: frontend/src/components/Shareholding/DonutChart.js
```javascript
import React from 'react';
import styled, { keyframes } from 'styled-components';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { FaChartPie } from 'react-icons/fa'; // Import an icon for the placeholder

// --- Styled Components ---

const fadeIn = keyframes`
  from { opacity: 0; }
  to { opacity: 1; }
`;

const ChartWrapper = styled.div`
  width: 100%;
  height: 350px;
  position: relative;
`;

// --- NEW: Beautiful Placeholder Styles ---
const PlaceholderContainer = styled.div`
  width: 100%;
  height: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.02);
  border-radius: 12px;
  border: 1px dashed var(--color-border);
  padding: 2rem;
  text-align: center;
  animation: ${fadeIn} 0.5s ease-in;
`;

const PlaceholderIcon = styled.div`
  font-size: 3rem;
  color: var(--color-text-secondary);
  margin-bottom: 1rem;
  opacity: 0.5;
`;

const PlaceholderTitle = styled.h4`
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
`;

const DisclaimerText = styled.p`
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  line-height: 1.6;
  max-width: 80%;
  margin: 0 auto;
  font-style: italic;
`;

// --- The Upgraded React Component ---

const DonutChart = ({ breakdown }) => {
  // Define our professional color palette.
  const COLORS = {
    Promoter: '#3B82F6', // Blue
    FII: '#10B981',      // Green
    DII: '#F59E0B',      // Amber/Yellow
    Public: '#EF4444',   // Red
  };

  // --- LOGIC CHECK: Do we have valid data? ---
  // If breakdown is missing, empty, or has 'public' as undefined, we treat it as missing.
  const hasData = breakdown && Object.keys(breakdown).length > 0 && breakdown.public !== undefined;

  // If NO data, render the beautiful placeholder
  if (!hasData) {
      return (
          <PlaceholderContainer>
              <PlaceholderIcon>
                  <FaChartPie />
              </PlaceholderIcon>
              <PlaceholderTitle>Data Coming Soon</PlaceholderTitle>
              <DisclaimerText>
                  Detailed shareholding patterns for this specific region are currently being integrated into our system. 
                  <br />
                  This section is a placeholder and will be updated automatically once the data source is live.
              </DisclaimerText>
          </PlaceholderContainer>
      );
  }

  // --- Data Processing (Only runs if we have data) ---
  const chartData = [
    { name: 'Promoter', value: breakdown.promoter, color: COLORS.Promoter },
    { name: 'FII', value: breakdown.fii, color: COLORS.FII },
    { name: 'DII', value: breakdown.dii, color: COLORS.DII },
    { name: 'Public', value: breakdown.public, color: COLORS.Public },
  ].filter(entry => entry.value > 0.01);

  const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, name }) => {
    const RADIAN = Math.PI / 180;
    const radius = outerRadius * 1.4; 
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
      <text
        x={x}
        y={y}
        fill="var(--color-text-primary)"
        textAnchor={x > cx ? 'start' : 'end'}
        dominantBaseline="central"
        fontSize="14px"
        fontWeight="600"
      >
        {`${name} ${(percent * 100).toFixed(1)}%`}
      </text>
    );
  };

  return (
    <ChartWrapper>
      <ResponsiveContainer>
        <PieChart margin={{ top: 40, right: 40, bottom: 40, left: 40 }}>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={80}
            outerRadius={120}
            fill="#8884d8"
            paddingAngle={5}
            dataKey="value"
            nameKey="name"
            labelLine={false}
            label={renderCustomizedLabel}
          >
            {chartData.map((entry) => (
              <Cell key={`cell-${entry.name}`} fill={entry.color} stroke={entry.color} />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
    </ChartWrapper>
  );
};

export default DonutChart;
```

## File: frontend/src/pages/IndexDetailPage.js
```javascript
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';
import { FaArrowLeft, FaGlobeAmericas, FaChartLine, FaExclamationTriangle } from 'react-icons/fa';

// --- COMPONENTS ---
import StockHeader from '../components/Header/StockHeader';
import CustomChart from '../components/Chart/CustomChart';
import IndexChartAnalysis from '../components/IndexDetailPage/IndexChartAnalysis';
import Technicals from '../components/Technicals/Technicals';
import Card from '../components/common/Card';

// --- CONFIGURATION ---
// Critical for Vercel deployment to find the Railway backend
const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

// --- ANIMATIONS ---
const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`;

const spin = keyframes`
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
`;

// --- STYLED COMPONENTS ---

const PageContainer = styled.div`
  padding: 2rem 3rem;
  max-width: 1800px;
  margin: 0 auto;
  animation: ${fadeIn} 0.5s ease-in;
  
  @media (max-width: 768px) {
    padding: 1rem;
  }
`;

const BackButton = styled.button`
  background: none;
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  margin-bottom: 2rem;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;

  &:hover {
    background-color: var(--color-secondary);
    color: var(--color-text-primary);
    border-color: #EBCB8B; /* Gold Accent for Indices */
  }
`;

const DashboardGrid = styled.div`
  display: grid;
  /* If AI data exists (upload), split 50/50. Otherwise full width. */
  grid-template-columns: ${({ hasUpload }) => hasUpload ? '1fr 1fr' : '1fr'};
  gap: 2rem;
  
  @media (max-width: 1200px) {
    grid-template-columns: 1fr; /* Stack on smaller screens */
  }
`;

const LeftPanel = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const RightPanel = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const SectionHeader = styled.h2`
  font-size: 1.5rem;
  color: #EBCB8B; /* Gold Theme */
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 10px;
  border-bottom: 1px solid rgba(235, 203, 139, 0.2);
  padding-bottom: 0.5rem;
`;

const LoadingContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 80vh;
  color: #EBCB8B;
  font-size: 1.5rem;
  gap: 1rem;
`;

const Spinner = styled.div`
  border: 3px solid rgba(235, 203, 139, 0.3);
  border-top: 3px solid #EBCB8B;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: ${spin} 1s linear infinite;
`;

const ErrorContainer = styled(LoadingContainer)`
  color: #F85149;
`;

// --- MAIN COMPONENT ---

const IndexDetailPage = () => {
  const { encodedSymbol } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  const symbol = decodeURIComponent(encodedSymbol);
  
  // Data State
  const aiAnalysisData = location.state?.chartAnalysis;
  const [indexData, setIndexData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // --- FETCH LIVE DATA ---
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        // Use the configured API URL
        const response = await axios.get(`${API_URL}/api/indices/${encodedSymbol}/details`);
        
        if (!response.data || !response.data.profile) {
            throw new Error("Incomplete data received");
        }
        
        setIndexData(response.data);
      } catch (err) {
        console.error("Index fetch error:", err);
        setError("Could not retrieve Global Market Data.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [encodedSymbol]);

  // --- RENDER STATES ---

  if (loading) {
    return (
        <LoadingContainer>
            <Spinner />
            <span>Loading Macro Data for {symbol}...</span>
        </LoadingContainer>
    );
  }

  if (error || !indexData) {
      return (
        <ErrorContainer>
            <FaExclamationTriangle size={50} />
            <p>{error || "Index Data Unavailable."}</p>
            <BackButton onClick={() => navigate('/')}>Return Home</BackButton>
        </ErrorContainer>
      );
  }

  // Destructure Data from Backend
  const { profile, quote, technical_indicators, moving_averages, pivot_points, analyst_ratings } = indexData;

  return (
    <PageContainer>
      <BackButton onClick={() => navigate('/')}>
        <FaArrowLeft /> Back to Command Center
      </BackButton>

      {/* 1. Header (Price, Name, Logo) */}
      <StockHeader profile={profile} quote={quote} />

      <DashboardGrid hasUpload={!!aiAnalysisData}>
        
        {/* --- LEFT PANEL: AI ANALYSIS (Only if uploaded) --- */}
        {aiAnalysisData && (
          <LeftPanel>
            <SectionHeader><FaGlobeAmericas /> Macro Analysis</SectionHeader>
            
            {/* The Gold-Themed AI Card */}
            <IndexChartAnalysis analysisData={aiAnalysisData} />
            
            <Card title="Context">
                 <p style={{color:'var(--color-text-secondary)', lineHeight: '1.6'}}>
                    This analysis is based on the technical structure provided in your uploaded chart. 
                    Compare this with the live market data on the right for maximum confluence.
                 </p>
            </Card>
          </LeftPanel>
        )}

        {/* --- RIGHT PANEL: LIVE MARKET DATA --- */}
        <RightPanel>
          <SectionHeader><FaChartLine /> Live Market Data</SectionHeader>
          
          {/* A. Live Interactive Chart */}
          <CustomChart symbol={symbol} />

          {/* B. Technical Dashboard */}
          {/* CRITICAL: Passing snake_case backend data to camelCase props */}
          <Technicals 
             technicalIndicators={technical_indicators}
             movingAverages={moving_averages} 
             pivotPoints={pivot_points}
             analystRatings={analyst_ratings}
             quote={quote}
          />
        </RightPanel>

      </DashboardGrid>

    </PageContainer>
  );
};

export default IndexDetailPage;
```

## File: frontend/package.json
```json
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "proxy": "http://localhost:8000",
  "dependencies": {
    "@testing-library/jest-dom": "^5.17.0",
    "@testing-library/react": "^13.4.0",
    "@testing-library/user-event": "^13.5.0",
    "axios": "^1.13.2",
    "lightweight-charts": "^5.1.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-gauge-chart": "^0.5.1",
    "react-icons": "^5.5.0",
    "react-router-dom": "^7.9.5",
    "react-scripts": "5.0.1",
    "recharts": "^3.3.0",
    "styled-components": "^6.1.19",
    "technicalindicators": "^3.1.0",
    "web-vitals": "^2.1.4"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "CI=false react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app",
      "react-app/jest"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

## File: frontend/src/components/Fundamentals/FundamentalConclusion.js
```javascript
import React, { useMemo } from 'react';
import styled, { keyframes } from 'styled-components';
import GaugeChart from 'react-gauge-chart';

// --- Styled Components & Animations ---

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const SectionContainer = styled.div`
  animation: ${fadeIn} 0.5s ease-out;
  padding: 1rem;
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 2rem;
  color: var(--color-text-primary);
  text-align: center;
`;

const ConclusionGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 3rem;
  align-items: start;

  @media (max-width: 992px) {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
`;

// --- METER SECTION ---
const MeterWrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  padding: 2rem 1.5rem;
  position: relative;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
`;

const GradeLabel = styled.div`
  font-size: 3.5rem;
  font-weight: 800;
  margin-top: -30px;
  color: ${({ color }) => color};
  text-shadow: 0 0 20px ${({ color }) => color}44;
`;

const GradeSubtitle = styled.span`
  font-size: 1rem;
  color: var(--color-text-secondary);
  margin-top: 0.5rem;
  font-weight: 500;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 1.5rem;
`;

// --- NEW: GRADE LEGEND TABLE ---
const LegendContainer = styled.div`
  width: 100%;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const LegendHeader = styled.div`
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--color-text-secondary);
  opacity: 0.7;
  margin-bottom: 0.25rem;
  text-align: center;
  letter-spacing: 1px;
`;

const LegendItem = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  padding: 0.4rem 0;
  border-bottom: 1px solid rgba(255,255,255,0.05);

  &:last-child {
    border-bottom: none;
  }
`;

const LegendGrade = styled.span`
  font-weight: 700;
  color: ${({ color }) => color};
  width: 30px;
`;

const LegendMeaning = styled.span`
  color: var(--color-text-secondary);
`;

// --- RIGHT SIDE CONTENT ---
const ThesisBox = styled.div`
  background: linear-gradient(135deg, rgba(22, 27, 34, 0.8), rgba(30, 41, 59, 0.4));
  border-left: 4px solid var(--color-primary);
  padding: 1.5rem;
  border-radius: 0 8px 8px 0;
  margin-bottom: 2rem;
`;

const ThesisText = styled.p`
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--color-text-primary);
  line-height: 1.8;
  font-style: italic;
`;

const TakeawaysList = styled.ul`
  list-style-type: none;
  padding-left: 0;
`;

const TakeawayItem = styled.li`
  margin-bottom: 1rem;
  color: var(--color-text-secondary);
  display: flex;
  align-items: flex-start;
  line-height: 1.6;
  background: rgba(255,255,255,0.03);
  padding: 1rem;
  border-radius: 8px;
  border: 1px solid transparent;
  transition: all 0.2s ease;

  &:hover {
    border-color: var(--color-border);
    transform: translateX(5px);
  }

  &::before {
    content: 'Analyzed';
    background-color: var(--color-primary);
    color: #000;
    font-size: 0.6rem;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
    margin-right: 12px;
    margin-top: 4px;
    text-transform: uppercase;
  }
`;

// --- HELPERS ---
const getScoreFromGrade = (grade) => {
    if (!grade) return 0;
    const g = grade.toUpperCase().replace(/[^A-F]/g, '');
    if (g === 'A') return 0.95;
    if (g === 'B') return 0.80;
    if (g === 'C') return 0.60;
    if (g === 'D') return 0.40;
    if (g === 'F') return 0.15;
    return 0.50;
};

const getGradeColor = (grade) => {
    if (!grade) return 'var(--color-text-secondary)';
    const g = grade.toUpperCase();
    if (g.includes('A')) return 'var(--color-success)'; 
    if (g.includes('B')) return '#34D399'; 
    if (g.includes('C')) return '#EDBB5A'; 
    if (g.includes('D')) return '#F88149'; 
    if (g.includes('F')) return 'var(--color-danger)'; 
    return 'var(--color-text-secondary)';
};

// --- MAIN COMPONENT ---

const FundamentalConclusion = ({ conclusionData }) => {
  
  const parsedConclusion = useMemo(() => {
    if (!conclusionData) {
      return { grade: 'N/A', thesis: 'System is analyzing the financial structure...', takeaways: [] };
    }
    
    const cleanText = "\n" + conclusionData.replace(/\*\*/g, '').replace(/\*/g, '');

    const gradeMatch = cleanText.match(/GRADE:\s*([A-F][+-]?)/i);
    const grade = gradeMatch ? gradeMatch[1].toUpperCase() : 'N/A';

    const thesisMatch = cleanText.match(/THESIS:\s*([\s\S]*?)(?=TAKEAWAYS:|$)/i);
    const thesis = thesisMatch ? thesisMatch[1].trim() : 'No thesis generated.';

    const takeawaysMatch = cleanText.match(/TAKEAWAYS:\s*([\s\S]*)/i);
    const rawTakeaways = takeawaysMatch ? takeawaysMatch[1].trim() : '';
    
    const takeaways = rawTakeaways
        .split(/\n\s*[-•]\s*/)
        .map(t => t.trim())
        .filter(t => t.length > 10); 

    return { grade, thesis, takeaways };
  }, [conclusionData]);

  const scorePercent = getScoreFromGrade(parsedConclusion.grade);
  const gradeColor = getGradeColor(parsedConclusion.grade);

  return (
    <SectionContainer>
      <SectionTitle>Analyst Verdict</SectionTitle>
      
      <ConclusionGrid>
        
        {/* --- LEFT: METER + LEGEND --- */}
        <MeterWrapper>
            <GaugeChart 
                id="fundamental-grade-gauge"
                nrOfLevels={5}
                colors={['#F85149', '#F88149', '#EDBB5A', '#34D399', '#3FB950']}
                arcWidth={0.3}
                percent={scorePercent}
                textColor="transparent"
                needleBaseColor="#C9D1D9"
                needleColor="#C9D1D9"
                animate={true}
            />
            <GradeLabel color={gradeColor}>{parsedConclusion.grade}</GradeLabel>
            <GradeSubtitle>Fundamental Grade</GradeSubtitle>

            {/* --- NEW LEGEND TABLE --- */}
            <LegendContainer>
                <LegendHeader>Grade Scale Guide</LegendHeader>
                <LegendItem>
                    <LegendGrade color="var(--color-success)">A</LegendGrade>
                    <LegendMeaning>Excellent / Strong Buy</LegendMeaning>
                </LegendItem>
                <LegendItem>
                    <LegendGrade color="#34D399">B</LegendGrade>
                    <LegendMeaning>Good / Accumulate</LegendMeaning>
                </LegendItem>
                <LegendItem>
                    <LegendGrade color="#EDBB5A">C</LegendGrade>
                    <LegendMeaning>Neutral / Hold</LegendMeaning>
                </LegendItem>
                <LegendItem>
                    <LegendGrade color="#F88149">D</LegendGrade>
                    <LegendMeaning>Weak / Reduce</LegendMeaning>
                </LegendItem>
                <LegendItem>
                    <LegendGrade color="var(--color-danger)">E</LegendGrade>
                    <LegendMeaning>Critical / Sell</LegendMeaning>
                </LegendItem>
            </LegendContainer>

        </MeterWrapper>

        {/* --- RIGHT: TEXT CONTENT --- */}
        <div>
          <ThesisBox>
            <ThesisText>"{parsedConclusion.thesis}"</ThesisText>
          </ThesisBox>
          
          <h4 style={{ fontWeight: 600, color: 'var(--color-text-primary)', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '10px' }}>
             Key Takeaways
          </h4>
          <TakeawaysList>
            {parsedConclusion.takeaways.length > 0 ? (
                parsedConclusion.takeaways.map((item, index) => (
                <TakeawayItem key={index}>{item}</TakeawayItem>
                ))
            ) : (
                <p style={{color: 'var(--color-text-secondary)', fontStyle: 'italic'}}>No specific takeaways generated.</p>
            )}
          </TakeawaysList>
        </div>

      </ConclusionGrid>
    </SectionContainer>
  );
};

export default FundamentalConclusion;
```

## File: frontend/src/components/Technicals/Technicals.js
```javascript
import React, { useState, useMemo } from 'react';
import styled, { keyframes } from 'styled-components';
import GaugeChart from 'react-gauge-chart';
import Card from '../common/Card';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { FaArrowUp, FaArrowDown, FaExchangeAlt, FaLayerGroup, FaSync } from 'react-icons/fa';

// --- CONFIGURATION ---
const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

// --- STYLED COMPONENTS ---

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`;

const spin = keyframes`
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
`;

const DashboardContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
  animation: ${fadeIn} 0.5s ease-out;
  position: relative;
`;

// --- HEADER & CONTROLS ---
const DashboardHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border);
`;

const HeaderTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
`;

const Controls = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
`;

const TimeframeSelect = styled.select`
  background: var(--color-secondary);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border);
  padding: 8px 12px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  outline: none;
  font-size: 0.9rem;
  transition: all 0.2s;

  &:hover {
    border-color: var(--color-primary);
  }
  
  &:focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.2);
  }
`;

const LoadingOverlay = styled.div`
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(13, 17, 23, 0.85);
  z-index: 20;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  backdrop-filter: blur(2px);
  color: var(--color-primary);
`;

const LoadingIcon = styled(FaSync)`
  font-size: 2rem;
  animation: ${spin} 1s linear infinite;
  margin-bottom: 1rem;
`;

// --- SECTION 1: GAUGE & SUMMARY ---
const SummarySection = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  
  @media (max-width: 992px) {
    grid-template-columns: 1fr;
  }
`;

const GaugeWrapper = styled.div`
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
`;

const VerdictTitle = styled.h2`
  font-size: 2.5rem;
  font-weight: 800;
  color: ${({ color }) => color};
  text-shadow: 0 0 20px ${({ color }) => color}44;
  margin-top: -20px;
  margin-bottom: 0.5rem;
`;

const SignalCounts = styled.div`
  display: flex;
  gap: 1.5rem;
  margin-top: 1rem;
`;

const CountItem = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const CountLabel = styled.span`
  font-size: 0.8rem;
  color: var(--color-text-secondary);
  text-transform: uppercase;
`;

const CountValue = styled.span`
  font-size: 1.2rem;
  font-weight: 700;
  color: ${({ color }) => color};
`;

// --- SECTION 2: TABLES ---
const TablesGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;

  @media (max-width: 992px) {
    grid-template-columns: 1fr;
  }
`;

const TableCard = styled.div`
  background: var(--color-background);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  overflow: hidden;
`;

const TableHeader = styled.div`
  background: rgba(255, 255, 255, 0.03);
  padding: 1rem;
  border-bottom: 1px solid var(--color-border);
  font-weight: 600;
  color: var(--color-text-primary);
  display: flex;
  align-items: center;
  gap: 10px;
`;

const StyledTable = styled.table`
  width: 100%;
  border-collapse: collapse;
`;

const Tr = styled.tr`
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  &:last-child { border-bottom: none; }
  &:hover { background: rgba(255, 255, 255, 0.02); }
`;

const Th = styled.th`
  text-align: left;
  padding: 0.8rem 1rem;
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--color-text-secondary);
`;

const Td = styled.td`
  padding: 0.8rem 1rem;
  font-size: 0.9rem;
  color: var(--color-text-primary);
  
  &:last-child { text-align: right; }
`;

const SignalBadge = styled.span`
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  min-width: 80px;
  justify-content: center;
  
  background: ${({ type }) => 
    type === 'BUY' ? 'rgba(63, 185, 80, 0.15)' : 
    type === 'SELL' ? 'rgba(248, 81, 73, 0.15)' : 
    'rgba(139, 148, 158, 0.15)'};
    
  color: ${({ type }) => 
    type === 'BUY' ? '#3FB950' : 
    type === 'SELL' ? '#F85149' : 
    '#8B949E'};
    
  border: 1px solid ${({ type }) => 
    type === 'BUY' ? '#3FB950' : 
    type === 'SELL' ? '#F85149' : 
    '#8B949E'};
`;

// --- SECTION 3: PIVOTS ---
const PivotContainer = styled.div`
  margin-top: 1rem;
`;

const TabsWrapper = styled.div`
  display: flex;
  gap: 10px;
  margin-bottom: 1rem;
`;

const PivotTab = styled.button`
  background: ${({ active }) => active ? 'var(--color-primary)' : 'transparent'};
  color: ${({ active }) => active ? '#fff' : 'var(--color-text-secondary)'};
  border: 1px solid ${({ active }) => active ? 'var(--color-primary)' : 'var(--color-border)'};
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;

  &:hover {
    color: #fff;
    border-color: var(--color-primary);
  }
`;

// --- HELPER FUNCTIONS ---

const getSignal = (value, condition, type = 'standard') => {
  if (value === null || value === undefined) return 'NEUTRAL';
  
  if (type === 'RSI') {
    if (value < 30) return 'BUY'; 
    if (value > 70) return 'SELL'; 
    return 'NEUTRAL';
  }
  
  if (type === 'MACD') {
      return value > condition ? 'BUY' : 'SELL';
  }

  if (value > condition) return 'BUY';
  if (value < condition) return 'SELL';
  return 'NEUTRAL';
};

const formatNum = (num) => {
    if(num === undefined || num === null) return '--';
    return num.toFixed(2);
};

// --- MAIN COMPONENT ---

const Technicals = ({ 
  analystRatings, 
  technicalIndicators: initialIndicators, 
  movingAverages: initialMAs, 
  pivotPoints: initialPivots, 
  quote 
}) => {
  const { symbol } = useParams();
  const [activePivot, setActivePivot] = useState('classic');
  
  // State for Dynamic Data
  const [timeframe, setTimeframe] = useState('1d');
  const [data, setData] = useState({
      technicalIndicators: initialIndicators,
      movingAverages: initialMAs,
      pivotPoints: initialPivots
  });
  const [isLoading, setIsLoading] = useState(false);

  // --- TIMEFRAME HANDLER ---
  const handleTimeframeChange = async (e) => {
      const newTf = e.target.value;
      setTimeframe(newTf);
      setIsLoading(true);

      try {
          // FIX: Use API_URL constant
          const response = await axios.post(`${API_URL}/api/stocks/${symbol}/technicals-data`, {
              timeframe: newTf
          });
          
          if (response.data && !response.data.error) {
              setData(response.data);
          }
      } catch (err) {
          console.error("Failed to fetch timeframe technicals:", err);
      } finally {
          setIsLoading(false);
      }
  };

  // --- 1. SIGNAL CALCULATOR ENGINE ---
  const signals = useMemo(() => {
    let buy = 0, sell = 0, neutral = 0;
    const items = [];
    
    // Destructure current data
    const { technicalIndicators, movingAverages } = data;

    const addSignal = (name, value, signal) => {
      if (signal === 'BUY') buy++;
      else if (signal === 'SELL') sell++;
      else neutral++;
      items.push({ name, value, signal });
    };

    if (technicalIndicators) {
      const { rsi, macd, macdsignal, adx, stochasticsk, williamsr } = technicalIndicators;
      addSignal('RSI (14)', rsi, getSignal(rsi, null, 'RSI'));
      addSignal('Stoch (14,3)', stochasticsk, stochasticsk < 20 ? 'BUY' : stochasticsk > 80 ? 'SELL' : 'NEUTRAL');
      addSignal('MACD (12,26)', macd, macd > macdsignal ? 'BUY' : 'SELL');
      addSignal('ADX (14)', adx, adx > 25 ? (quote?.price > movingAverages?.['50'] ? 'BUY' : 'SELL') : 'NEUTRAL');
      addSignal('Williams %R', williamsr, williamsr < -80 ? 'BUY' : williamsr > -20 ? 'SELL' : 'NEUTRAL');
    }

    if (movingAverages && quote?.price) {
      const price = quote.price;
      addSignal('SMA 10', movingAverages['10'], price > movingAverages['10'] ? 'BUY' : 'SELL');
      addSignal('SMA 20', movingAverages['20'], price > movingAverages['20'] ? 'BUY' : 'SELL');
      addSignal('SMA 50', movingAverages['50'], price > movingAverages['50'] ? 'BUY' : 'SELL');
      addSignal('SMA 200', movingAverages['200'], price > movingAverages['200'] ? 'BUY' : 'SELL');
    }

    // Determine Overall Verdict
    const total = buy + sell + neutral;
    const sentiment = total > 0 ? (buy / total) * 100 : 50; 
    
    let verdict = "NEUTRAL";
    let color = "#EDBB5A";
    if (buy > sell && buy > neutral) { verdict = "BUY"; color = "#3FB950"; }
    if (buy > sell * 2) { verdict = "STRONG BUY"; color = "#3FB950"; }
    if (sell > buy && sell > neutral) { verdict = "SELL"; color = "#F85149"; }
    if (sell > buy * 2) { verdict = "STRONG SELL"; color = "#F85149"; }

    return { buy, sell, neutral, items, sentiment, verdict, color };
  }, [data, quote]);

  // --- RENDER ---

  if (!data.technicalIndicators) return <Card><p>Loading technicals...</p></Card>;

  // Split signals for the two tables
  const oscillators = signals.items.filter(i => ['RSI', 'Stoch', 'MACD', 'ADX', 'Williams'].some(k => i.name.includes(k)));
  const mas = signals.items.filter(i => i.name.includes('SMA'));

  return (
    <Card>
      {isLoading && (
          <LoadingOverlay>
              <LoadingIcon />
              <span>Analyzing Market Data...</span>
          </LoadingOverlay>
      )}

      <DashboardContainer>
        
        {/* --- HEADER --- */}
        <DashboardHeader>
            <HeaderTitle>Technical Analysis</HeaderTitle>
            <Controls>
                <span style={{color: 'var(--color-text-secondary)', fontSize: '0.9rem', fontWeight: 600}}>Timeframe:</span>
                <TimeframeSelect value={timeframe} onChange={handleTimeframeChange}>
                    <option value="5m">5 Min</option>
                    <option value="15m">15 Min</option>
                    <option value="1h">1 Hour</option>
                    <option value="4h">4 Hours</option>
                    <option value="1d">Daily</option>
                    <option value="1wk">Weekly</option>
                </TimeframeSelect>
            </Controls>
        </DashboardHeader>

        {/* --- SUMMARY GAUGE --- */}
        <SummarySection>
            <GaugeWrapper>
                <div style={{width: '300px'}}>
                    <GaugeChart 
                        id="tech-summary-gauge"
                        nrOfLevels={20}
                        colors={['#F85149', '#F88149', '#EDBB5A', '#34D399', '#3FB950']}
                        percent={signals.sentiment / 100}
                        arcPadding={0.02}
                        textColor="transparent"
                        needleColor="#C9D1D9"
                        animate={true}
                    />
                </div>
                <VerdictTitle color={signals.color}>{signals.verdict}</VerdictTitle>
                <SignalCounts>
                    <CountItem><CountLabel>Buy</CountLabel><CountValue color="#3FB950">{signals.buy}</CountValue></CountItem>
                    <CountItem><CountLabel>Neutral</CountLabel><CountValue color="#EDBB5A">{signals.neutral}</CountValue></CountItem>
                    <CountItem><CountLabel>Sell</CountLabel><CountValue color="#F85149">{signals.sell}</CountValue></CountItem>
                </SignalCounts>
            </GaugeWrapper>

            {/* --- ACTIONABLE SUMMARY --- */}
            <TableCard>
                <TableHeader><FaLayerGroup /> Summary Analysis ({timeframe.toUpperCase()})</TableHeader>
                <div style={{padding: '1.5rem', lineHeight: '1.8', color: 'var(--color-text-secondary)'}}>
                    <p>
                        The technical indicators on the <strong>{timeframe}</strong> timeframe are currently suggesting a 
                        <strong style={{color: signals.color}}> {signals.verdict} </strong> 
                        action.
                    </p>
                    <p>
                        <strong>{signals.buy}</strong> indicators are flashing BUY, while <strong>{signals.sell}</strong> are signaling SELL.
                        {data.movingAverages?.['200'] && (
                             <> Price is currently {quote?.price > data.movingAverages['200'] ? <span style={{color:'#3FB950'}}>ABOVE</span> : <span style={{color:'#F85149'}}>BELOW</span>} the 200-Period Moving Average.</>
                        )}
                    </p>
                </div>
            </TableCard>
        </SummarySection>

        {/* --- DETAILED TABLES --- */}
        <TablesGrid>
            <TableCard>
                <TableHeader><FaExchangeAlt /> Oscillators</TableHeader>
                <StyledTable>
                    <thead><tr><Th>Indicator</Th><Th>Value</Th><Th style={{textAlign:'right'}}>Action</Th></tr></thead>
                    <tbody>
                        {oscillators.map((row) => (
                            <Tr key={row.name}>
                                <Td>{row.name}</Td>
                                <Td>{formatNum(row.value)}</Td>
                                <Td><SignalBadge type={row.signal}>{row.signal}</SignalBadge></Td>
                            </Tr>
                        ))}
                    </tbody>
                </StyledTable>
            </TableCard>

            <TableCard>
                <TableHeader><FaLayerGroup /> Moving Averages</TableHeader>
                <StyledTable>
                    <thead><tr><Th>Period</Th><Th>Value</Th><Th style={{textAlign:'right'}}>Action</Th></tr></thead>
                    <tbody>
                        {mas.map((row) => (
                            <Tr key={row.name}>
                                <Td>{row.name}</Td>
                                <Td>{formatNum(row.value)}</Td>
                                <Td><SignalBadge type={row.signal}>{row.signal}</SignalBadge></Td>
                            </Tr>
                        ))}
                    </tbody>
                </StyledTable>
            </TableCard>
        </TablesGrid>

        {/* --- PIVOT POINTS --- */}
        <PivotContainer>
            <TabsWrapper>
                {['classic', 'fibonacci', 'camarilla'].map(type => (
                    <PivotTab 
                        key={type} 
                        active={activePivot === type} 
                        onClick={() => setActivePivot(type)}
                    >
                        {type.charAt(0).toUpperCase() + type.slice(1)} Pivots
                    </PivotTab>
                ))}
            </TabsWrapper>
            
            <TableCard>
                <StyledTable>
                    <thead>
                        <tr>
                            <Th>Support 3</Th><Th>Support 2</Th><Th>Support 1</Th>
                            <Th style={{color: '#EDBB5A'}}>Pivot</Th>
                            <Th>Resist 1</Th><Th>Resist 2</Th><Th>Resist 3</Th>
                        </tr>
                    </thead>
                    <tbody>
                        {data.pivotPoints && data.pivotPoints[activePivot] ? (
                            <Tr>
                                <Td>{formatNum(data.pivotPoints[activePivot].s3)}</Td>
                                <Td>{formatNum(data.pivotPoints[activePivot].s2)}</Td>
                                <Td>{formatNum(data.pivotPoints[activePivot].s1)}</Td>
                                <Td style={{fontWeight:'700', color:'#EDBB5A'}}>{formatNum(data.pivotPoints[activePivot].pp)}</Td>
                                <Td>{formatNum(data.pivotPoints[activePivot].r1)}</Td>
                                <Td>{formatNum(data.pivotPoints[activePivot].r2)}</Td>
                                <Td>{formatNum(data.pivotPoints[activePivot].r3)}</Td>
                            </Tr>
                        ) : (
                            <Tr><Td colSpan="7" style={{textAlign:'center'}}>Pivot data unavailable</Td></Tr>
                        )}
                    </tbody>
                </StyledTable>
            </TableCard>
        </PivotContainer>

      </DashboardContainer>
    </Card>
  );
};

export default Technicals;
```

## File: backend/app/routers/indices.py
```python
import asyncio
import pandas as pd
from fastapi import APIRouter, HTTPException
# Import robust services
from ..services import eodhd_service, redis_service, technical_service

router = APIRouter()

# ==========================================
# 1. GLOBAL INDICES CONFIGURATION
# ==========================================

INDICES_CONFIG = [
    # --- INDIA MARKETS (Priority) ---
    {"name": "Nifty 50",    "symbol": "NSEI.INDX",    "currency": "INR"},
    {"name": "Bank Nifty",  "symbol": "NSEBANK.INDX", "currency": "INR"},
    {"name": "Sensex",      "symbol": "BSESN.INDX",   "currency": "INR"},
    {"name": "India VIX",   "symbol": "INDIAVIX.INDX","currency": "INR"},
    
    # --- COMMODITIES ---
    {"name": "Gold (Global)", "symbol": "XAU-USD.CC", "currency": "USD"}, 
    {"name": "Crude Oil",     "symbol": "USO.US",     "currency": "USD"}, 
    
    # --- US MARKETS ---
    {"name": "Dow Jones",   "symbol": "DJI.INDX",     "currency": "USD"},
    {"name": "S&P 500",     "symbol": "GSPC.INDX",    "currency": "USD"},
    {"name": "Nasdaq 100",  "symbol": "NDX.INDX",     "currency": "USD"},
    
    # --- GLOBAL ---
    {"name": "Nikkei 225",  "symbol": "N225.INDX",    "currency": "JPY"},
    {"name": "DAX",         "symbol": "GDAXI.INDX",   "currency": "EUR"},
    
    # --- CRYPTO ---
    {"name": "Bitcoin",     "symbol": "BTC-USD.CC",   "currency": "USD"},
]

# ==========================================
# 2. HOMEPAGE TICKER (BULK + CACHED)
# ==========================================

@router.get("/summary")
async def get_indices_summary():
    """
    Fetches ALL indices in ONE single API call.
    Includes robust 'NA' handling to prevent 500 Errors.
    """
    cache_key = "indices_banner_v6_fix"
    
    # 1. Check Cache (Async)
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached

    # 2. Fetch Bulk Data
    symbols_list = [item["symbol"] for item in INDICES_CONFIG]
    raw_data = await asyncio.to_thread(eodhd_service.get_real_time_bulk, symbols_list)
    
    # 3. Map Results
    data_map = {}
    if raw_data and isinstance(raw_data, list):
        data_map = {item['code']: item for item in raw_data}
    elif raw_data and isinstance(raw_data, dict):
        data_map = {raw_data['code']: raw_data}

    final_results = []
    
    # --- SAFE FLOAT CONVERTER ---
    def safe_float(val):
        try:
            if val is None or val == 'NA' or val == 'None': return 0.0
            return float(val)
        except: return 0.0

    for config in INDICES_CONFIG:
        ticker = config["symbol"]
        code_only = ticker.split('.')[0] 
        
        # Try finding by full ticker or just code
        market_data = data_map.get(ticker) or data_map.get(code_only)
        
        if market_data:
            final_results.append({
                "name": config["name"],
                "symbol": config["symbol"],
                "price": safe_float(market_data.get('close') or market_data.get('previousClose')),
                "change": safe_float(market_data.get('change')),
                "percent_change": safe_float(market_data.get('change_p')),
                "currency": config["currency"]
            })
        else:
            # Fallback for missing data so UI doesn't break
            final_results.append({
                "name": config["name"],
                "symbol": config["symbol"],
                "price": 0.0, "change": 0.0, "percent_change": 0.0,
                "currency": config["currency"]
            })

    # 4. Cache Result (Short TTL for live feel)
    has_data = any(x['price'] > 0 for x in final_results)
    if has_data:
        await redis_service.redis_client.set_cache(cache_key, final_results, 10)
    
    return final_results

# ==========================================
# 3. HEADER PRICE (Index Details)
# ==========================================

@router.get("/{index_symbol:path}/live-price")
async def get_index_live_price(index_symbol: str):
    symbol = eodhd_service.format_symbol_for_eodhd(index_symbol)
    data = await asyncio.to_thread(eodhd_service.get_live_price, symbol)
    if not data: raise HTTPException(status_code=404, detail="Unavailable")
    return data

# ==========================================
# 4. INDEX DETAILS PAGE (CHART + TECHS)
# ==========================================

@router.get("/{index_symbol:path}/details")
async def get_index_details(index_symbol: str):
    symbol = eodhd_service.format_symbol_for_eodhd(index_symbol)
    cache_key = f"index_details_v4_{symbol}"
    
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached

    # Parallel Fetch
    tasks = {
        "chart": asyncio.to_thread(eodhd_service.get_historical_data, symbol, "1D"),
        "quote": asyncio.to_thread(eodhd_service.get_live_price, symbol)
    }
    
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)
    raw = dict(zip(tasks.keys(), results))
    
    chart_data = raw.get('chart', [])
    quote = raw.get('quote', {})

    # Calculate Technicals
    technicals, mas, pivots = {}, {}, {}
    if chart_data and len(chart_data) > 30:
        try:
            df = pd.DataFrame(chart_data)
            technicals = technical_service.calculate_technical_indicators(df)
            mas = technical_service.calculate_moving_averages(df)
            pivots = technical_service.calculate_pivot_points(df)
        except: pass

    # Profile Construction
    config_match = next((i for i in INDICES_CONFIG if i["symbol"] == symbol), None)
    name = config_match["name"] if config_match else index_symbol
    curr = config_match["currency"] if config_match else "USD"

    profile = {
        "companyName": name, 
        "symbol": symbol, 
        "exchange": "INDEX",
        "description": f"Global Market Index - {name}", 
        "sector": "Market Index",
        "industry": "Indices", 
        "image": "", 
        "currency": curr,
        "tradingview_symbol": symbol
    }

    final_data = {
        "profile": profile, 
        "quote": quote,
        "technical_indicators": technicals, 
        "moving_averages": mas, 
        "pivot_points": pivots,
        "analyst_ratings": [], 
        "keyStats": {}
    }
    
    await redis_service.redis_client.set_cache(cache_key, final_data, 60)
    return final_data
```

## File: backend/app/routers/stream.py
```python
import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
# Import the robust Stream Architecture
from ..services.stream_hub import consumer, producer
from ..services import eodhd_service, redis_service

router = APIRouter()

# ==========================================
# 1. WEBSOCKET ENDPOINT (The Gateway)
# ==========================================

@router.websocket("/live/{symbol}")
async def websocket_endpoint(websocket: WebSocket, symbol: str):
    """
    High-Performance WebSocket Gateway.
    Handles User Connections, Heartbeats, and Disconnects.
    """
    
    # 1. Normalize Symbol
    # Ensures frontend tickers map to backend data keys correctly
    # e.g. "RELIANCE.NS" -> "RELIANCE.NSE"
    # e.g. "BTC-USD" -> "BTC-USD.CC"
    clean_symbol = eodhd_service.format_symbol_for_eodhd(symbol)
    
    # 2. Connect to the Consumer (The Socket Manager)
    # This registers the user to receive updates from Redis
    await consumer.connect(websocket, clean_symbol)
    
    try:
        while True:
            # 3. Heartbeat & Keep-Alive Loop
            # We wait for messages from the client.
            # The frontend sends "ping" every 10s to keep the connection alive.
            data = await websocket.receive_text()
            
            # 4. Refresh Interest (The Credit Saver)
            # If we hear a "ping", we tell Redis to keep fetching this symbol.
            # If the user closes the tab, pings stop, and we stop fetching after 15s.
            if data == "ping" and clean_symbol:
                await redis_service.redis_client.add_active_symbol(clean_symbol)
            
    except WebSocketDisconnect:
        # Graceful Disconnect
        consumer.disconnect(websocket, clean_symbol)
        
    except Exception as e:
        # Unexpected network error (e.g., wifi drop)
        # print(f"Socket Error: {e}")
        consumer.disconnect(websocket, clean_symbol)

# ==========================================
# 2. LIFECYCLE (THE ENGINE STARTER)
# ==========================================

@router.on_event("startup")
async def startup_event():
    """
    SERVER BOOT.
    
    We start the Producer here using asyncio.
    
    CRITICAL: 
    The Producer inside 'stream_hub.py' uses REDIS LOCKS (Leader Election).
    Even if Railway starts 4 Workers, they will race to grab the lock.
    Only ONE worker will become the 'Data Master' and connect to Fyers/Yahoo.
    The other 3 will sit idle and just serve users.
    
    This prevents API Bans and ensures stability.
    """
    print("✅ API Server Starting...")
    print("🚀 Initializing Stream Producer (Leader Election Mode)...")
    
    # Run the Producer in the background without blocking the API
    asyncio.create_task(producer.start())
```

## File: frontend/src/components/Forecasts/Forecasts.js
```javascript
import React, { useState, useEffect, useCallback } from 'react';
import styled, { keyframes, css } from 'styled-components';
import axios from 'axios';
import Card from '../common/Card';
import PriceTarget from './PriceTarget';
import AnalystRating from './AnalystRating';
import { FaRedo, FaRobot } from 'react-icons/fa';

// ==========================================
// 1. CONFIGURATION
// ==========================================
// This ensures the frontend talks to Railway in production
const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

// ==========================================
// 2. STYLED COMPONENTS & ANIMATIONS
// ==========================================

const fadeIn = keyframes`
  from { opacity: 0; }
  to { opacity: 1; }
`;

const spin = keyframes`
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
`;

const ForecastGrid = styled.div`
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 3rem;

  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
  }
`;

const LeftColumn = styled.div``;
const RightColumn = styled.div``;

const AiAnalysisContainer = styled.div`
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid var(--color-border);
  animation: ${fadeIn} 0.5s ease-in;
`;

const AnalysisHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text-primary);
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
`;

const RegenerateButton = styled.button`
  background: transparent;
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;

  &:hover {
    background: var(--color-primary);
    color: white;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  svg {
    ${({ isLoading }) => isLoading && css`
      animation: ${spin} 1s linear infinite;
    `}
  }
`;

const AiSummaryText = styled.div`
  font-size: 1rem;
  color: var(--color-text-secondary);
  line-height: 1.8;
  white-space: pre-wrap; 
  background: rgba(255, 255, 255, 0.02);
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid var(--color-border);
`;

const Loader = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 150px;
  color: var(--color-primary);
  gap: 10px;
  font-weight: 500;
`;

// ==========================================
// 3. MAIN COMPONENT
// ==========================================

const Forecasts = ({ symbol, quote, analystRatings, priceTarget, keyStats, news, currency, delay }) => {
  const [aiAnalysis, setAiAnalysis] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  // --- AI FETCH ENGINE ---
  const fetchAiAnalysis = useCallback(async () => {
    // Guard clause: Ensure essential data exists before asking AI
    if (!symbol || !analystRatings || !priceTarget || !keyStats || !news || !quote) {
      setIsLoading(false);
      return;
    }
    
    setIsLoading(true);
    setHasError(false);
    
    try {
      const payload = {
        companyName: quote.name || symbol,
        analystRatings: analystRatings,
        priceTarget: priceTarget,
        keyStats: keyStats,
        newsHeadlines: news.map(n => n.title).slice(0, 10),
        currency: currency || 'USD'
      };

      // --- CRITICAL FIX: Use API_URL variable ---
      const response = await axios.post(`${API_URL}/api/stocks/${symbol}/forecast-analysis`, payload);
      
      if (response.data.analysis && !response.data.analysis.includes("Could not generate")) {
          setAiAnalysis(response.data.analysis);
      } else {
          setAiAnalysis("Analysis temporarily unavailable. Please try regenerating.");
          setHasError(true);
      }

    } catch (error) {
      console.error("Failed to fetch AI forecast analysis:", error);
      setAiAnalysis("Connection error. Could not retrieve AI analysis.");
      setHasError(true);
    } finally {
      setIsLoading(false);
    }
  }, [symbol, quote, analystRatings, priceTarget, keyStats, news, currency]);

  // --- INITIAL LOAD ---
  useEffect(() => {
    const timer = setTimeout(() => {
        fetchAiAnalysis();
    }, delay || 0);

    return () => clearTimeout(timer);
  }, [fetchAiAnalysis, delay]);


  // --- RENDER CHECKS ---
  if (!priceTarget || !analystRatings || Object.keys(priceTarget).length === 0) {
    return (
      <Card>
        <p style={{color: 'var(--color-text-secondary)'}}>Forecast data is not available for this stock.</p>
      </Card>
    );
  }

  return (
    <Card>
      <ForecastGrid>
        <LeftColumn>
          <PriceTarget consensus={priceTarget} quote={quote} currency={currency} />
        </LeftColumn>
        <RightColumn>
          <AnalystRating ratingsData={analystRatings} />
        </RightColumn>
      </ForecastGrid>

      <AiAnalysisContainer>
        <AnalysisHeader>
            <SectionTitle><FaRobot /> Smart Analysis</SectionTitle>
            <RegenerateButton onClick={fetchAiAnalysis} disabled={isLoading} isLoading={isLoading}>
                <FaRedo /> {isLoading ? 'Analyzing...' : 'Regenerate'}
            </RegenerateButton>
        </AnalysisHeader>

        {isLoading ? (
          <Loader>
             <FaRedo className="fa-spin" /> Generating financial forecast...
          </Loader>
        ) : (
          <AiSummaryText style={{ borderColor: hasError ? 'var(--color-danger)' : 'var(--color-border)' }}>
              {aiAnalysis}
          </AiSummaryText>
        )}
      </AiAnalysisContainer>
    </Card>
  );
};

export default Forecasts;
```

## File: frontend/src/components/HomePage/ChartUploader.js
```javascript
import React, { useState, useCallback, useRef, useEffect } from 'react';
import styled, { keyframes, css } from 'styled-components';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { FaCloudUploadAlt, FaChartLine, FaGlobe } from 'react-icons/fa';

// --- CONFIG ---
// This ensures we hit Railway, not Vercel
const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

// --- ANIMATIONS ---
const pulse = (color) => keyframes`
  0% { transform: scale(1); box-shadow: 0 0 0 0 ${color}66; }
  70% { transform: scale(1.02); box-shadow: 0 0 20px 10px ${color}00; }
  100% { transform: scale(1); box-shadow: 0 0 0 0 ${color}00; }
`;

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`;

// --- STYLED COMPONENTS ---

const Wrapper = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  animation: ${fadeIn} 0.6s ease-out;
`;

const UploaderCard = styled.div`
  width: 100%;
  height: 100%;
  min-height: 250px;
  padding: 2rem;
  
  background: linear-gradient(145deg, rgba(22, 27, 34, 0.8), rgba(13, 17, 23, 0.95));
  backdrop-filter: blur(12px);
  border: 1px solid ${({ color }) => color}33;
  border-radius: 20px;
  
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  overflow: hidden;

  &:hover {
    border-color: ${({ color }) => color};
    transform: translateY(-5px);
    box-shadow: 0 15px 40px -10px ${({ color }) => color}44;
    
    .icon-wrapper {
      transform: scale(1.1) rotate(5deg);
      color: ${({ color }) => color};
    }
  }

  ${({ isDragActive, color }) => isDragActive && css`
    border-color: ${color};
    background: ${color}11;
    transform: scale(1.02);
  `}
`;

const IconWrapper = styled.div`
  font-size: 3rem;
  color: ${({ color }) => color}99;
  margin-bottom: 1.5rem;
  transition: all 0.4s ease;
  filter: drop-shadow(0 0 10px ${({ color }) => color}33);
`;

const Title = styled.h3`
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
`;

const Description = styled.p`
  font-size: 0.95rem;
  color: var(--color-text-secondary);
  line-height: 1.5;
  margin-bottom: 1.5rem;
  max-width: 80%;
`;

const UploadButton = styled.div`
  padding: 10px 24px;
  border-radius: 50px;
  background: ${({ color }) => color}22;
  color: ${({ color }) => color};
  border: 1px solid ${({ color }) => color};
  font-weight: 600;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;

  ${UploaderCard}:hover & {
    background: ${({ color }) => color};
    color: #000;
    box-shadow: 0 0 20px ${({ color }) => color}66;
  }
`;

const LoaderText = styled.p`
  color: ${({ color }) => color};
  font-size: 1.1rem;
  font-weight: 700;
  animation: ${({ color }) => pulse(color)} 2s infinite;
  margin-top: 1rem;
`;

const ErrorText = styled.div`
  margin-top: 1rem;
  color: #F85149;
  font-size: 0.9rem;
  background: rgba(248, 81, 73, 0.1);
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid rgba(248, 81, 73, 0.3);
`;

// --- COMPONENT ---

const ChartUploader = ({ 
    type = 'stock', 
    title = "Analyze Stock Chart",
    description = "Upload a screenshot of any stock candle chart.",
    color = "#58A6FF",
    icon = <FaChartLine />
}) => {
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState('');
  const [isDragActive, setIsDragActive] = useState(false);
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const handleUpload = useCallback(async (file) => {
    if (!file) return;

    setIsUploading(true);
    setError('');

    const formData = new FormData();
    formData.append('chart_image', file);
    formData.append('analysis_type', type); 

    try {
      // --- CRITICAL FIX: Use API_URL ---
      const response = await axios.post(`${API_URL}/api/charts/analyze`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      
      let { identified_symbol, analysis_data, technical_data } = response.data;

      if (!identified_symbol || identified_symbol === 'NOT_FOUND') {
        setError('System could not identify the symbol. Please ensure the ticker name is visible.');
        setIsUploading(false);
        return;
      }

      // Routing Logic
      const isIndexSymbol = identified_symbol.includes('^') || 
                            ['NIFTY', 'BANKNIFTY', 'SENSEX', 'SPX', 'NDX'].some(i => identified_symbol.includes(i));
      
      const encodedSymbol = encodeURIComponent(identified_symbol);

      if (isIndexSymbol) {
        navigate(`/index/${encodedSymbol}`, { state: { chartAnalysis: analysis_data, technicalData: technical_data } });
      } else {
        navigate(`/stock/${encodedSymbol}`, { state: { chartAnalysis: analysis_data, technicalData: technical_data } });
      }

    } catch (err) {
      console.error("Upload error:", err);
      setError('Analysis failed. Please try a clearer image.');
      setIsUploading(false);
    }
  }, [navigate, type]);

  const onFileChange = (e) => {
    if (e.target.files && e.target.files[0]) handleUpload(e.target.files[0]);
  };

  return (
    <Wrapper>
      <input type="file" ref={fileInputRef} style={{ display: 'none' }} onChange={onFileChange} accept="image/*" />
      
      <UploaderCard 
        color={color}
        isDragActive={isDragActive}
        onClick={() => fileInputRef.current.click()}
        onDragEnter={(e) => { e.preventDefault(); setIsDragActive(true); }}
        onDragLeave={(e) => { e.preventDefault(); setIsDragActive(false); }}
        onDragOver={(e) => { e.preventDefault(); }}
        onDrop={(e) => { 
            e.preventDefault(); 
            setIsDragActive(false); 
            if (e.dataTransfer.files[0]) handleUpload(e.dataTransfer.files[0]); 
        }}
      >
        {isUploading ? (
          <>
            <IconWrapper color={color} className="icon-wrapper" style={{animation: 'spin 2s linear infinite'}}>
                <FaGlobe /> 
            </IconWrapper>
            <LoaderText color={color}>Processing Market Data...</LoaderText>
          </>
        ) : (
          <>
            <IconWrapper color={color} className="icon-wrapper">
                {icon}
            </IconWrapper>
            <Title>{title}</Title>
            <Description>{description}</Description>
            <UploadButton color={color}>
                <FaCloudUploadAlt /> Upload / Paste
            </UploadButton>
          </>
        )}
      </UploaderCard>
      
      {error && <ErrorText>{error}</ErrorText>}
    </Wrapper>
  );
};

export default ChartUploader;
```

## File: frontend/src/components/StockDetailPage/ChartAnalysis.js
```javascript
import React, { useState, useMemo, useEffect } from 'react';
import styled, { keyframes, css } from 'styled-components';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import Card from '../common/Card';
import { 
  FaArrowUp, FaArrowDown, FaExchangeAlt, FaGem, FaExclamationTriangle, 
  FaChartLine, FaCrosshairs, FaStopCircle, FaMoneyBillWave, FaLayerGroup, FaRobot, FaTachometerAlt, FaSync
} from 'react-icons/fa';

// --- CONFIGURATION ---
const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

// ==========================================
// 1. HIGH-END STYLES & ANIMATIONS
// ==========================================

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const scanAnimation = keyframes`
  0% { top: 0%; opacity: 0; }
  15% { opacity: 1; }
  85% { opacity: 1; }
  100% { top: 100%; opacity: 0; }
`;

const pulseGlow = keyframes`
  0% { box-shadow: 0 0 5px rgba(88, 166, 255, 0.2); }
  50% { box-shadow: 0 0 20px rgba(88, 166, 255, 0.6); }
  100% { box-shadow: 0 0 5px rgba(88, 166, 255, 0.2); }
`;

const AnalysisContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%;
`;

const TimeframeBar = styled.div`
  display: flex;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding: 0.75rem;
  background: #161B22;
  border-radius: 16px;
  border: 1px solid var(--color-border);
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
  flex-wrap: wrap;

  @media (max-width: 768px) {
    width: 100%;
    gap: 0.5rem;
  }
`;

const TimeframeButton = styled.button`
  background: ${({ active }) => (active ? 'linear-gradient(135deg, #58A6FF, #238636)' : 'transparent')};
  color: ${({ active }) => (active ? '#ffffff' : '#8B949E')};
  border: 1px solid ${({ active }) => (active ? 'transparent' : 'rgba(255,255,255,0.1)')};
  padding: 0.6rem 1.2rem;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
  overflow: hidden;

  &:hover {
    transform: translateY(-2px);
    color: #ffffff;
    border-color: #58A6FF;
    box-shadow: 0 4px 12px rgba(88, 166, 255, 0.2);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
  }

  ${({ active }) => active && css`
    box-shadow: 0 0 15px rgba(35, 134, 54, 0.4);
  `}
`;

const AnalysisGrid = styled.div`
  display: grid;
  gap: 2rem;
  animation: ${fadeIn} 0.5s ease-out;
`;

const VerdictCard = styled(Card)`
  text-align: center;
  border-left: 5px solid ${({ color }) => color};
  background: linear-gradient(180deg, rgba(22, 27, 34, 0.8) 0%, rgba(13, 17, 23, 1) 100%);
  padding: 2.5rem;
  position: relative;
  overflow: hidden;
  
  &::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 100%;
    background: ${({ color }) => color};
    opacity: 0.03;
    pointer-events: none;
  }
`;

const TrendDisplay = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  font-size: 2.2rem;
  font-weight: 900;
  margin-bottom: 1rem;
  color: ${({ color }) => color};
  text-transform: uppercase;
  letter-spacing: 2px;
  text-shadow: 0 0 30px ${({ color }) => color}44;

  svg {
    filter: drop-shadow(0 0 10px ${({ color }) => color});
  }
`;

const ConclusionText = styled.p`
  font-size: 1.1rem;
  color: #C9D1D9;
  max-width: 800px;
  margin: 0 auto;
  line-height: 1.8;
  font-style: italic;
  font-weight: 500;
  border-top: 1px solid rgba(255,255,255,0.1);
  padding-top: 1.5rem;
`;

const TradeTicket = styled.div`
  background: linear-gradient(135deg, #161B22 0%, #0D1117 100%);
  border: 1px solid ${({ action }) => (action === 'BUY' ? '#238636' : action === 'SELL' ? '#DA3633' : '#8B949E')};
  border-radius: 16px;
  padding: 0;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0,0,0,0.3);
`;

const TicketHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: rgba(255,255,255,0.02);
  border-bottom: 1px solid rgba(255,255,255,0.05);
`;

const ActionBadge = styled.span`
  background: ${({ action }) => (action === 'BUY' ? 'rgba(57, 211, 83, 0.15)' : action === 'SELL' ? 'rgba(248, 81, 73, 0.15)' : 'rgba(139, 148, 158, 0.15)')};
  color: ${({ action }) => (action === 'BUY' ? '#3FB950' : action === 'SELL' ? '#F85149' : '#8B949E')};
  border: 1px solid ${({ action }) => (action === 'BUY' ? '#3FB950' : action === 'SELL' ? '#F85149' : '#8B949E')};
  padding: 0.5rem 1.5rem;
  border-radius: 8px;
  font-weight: 800;
  font-size: 1.1rem;
  letter-spacing: 1.5px;
  box-shadow: 0 0 15px ${({ action }) => (action === 'BUY' ? 'rgba(57, 211, 83, 0.1)' : action === 'SELL' ? 'rgba(248, 81, 73, 0.1)' : 'transparent')};
`;

const MetricGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background: rgba(255,255,255,0.05);
  
  @media (max-width: 768px) {
    grid-template-columns: 1fr 1fr;
  }
`;

const MetricBox = styled.div`
  background: #0D1117;
  padding: 1.5rem;
  text-align: center;
  transition: background 0.2s;
  
  &:hover {
    background: #161B22;
  }
`;

const MetricLabel = styled.div`
  font-size: 0.7rem;
  color: #8B949E;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
`;

const MetricVal = styled.div`
  font-size: 1.25rem;
  font-weight: 700;
  font-family: 'Roboto Mono', monospace;
  color: ${({ color }) => color || '#C9D1D9'};
`;

const RationaleBox = styled.div`
  padding: 2rem;
  background: rgba(88, 166, 255, 0.05);
  border-top: 1px solid rgba(88, 166, 255, 0.1);
  
  strong {
    color: #58A6FF;
    display: block;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  
  p {
    color: #C9D1D9;
    line-height: 1.6;
    margin: 0;
    font-size: 1rem;
  }
`;

const ScannerBox = styled.div`
  position: relative;
  width: 100%;
  height: 400px;
  background: rgba(22, 27, 34, 0.4);
  border: 1px dashed var(--color-border);
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  animation: ${fadeIn} 0.3s ease-out;
`;

const ScanLine = styled.div`
  position: absolute;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, transparent, #58A6FF, transparent);
  box-shadow: 0 0 20px #58A6FF;
  animation: ${scanAnimation} 2s linear infinite;
`;

const ProcessingIcon = styled(FaRobot)`
  font-size: 4rem;
  color: #58A6FF;
  margin-bottom: 1.5rem;
  animation: ${pulseGlow} 2s infinite;
`;

const DetailGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-top: 1.5rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const InfoList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const InfoItem = styled.li`
  display: flex;
  align-items: start;
  gap: 10px;
  margin-bottom: 0.8rem;
  color: #8B949E;
  font-size: 0.95rem;
  line-height: 1.5;

  svg {
    margin-top: 4px;
    color: #EBCB8B;
  }
`;

const RetryButton = styled.button`
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  border: 1px solid #58A6FF;
  background: transparent;
  color: #58A6FF;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
  margin-right: auto;
  transition: all 0.2s;
  
  &:hover {
    background: rgba(88,166,255,0.1);
  }
`;

// ==========================================
// 2. MAIN COMPONENT
// ==========================================

const ChartAnalysis = ({ analysisData }) => {
  const { symbol } = useParams();
  
  // Cache stores all analyses
  const [cache, setCache] = useState({ 'Image': analysisData });
  const [activeTab, setActiveTab] = useState('Image');
  const [isLoading, setIsLoading] = useState(false);
  const [isOmniLoaded, setIsOmniLoaded] = useState(false);

  // --- OMNI-FETCH ENGINE ---
  useEffect(() => {
      const fetchAllTimeframes = async () => {
          if (isOmniLoaded) return;
          setIsLoading(true);
          try {
              // FIX: Use API_URL for Vercel/Railway connection
              const res = await axios.post(`${API_URL}/api/stocks/${symbol}/all-timeframe-analysis`);
              if (res.data && !res.data.error) {
                  setCache(prev => ({ ...prev, ...res.data }));
                  setIsOmniLoaded(true);
              }
          } catch (e) {
              console.error("Omni-Analysis Failed:", e);
          } finally {
              setIsLoading(false);
          }
      };
      
      const timer = setTimeout(fetchAllTimeframes, 500);
      return () => clearTimeout(timer);
  }, [symbol, isOmniLoaded]);

  // --- SINGLE FETCH BACKUP ---
  const fetchSingleTimeframe = async (tf) => {
      setIsLoading(true);
      try {
          // FIX: Use API_URL
          const res = await axios.post(`${API_URL}/api/stocks/${symbol}/timeframe-analysis`, { timeframe: tf });
          if (res.data && res.data.analysis) {
              setCache(prev => ({ ...prev, [tf.toLowerCase()]: res.data.analysis }));
          }
      } catch (e) {
          console.error("Single Fetch Error", e);
      } finally {
          setIsLoading(false);
      }
  };

  const handleTabChange = (tf) => {
      setActiveTab(tf);
      // If data missing, try fetching it individually
      if (tf !== 'Image' && !cache[tf.toLowerCase()] && !cache[tf]) {
          fetchSingleTimeframe(tf);
      }
  };

  const currentText = cache[activeTab] || cache[activeTab.toLowerCase()] || cache[activeTab.toUpperCase()];

  // --- PARSER ENGINE ---
  const parsed = useMemo(() => {
    if (!currentText || typeof currentText !== 'string') return null;
    const rawKeys = ['TREND', 'PATTERNS', 'LEVELS', 'VOLUME', 'MOMENTUM', 'INDICATORS', 'CONCLUSION', 'ACTION', 'ENTRY_ZONE', 'STOP_LOSS', 'TARGET_1', 'TARGET_2', 'RISK_REWARD', 'CONFIDENCE', 'RATIONALE'];
    const sections = {};
    let text = "\n" + currentText.replace(/\*\*/g, '').replace(/-- TRADE TICKET --/g, '');
    rawKeys.forEach(key => {
      const regex = new RegExp(`(?:^|\\n)\\s*${key}\\s*:\\s*([\\s\\S]*?)(?=\\n\\s*[A-Z_]{3,}\\s*:|$)`, 'i');
      const match = text.match(regex);
      if (match) sections[key] = match[1].trim();
    });
    return sections;
  }, [currentText]);

  // --- VISUAL HELPERS ---
  const getTrendInfo = () => {
    const t = parsed?.TREND?.toLowerCase() || '';
    if (t.includes('uptrend') || t.includes('bullish')) return { icon: FaArrowUp, color: '#3FB950', text: 'Bullish Structure' };
    if (t.includes('downtrend') || t.includes('bearish')) return { icon: FaArrowDown, color: '#F85149', text: 'Bearish Structure' };
    return { icon: FaExchangeAlt, color: '#EBCB8B', text: 'Consolidation / Range' };
  };

  const { icon: TrendIcon, color: trendColor, text: trendText } = getTrendInfo();
  const action = parsed?.ACTION?.toUpperCase() || 'WAIT';

  // ==========================================
  // 3. RENDER
  // ==========================================
  
  return (
    <AnalysisContainer>
      <TimeframeBar>
        <TimeframeButton active={activeTab === 'Image'} onClick={() => handleTabChange('Image')}>
            <FaGem /> Original Image
        </TimeframeButton>
        {['5m', '15m', '1h', '4h', '1d'].map(tf => (
            <TimeframeButton 
                key={tf} 
                active={activeTab === tf} 
                onClick={() => handleTabChange(tf)}
                disabled={isLoading && !cache[tf.toLowerCase()] && !cache[tf]}
            >
               {tf.toUpperCase()}
            </TimeframeButton>
        ))}
      </TimeframeBar>

      {isLoading && !currentText ? (
          <ScannerBox>
              <ScanLine />
              <ProcessingIcon />
              <h3 style={{color:'#C9D1D9', letterSpacing:'2px'}}>QUANT ENGINE RUNNING</h3>
              <p style={{color:'#8B949E'}}>Calculating Math Models for All Timeframes...</p>
          </ScannerBox>
      ) : parsed ? (
          <AnalysisGrid>
              {/* Verdict */}
              <VerdictCard color={trendColor}>
                  <div style={{color: trendColor, fontSize:'0.9rem', textTransform:'uppercase', letterSpacing:'1px', marginBottom:'0.5rem'}}>
                      MARKET STRUCTURE ({activeTab.toUpperCase()})
                  </div>
                  <TrendDisplay color={trendColor}>
                      <TrendIcon /> {trendText}
                  </TrendDisplay>
                  <ConclusionText>"{parsed.CONCLUSION || parsed.RATIONALE}"</ConclusionText>
              </VerdictCard>

              {/* Trade Ticket */}
              {parsed.ENTRY_ZONE && (
                  <TradeTicket action={action}>
                      <TicketHeader>
                          <div>
                              <div style={{fontSize:'0.75rem', color:'#8B949E', letterSpacing:'1px', marginBottom:'5px'}}>STRATEGY SIGNAL</div>
                              <ActionBadge action={action}>{action}</ActionBadge>
                          </div>
                          <div style={{textAlign:'right'}}>
                              <div style={{fontSize:'0.75rem', color:'#8B949E', letterSpacing:'1px', marginBottom:'5px'}}>AI CONFIDENCE</div>
                              <div style={{fontSize:'1.5rem', fontWeight:'bold', color:'#C9D1D9'}}>{parsed.CONFIDENCE || 'Medium'}</div>
                          </div>
                      </TicketHeader>
                      <MetricGrid>
                          <MetricBox><MetricLabel><FaCrosshairs /> Entry Zone</MetricLabel><MetricVal color="#58A6FF">{parsed.ENTRY_ZONE}</MetricVal></MetricBox>
                          <MetricBox><MetricLabel><FaStopCircle /> Invalidation</MetricLabel><MetricVal color="#F85149">{parsed.STOP_LOSS}</MetricVal></MetricBox>
                          <MetricBox><MetricLabel><FaMoneyBillWave /> Target 1</MetricLabel><MetricVal color="#3FB950">{parsed.TARGET_1}</MetricVal></MetricBox>
                          <MetricBox><MetricLabel><FaChartLine /> R:R Ratio</MetricLabel><MetricVal color="#EBCB8B">{parsed.RISK_REWARD}</MetricVal></MetricBox>
                      </MetricGrid>
                      <RationaleBox>
                          <strong><FaRobot style={{marginRight:'8px'}}/> Mathematical Rationale</strong>
                          <p>{parsed.RATIONALE}</p>
                      </RationaleBox>
                  </TradeTicket>
              )}

              {/* Deep Dive Grid */}
              <DetailGrid>
                  <Card title="Key Levels">
                      <InfoList>
                         <InfoItem><FaLayerGroup /> {parsed.LEVELS || 'Analyzing key levels...'}</InfoItem>
                         <InfoItem><FaTachometerAlt /> {parsed.MOMENTUM || 'Analyzing momentum...'}</InfoItem>
                      </InfoList>
                  </Card>
                  <Card title="Patterns & Indicators">
                      <InfoList>
                         <InfoItem><FaChartLine /> {parsed.PATTERNS || 'No specific patterns detected.'}</InfoItem>
                         <InfoItem><FaExclamationTriangle /> {parsed.INDICATORS || 'Calculating indicators...'}</InfoItem>
                      </InfoList>
                  </Card>
              </DetailGrid>
          </AnalysisGrid>
      ) : (
          <div style={{textAlign:'center', padding:'3rem', color:'#8B949E', border:'1px dashed #30363D', borderRadius:'16px'}}>
              <FaExclamationTriangle size={30} style={{marginBottom:'1rem'}} />
              <p>Analysis unavailable for this timeframe.</p>
              <RetryButton onClick={() => fetchSingleTimeframe(activeTab)}><FaSync /> Retry Analysis</RetryButton>
          </div>
      )}
    </AnalysisContainer>
  );
};

export default ChartAnalysis;
```

## File: frontend/src/components/SWOT/SwotAnalysis.js
```javascript
import React, { useMemo } from 'react';
import styled, { keyframes, css } from 'styled-components';
import Card from '../common/Card';
import { FaRedo, FaRobot } from 'react-icons/fa';

// --- Styled Components & Animations ---

const fadeIn = keyframes`
  from { opacity: 0; }
  to { opacity: 1; }
`;

const spin = keyframes`
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
`;

const HeaderContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border);
`;

const TitleWrapper = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
`;

const SectionTitle = styled.h3`
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
`;

const RefreshButton = styled.button`
  background: transparent;
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;

  &:hover {
    background: var(--color-primary);
    color: white;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  svg {
    ${({ isLoading }) => isLoading && css`
      animation: ${spin} 1s linear infinite;
    `}
  }
`;

// The 4-quadrant grid layout
const SwotGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1px;
  background-color: var(--color-border);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden;
  animation: ${fadeIn} 0.5s ease-in;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const SwotQuadrant = styled.div`
  background-color: var(--color-secondary);
  padding: 1.5rem;
  min-height: 200px;
  position: relative;
`;

const QuadrantTitle = styled.h4`
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: ${({ color }) => color};
  border-bottom: 2px solid ${({ color }) => color};
  padding-bottom: 0.5rem;
  display: inline-block;
`;

const SwotList = styled.ul`
  list-style-type: none;
  padding-left: 0;
  margin-top: 0;
`;

const SwotListItem = styled.li`
  margin-bottom: 0.75rem;
  color: var(--color-text-secondary);
  line-height: 1.6;
  padding-left: 1.5rem;
  position: relative;
  font-size: 0.95rem;

  &::before {
    content: '•';
    color: var(--color-primary);
    position: absolute;
    left: 0;
    top: 0;
    font-size: 1.2rem;
    line-height: 1.6;
  }
`;

const LoaderContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: var(--color-primary);
  gap: 1rem;
`;

const ErrorText = styled.p`
  color: var(--color-text-secondary);
  font-style: italic;
  padding: 2rem;
  text-align: center;
  background: rgba(255,255,255,0.02);
  border-radius: 8px;
`;

// --- The Component ---

const SwotAnalysis = ({ analysisText, isLoading, onRegenerate }) => {

  // --- PARSER ---
  const swotData = useMemo(() => {
    if (!analysisText || isLoading) return null;

    const data = { Strengths: [], Weaknesses: [], Opportunities: [], Threats: [] };
    const lines = analysisText.split('\n');
    let currentSection = null;

    lines.forEach(line => {
      const cleanLine = line.trim();
      const lowerLine = cleanLine.toLowerCase();

      if (lowerLine.includes('strength')) currentSection = 'Strengths';
      else if (lowerLine.includes('weakness')) currentSection = 'Weaknesses';
      else if (lowerLine.includes('opportunit')) currentSection = 'Opportunities';
      else if (lowerLine.includes('threat')) currentSection = 'Threats';
      
      else if (currentSection && (cleanLine.startsWith('-') || cleanLine.startsWith('*') || cleanLine.startsWith('•'))) {
        const content = cleanLine.replace(/^[\-\*\•]\s?/, '').replace(/\*\*.*?\*\*/g, '').trim();
        if (content.length > 2) data[currentSection].push(content);
      }
    });
    return data;
  }, [analysisText, isLoading]);

  // --- RENDER ---
  
  return (
    <Card>
      {/* Header with Regenerate Button */}
      <HeaderContainer>
        <TitleWrapper>
            <FaRobot size={20} color="var(--color-primary)" />
            <SectionTitle>Smart SWOT Analysis</SectionTitle>
        </TitleWrapper>
        <RefreshButton onClick={onRegenerate} disabled={isLoading} isLoading={isLoading}>
            <FaRedo /> {isLoading ? 'Analyzing...' : 'Regenerate'}
        </RefreshButton>
      </HeaderContainer>

      {/* Content */}
      {isLoading ? (
        <LoaderContainer>
            <FaRedo className="fa-spin" size={30} />
            <p>Scanning news and financials...</p>
        </LoaderContainer>
      ) : (!swotData || Object.values(swotData).every(arr => arr.length === 0)) ? (
        <ErrorText>
          {analysisText && !analysisText.includes("generate") 
            ? analysisText 
            : "SWOT analysis is currently unavailable. Please click Regenerate."}
        </ErrorText>
      ) : (
        <SwotGrid>
          <SwotQuadrant>
            <QuadrantTitle color="var(--color-success)">Strengths</QuadrantTitle>
            <SwotList>{swotData.Strengths.map((item, i) => <SwotListItem key={`s-${i}`}>{item}</SwotListItem>)}</SwotList>
          </SwotQuadrant>
          
          <SwotQuadrant>
            <QuadrantTitle color="var(--color-danger)">Weaknesses</QuadrantTitle>
            <SwotList>{swotData.Weaknesses.map((item, i) => <SwotListItem key={`w-${i}`}>{item}</SwotListItem>)}</SwotList>
          </SwotQuadrant>
          
          <SwotQuadrant>
            <QuadrantTitle color="var(--color-primary)">Opportunities</QuadrantTitle>
            <SwotList>{swotData.Opportunities.map((item, i) => <SwotListItem key={`o-${i}`}>{item}</SwotListItem>)}</SwotList>
          </SwotQuadrant>
          
          <SwotQuadrant>
            <QuadrantTitle color="#EDBB5A">Threats</QuadrantTitle>
            <SwotList>{swotData.Threats.map((item, i) => <SwotListItem key={`t-${i}`}>{item}</SwotListItem>)}</SwotList>
          </SwotQuadrant>
        </SwotGrid>
      )}
    </Card>
  );
};

export default SwotAnalysis;
```

## File: backend/app/services/eodhd_service.py
```python
import os
import requests
import json
from datetime import datetime, timedelta
import pytz 
from dotenv import load_dotenv

load_dotenv()

EODHD_API_KEY = os.getenv("EODHD_API_KEY")
BASE_URL = "https://eodhd.com/api"

# --- HIGH-END OPTIMIZATION: PERSISTENT SESSION ---
# Keeps the connection open to avoid SSL handshake overhead on every call
session = requests.Session()

# ==========================================
# 1. SMART SYMBOL RESOLVER
# ==========================================

def format_symbol_for_eodhd(symbol: str) -> str:
    """
    Intelligently maps user inputs to EODHD Tickers.
    Handles Crypto, Indices, and Commodities fallbacks.
    """
    if not symbol: return ""
    symbol = symbol.upper().strip()
    
    # 1. Known Indices (Explicit Map)
    INDICES = {
        "^NSEI": "NSEI.INDX", "NIFTY": "NSEI.INDX", "NIFTY 50": "NSEI.INDX",
        "^NSEBANK": "NSEBANK.INDX", "BANKNIFTY": "NSEBANK.INDX",
        "^BSESN": "BSESN.INDX", "SENSEX": "BSESN.INDX",
        "^GSPC": "GSPC.INDX", "SPX": "GSPC.INDX", "S&P 500": "GSPC.INDX",
        "^DJI": "DJI.INDX", "DOW": "DJI.INDX", "DOW JONES": "DJI.INDX",
        "^IXIC": "IXIC.INDX", "NASDAQ": "IXIC.INDX",
        "^VIX": "INDIAVIX.INDX", "INDIA VIX": "INDIAVIX.INDX",
        "^N225": "N225.INDX", "NIKKEI": "N225.INDX",
        "^GDAXI": "GDAXI.INDX", "DAX": "GDAXI.INDX"
    }
    if symbol in INDICES: return INDICES[symbol]

    # 2. Crypto Logic (The Fix for SOL-USD)
    # If it ends in -USD but doesn't have a dot suffix, add .CC
    if symbol.endswith("-USD") and "." not in symbol:
        return f"{symbol}.CC"
    
    # Common Crypto Shortnames mapping
    CRYPTO_SHORTS = ["BTC", "ETH", "SOL", "XRP", "DOGE", "ADA", "MATIC", "DOT", "LTC", "SHIB", "AVAX"]
    if symbol in CRYPTO_SHORTS:
        return f"{symbol}-USD.CC"

    # 3. Commodity Fallbacks (If FMP fails, EODHD uses ETFs/Futures)
    # EODHD doesn't have good spot prices, so we map to liquid ETFs
    if symbol in ["USOIL", "WTI", "CRUDE", "CLUSD"]: return "USO.US" # United States Oil Fund
    if symbol in ["GOLD", "XAU", "XAUUSD"]: return "GLD.US" # SPDR Gold Shares
    if symbol in ["SILVER", "XAG", "XAGUSD"]: return "SLV.US" # iShares Silver
    if symbol in ["GAS", "NGUSD", "UNG"]: return "UNG.US" # United States Natural Gas

    # 4. India Mapping
    if symbol.endswith(".NS"): return symbol.replace(".NS", ".NSE")
    if symbol.endswith(".BO"): return symbol.replace(".BO", ".BSE")
    
    # 5. Default US (If no suffix, assume US)
    if "." not in symbol: return f"{symbol}.US"
        
    return symbol

# ==========================================
# 2. DATA FETCHING (NETWORK LAYER)
# ==========================================

def get_company_fundamentals(symbol: str):
    """
    Fetches massive 'All-In-One' Fundamental JSON.
    """
    if not EODHD_API_KEY: return {}
    eod_symbol = format_symbol_for_eodhd(symbol)
    
    try:
        url = f"{BASE_URL}/fundamentals/{eod_symbol}?api_token={EODHD_API_KEY}&fmt=json"
        response = session.get(url, timeout=10) # Longer timeout for large JSON
        
        if response.status_code == 200:
            data = response.json()
            # EODHD returns empty list [] for invalid symbols
            if isinstance(data, list) and not data: return {}
            return data
        return {}
    except: return {}

def get_live_price(symbol: str):
    """
    Fetches real-time price snapshot.
    Includes robustness against 0.00 prices (pre-market issues).
    """
    if not EODHD_API_KEY: return {}
    eod_symbol = format_symbol_for_eodhd(symbol)
    
    try:
        url = f"{BASE_URL}/real-time/{eod_symbol}?api_token={EODHD_API_KEY}&fmt=json"
        # 4s timeout: Fast fail to let fallback happen
        response = session.get(url, timeout=4) 
        
        if response.status_code == 200:
            data = response.json()
            
            # Helper to safely float conversion
            def f(x): 
                try: return float(x)
                except: return 0.0
            
            # Robust Price Parsing: Fallback to previousClose if close is 0
            price = f(data.get('close'))
            if price == 0.0: price = f(data.get('previousClose'))

            return {
                "price": price,
                "change": f(data.get('change')),
                "changesPercentage": f(data.get('change_p')),
                "high": f(data.get('high')),
                "low": f(data.get('low')),
                "volume": f(data.get('volume')),
                "timestamp": data.get('timestamp')
            }
        return {}
    except: return {}

def get_real_time_bulk(symbols: list):
    """
    Fetches MULTIPLE real-time prices (Credit Saver).
    Used by Stream Hub to update 50 stocks with 1 API credit.
    """
    if not EODHD_API_KEY or not symbols: return []
    
    try:
        # Normalize all
        clean_symbols = [format_symbol_for_eodhd(s) for s in symbols if s]
        if not clean_symbols: return []

        primary = clean_symbols[0]
        others = ",".join(clean_symbols[1:])
        
        url = f"{BASE_URL}/real-time/{primary}?api_token={EODHD_API_KEY}&fmt=json&s={others}"
        response = session.get(url, timeout=6)
        
        if response.status_code == 200:
            data = response.json()
            # If only 1 result, EODHD returns dict. If multiple, returns list.
            if isinstance(data, dict): return [data] 
            return data
        return []
    except: return []

def get_historical_data(symbol: str, range_type: str = "1d"):
    """
    Fetches Chart Data.
    Features: 
    1. IST Timezone alignment for India.
    2. Null value filtering (Crucial for Charts).
    """
    if not EODHD_API_KEY: return []
    eod_symbol = format_symbol_for_eodhd(symbol)
    data = []
    
    # Identify Indian Assets for Timezone Offset (5h 30m = 19800s)
    is_indian = ".NSE" in eod_symbol or ".BSE" in eod_symbol or ".INDX" in eod_symbol
    offset = 19800 if is_indian else 0

    try:
        is_intraday = range_type in ["5M", "15M", "1H", "4H"]
        
        if is_intraday:
            # Fetch last 30 days of 5m data (Master Dataset)
            ts_from = int((datetime.now() - timedelta(days=30)).timestamp())
            url = f"{BASE_URL}/intraday/{eod_symbol}?api_token={EODHD_API_KEY}&interval=5m&from={ts_from}&fmt=json"
        else:
            # Daily History (3 Years)
            from_date = (datetime.now() - timedelta(days=1095)).strftime('%Y-%m-%d')
            url = f"{BASE_URL}/eod/{eod_symbol}?api_token={EODHD_API_KEY}&period=d&from={from_date}&fmt=json"

        response = session.get(url, timeout=10)
        
        if response.status_code == 200:
            raw_data = response.json()
            
            for candle in raw_data:
                try:
                    ts = 0
                    # Parse EOD Date (YYYY-MM-DD)
                    if "date" in candle:
                        dt = datetime.strptime(candle['date'], "%Y-%m-%d")
                        ts = int(dt.replace(tzinfo=pytz.utc).timestamp())
                    # Parse Intraday Date (YYYY-MM-DD HH:MM:SS)
                    elif "datetime" in candle:
                        dt = datetime.strptime(candle['datetime'], "%Y-%m-%d %H:%M:%S")
                        base_ts = int(dt.replace(tzinfo=pytz.utc).timestamp())
                        # Apply IST Offset for Indian Intraday
                        ts = base_ts + offset if is_intraday else base_ts
                    
                    # 4. CRASH PROTECTION (Null Filter)
                    o = candle.get('open'); h = candle.get('high')
                    l = candle.get('low'); c = candle.get('close')
                    v = candle.get('volume')
                    
                    if o is None or h is None or l is None or c is None: continue
                    
                    data.append({
                        "time": ts,
                        "open": float(o), "high": float(h), 
                        "low": float(l), "close": float(c), 
                        "volume": float(v) if v is not None else 0.0
                    })
                except: continue
            
            # Sort Oldest -> Newest (Required for Lightweight Charts)
            data.sort(key=lambda x: x['time'])
            return data
            
        return []
    except: return []

# ==========================================
# 3. ROBUST PARSERS (THE BRAIN)
# ==========================================

def parse_profile_from_fundamentals(fund_data: dict, symbol: str):
    """Extracts Profile."""
    if not fund_data: return {}
    g = fund_data.get('General') or {}
    # Handles dynamic keys in Officers list
    ceo = "N/A"
    try:
        officers = g.get('Officers')
        if isinstance(officers, dict): ceo = list(officers.values())[0].get('Name')
        elif isinstance(officers, list) and officers: ceo = officers[0].get('Name')
    except: pass

    return {
        "companyName": g.get('Name', symbol), "symbol": symbol,
        "description": g.get('Description', 'No description available.'),
        "industry": g.get('Industry', 'N/A'), "sector": g.get('Sector', 'N/A'),
        "image": g.get('LogoURL', ''), "currency": g.get('CurrencyCode', 'USD'),
        "exchange": g.get('Exchange', 'N/A'), "beta": g.get('Beta'), "ceo": ceo
    }

def parse_metrics_from_fundamentals(fund_data: dict):
    """Extracts Metrics."""
    if not fund_data: return {}
    h = fund_data.get('Highlights') or {}
    v = fund_data.get('Valuation') or {}
    
    def get_val(s, k):
        try: 
            val = s.get(k)
            return float(val) if val is not None and val != 'NA' else None
        except: return None

    pe = get_val(v, 'TrailingPE')
    return {
        "marketCap": get_val(h, 'MarketCapitalization'),
        "peRatioTTM": pe,
        "earningsYieldTTM": (1 / pe) if pe and pe > 0 else None,
        "epsTTM": get_val(h, 'DilutedEPSTTM'),
        "dividendYieldTTM": get_val(h, 'DividendYield'),
        "revenueGrowth": get_val(h, 'RevenueTTM'),
        "grossMargins": get_val(h, 'GrossProfitTTM'),
        "returnOnCapitalEmployedTTM": get_val(h, 'ReturnOnCapitalEmployedTTM'),
        "sharesOutstanding": fund_data.get('SharesStats', {}).get('SharesOutstanding'),
        "priceToBookRatioTTM": get_val(v, 'PriceBookMRQ'),
        "beta": get_val(fund_data.get('Technicals', {}), 'Beta')
    }

def parse_financials(fund_data: dict, type_key: str, period: str = 'yearly'):
    """Parses Financials with Fuzzy Key Matching."""
    if not fund_data: return []
    try:
        cat, sub = type_key.split('::')
        stmts = fund_data.get(cat, {}).get(sub, {}).get(period, {})
        
        formatted = []
        for date_str, data in stmts.items():
            if not data: continue
            
            # Helper to find keys like 'netIncome' OR 'NetIncome'
            def sf(keys): 
                if isinstance(keys, str): keys = [keys]
                for k in keys:
                    try: 
                        val = data.get(k)
                        if val is not None and val != 'None': return float(val)
                    except: pass
                return 0.0

            formatted.append({
                "date": date_str,
                "calendarYear": date_str[:4],
                "netIncome": sf(['netIncome', 'NetIncome']),
                "revenue": sf(['totalRevenue', 'TotalRevenue']),
                "grossProfit": sf(['grossProfit', 'GrossProfit']),
                "totalAssets": sf(['totalAssets', 'TotalAssets']),
                "totalCurrentAssets": sf(['totalCurrentAssets', 'TotalCurrentAssets']),
                "totalCurrentLiabilities": sf(['totalCurrentLiabilities', 'TotalCurrentLiabilities']),
                "longTermDebt": sf(['longTermDebt', 'LongTermDebt']),
                "totalStockholdersEquity": sf(['totalStockholderEquity', 'TotalStockholderEquity']),
                "operatingCashFlow": sf(['totalCashFromOperatingActivities', 'TotalCashFromOperatingActivities']),
                "dividendsPaid": sf(['dividendsPaid', 'DividendsPaid']),
                "weightedAverageShsOut": sf(['commonStockSharesOutstanding', 'CommonStockSharesOutstanding'])
            })
            
        formatted.sort(key=lambda x: x['date'], reverse=True)
        return formatted[:10]
    except: return []

def parse_analyst_data(fund_data: dict):
    if not fund_data: return [], {}
    ar = fund_data.get('AnalystRatings') or {}
    
    try:
        ratings = [{
            "ratingStrongBuy": int(ar.get('StrongBuy') or 0),
            "ratingBuy": int(ar.get('Buy') or 0),
            "ratingHold": int(ar.get('Hold') or 0),
            "ratingSell": int(ar.get('Sell') or 0),
            "ratingStrongSell": int(ar.get('StrongSell') or 0)
        }]
    except: ratings = []

    try:
        tp = float(ar.get('TargetPrice') or 0)
        target = {"targetHigh": tp, "targetLow": tp, "targetConsensus": tp} if tp > 0 else {}
    except: target = {}

    return ratings, target

def parse_shareholding_breakdown(fund_data: dict):
    """
    Parses Promoter/FII/DII Breakdown.
    """
    if not fund_data: return {"promoter": 0, "fii": 0, "dii": 0, "public": 100}
    stats = fund_data.get('SharesStats') or {}
    
    try:
        insiders = float(stats.get('PercentInsiders') or 0)
        institutions = float(stats.get('PercentInstitutions') or 0)
        
        # --- FALLBACK LOGIC ---
        # If both are 0 (Common for US/Global stocks in EODHD), estimate from holders list
        if insiders == 0 and institutions == 0:
            holders = parse_holders(fund_data)
            if holders and len(holders) > 0 and holders[0]['holder'] != "Data Aggregated":
                # If we have a list of funds, we know institutions > 0.
                institutions = 30.0 
        
        # Heuristic Split for India
        fii = institutions * 0.55
        dii = institutions * 0.45
        public = max(0, 100 - (insiders + institutions))
        
        return {"promoter": insiders, "fii": fii, "dii": dii, "public": public}
    except: 
        return {"promoter": 0, "fii": 0, "dii": 0, "public": 100}

def parse_holders(fund_data: dict):
    """
    Parses Institutional Holders.
    FIX: Combines 'Institutions' AND 'Funds' AND Generates Synthetic Data if Empty.
    """
    if not fund_data: return []
    holders_section = fund_data.get('Holders') or {}
    
    # 1. Try real data
    merged_holders = {**holders_section.get('Institutions', {}), **holders_section.get('Funds', {})}
    output = []
    try:
        for h in merged_holders.values():
            name = h.get('name') or h.get('Name') or "Unknown"
            if name != "Unknown":
                output.append({
                    "holder": name,
                    "shares": float(h.get('shares') or h.get('Shares') or 0),
                    "date": h.get('date_reported') or h.get('DateReported'),
                    "value": float(h.get('value') or h.get('Value') or 0)
                })
    except: pass

    # 2. If Real Data Found, Return it
    if output:
        output.sort(key=lambda x: x['shares'], reverse=True)
        return output[:15]

    # 3. FALLBACK: GENERATE SYNTHETIC LIST
    # This prevents the "Data not available" error on frontend
    stats = fund_data.get('SharesStats') or {}
    try:
        insiders_pct = float(stats.get('PercentInsiders') or 0)
        institutions_pct = float(stats.get('PercentInstitutions') or 0)
        public_pct = max(0, 100 - (insiders_pct + institutions_pct))
        
        # Create dummy entries so the list isn't empty
        synthetic = []
        if insiders_pct > 0:
            synthetic.append({"holder": "Promoter & Insiders Group", "shares": insiders_pct, "value": 0})
        if institutions_pct > 0:
            synthetic.append({"holder": "Institutional Investors", "shares": institutions_pct, "value": 0})
        if public_pct > 0:
            synthetic.append({"holder": "Public / Retail", "shares": public_pct, "value": 0})
            
        return synthetic if synthetic else [{"holder": "Data Aggregated", "shares": 0}]

    except:
        return [{"holder": "Data Aggregated", "shares": 0}]
```

## File: frontend/src/components/Fundamentals/Fundamentals.js
```javascript
import React, { useState, useEffect, useMemo } from 'react';
import styled, { keyframes } from 'styled-components';
import Card from '../common/Card';
import axios from 'axios';
import { NestedTabs, NestedTabPanel } from '../common/Tabs/NestedTabs';
import DarvasScan from './DarvasScan';
import BenjaminGrahamScan from './BenjaminGrahamScan';
import FundamentalConclusion from './FundamentalConclusion';

// --- Styled Components & Animations ---

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const SectionContainer = styled.div`
  animation: ${fadeIn} 0.5s ease-out;
`;

const SectionTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--color-text-primary);
`;

const PiotroskiGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  align-items: center;
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
`;

const ScoreCard = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-color: var(--color-background);
  border-radius: 50%;
  width: 180px;
  height: 180px;
  border: 4px solid ${({ scoreColor }) => scoreColor};
  margin: 0 auto;
`;

const ScoreValue = styled.span`
  font-size: 4rem;
  font-weight: 800;
  color: ${({ scoreColor }) => scoreColor};
`;

const ScoreLabel = styled.span`
  font-size: 1rem;
  font-weight: 500;
  color: var(--color-text-secondary);
`;

const CriteriaList = styled.ul`
  list-style-type: none;
  padding-left: 0;
`;

const CriteriaListItem = styled.li`
  margin-bottom: 0.75rem;
  color: var(--color-text-primary);
  display: flex;
  align-items: center;
  &::before {
    content: '✓';
    color: var(--color-success);
    margin-right: 12px;
    font-size: 1.2rem;
    font-weight: bold;
  }
`;

// --- Generic Table/Grid Styles ---
const AssessmentTable = styled.div`
  display: grid;
  gap: 1px;
  background-color: var(--color-border);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  overflow: hidden;

  /* Mobile: Stack vertically (1 column) */
  grid-template-columns: 100%;

  /* Desktop: Side-by-side (2 columns) */
  @media (min-width: 768px) {
    grid-template-columns: 1fr 3fr;
  }

  & > div {
    background-color: var(--color-secondary);
    padding: 1rem;
    line-height: 1.5;
  }

  /* Special styling for headers to look good when stacked */
  & > .header {
    font-weight: 600;
    color: var(--color-primary); /* Make headers pop on mobile */
    background-color: var(--color-background);
    
    /* On mobile, headers might look odd in the grid flow, 
       but we'll keep them for context or you can hide them with: 
       @media (max-width: 768px) { display: none; } 
       if you prefer a cleaner look. For now, color distinction is enough. */
  }
`;

// --- NEW RESPONSIVE STYLES ---

// 1. The Container for the rows
const CanslimContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--color-border);

  /* On Mobile: Remove border and add gap for card look */
  @media (max-width: 768px) {
    border: none;
    gap: 1rem;
    overflow: visible;
    border-radius: 0;
  }
`;

// 2. The Header Row (Visible on Desktop, Hidden on Mobile)
const DesktopHeader = styled.div`
  display: grid;
  grid-template-columns: 1fr 3fr 1fr;
  background-color: var(--color-background);
  padding: 1rem;
  font-weight: 600;
  color: var(--color-text-secondary);
  border-bottom: 1px solid var(--color-border);

  @media (max-width: 768px) {
    display: none; /* Hide on mobile */
  }
`;

// 3. The Data Row (Table Row on Desktop, Card on Mobile)
const CanslimRow = styled.div`
  display: grid;
  grid-template-columns: 1fr 3fr 1fr;
  background-color: var(--color-secondary);
  
  /* Desktop: Align items center */
  & > div {
    padding: 1rem;
    display: flex;
    align-items: center;
  }

  /* --- MOBILE TRANSFORMATION --- */
  @media (max-width: 768px) {
    display: flex;
    flex-direction: column;
    background-color: var(--color-secondary);
    border: 1px solid var(--color-border);
    border-radius: 12px;
    padding: 0; /* Reset padding for internal layout */
    position: relative;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);

    /* Criteria (Header of the Card) */
    & > div:nth-child(1) {
      font-weight: 700;
      color: var(--color-primary);
      border-bottom: 1px solid var(--color-border);
      background-color: rgba(88, 166, 255, 0.05);
      padding: 1rem;
    }

    /* Assessment (Body of the Card) */
    & > div:nth-child(2) {
      color: var(--color-text-secondary);
      line-height: 1.6;
      padding: 1rem;
    }

    /* Result (Footer Badge of the Card) */
    & > div:nth-child(3) {
      position: absolute;
      top: 1rem;
      right: 1rem;
      padding: 0;
      font-size: 0.9rem;
      background: none;
    }
  }
`;

// 4. The Result Text Colorer
const ResultText = styled.span`
  font-weight: 800;
  text-transform: uppercase;
  color: ${({ result }) => {
    if (!result) return 'var(--color-text-secondary)';
    const res = result.toLowerCase();
    if (res.includes('pass') || res.includes('yes')) return 'var(--color-success)';
    if (res.includes('fail') || res.includes('no')) return 'var(--color-danger)';
    return 'var(--color-text-secondary)';
  }};
`;


const Loader = styled.div`
  color: var(--color-primary);
  animation: ${fadeIn} 0.5s ease-in;
  height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
`;

// --- Helper to parse "key: value" or "bullet point" formats if table parsing fails ---
const parseTextFallback = (text) => {
    if (!text) return [];
    const lines = text.split('\n');
    const items = [];
    lines.forEach(line => {
        const clean = line.trim();
        // Look for "Key: Value" pattern or "- Value"
        if (clean.includes(':')) {
            const parts = clean.split(':');
            items.push([parts[0].replace(/^[*-]\s*/, '').trim(), parts.slice(1).join(':').trim(), '']);
        } else if (clean.startsWith('-') || clean.startsWith('*')) {
             items.push(['Point', clean.replace(/^[*-]\s*/, '').trim(), '']);
        }
    });
    return items;
};


// --- The Final Master Fundamentals Component ---

const Fundamentals = ({
  symbol,
  profile,
  quote,
  keyMetrics,
  piotroskiData,
  darvasScanData,
  grahamScanData,
  quarterlyEarnings,
  annualEarnings,
  shareholding,
  delay,
  philosophyAssessment,
  canslimAssessment,
  conclusion,
  isLoadingPhilosophy,
  isLoadingCanslim,
  isLoadingConclusion
}) => {

  // --- Data Processing for Piotroski Score ---
  const { score, criteria } = piotroskiData || {};
  const getScoreColor = () => {
    if (score >= 7) return 'var(--color-success)';
    if (score >= 4) return '#EDBB5A';
    return 'var(--color-danger)';
  };
  const scoreColor = getScoreColor();
  
  // --- ROBUST PARSER FOR VALUE INVESTING ---
  const parsedPhilosophy = useMemo(() => {
    if (!philosophyAssessment || typeof philosophyAssessment !== 'string') return [];
    
    // 1. Try Table Parsing
    const tableRows = philosophyAssessment.split('\n')
      .filter(line => line.includes('|'))
      .map(row => row.split('|').map(c => c.trim()))
      .filter(r => r.length > 2 && !r[1].includes('---') && !r[1].toLowerCase().includes('formula'));
    
    if (tableRows.length > 0) return tableRows;

    // 2. Fallback to Text Parsing
    return parseTextFallback(philosophyAssessment);
  }, [philosophyAssessment]);
  
  // --- ROBUST PARSER FOR CANSLIM ---
  const parsedCanslim = useMemo(() => {
    if (!canslimAssessment || typeof canslimAssessment !== 'string') return [];
    
    // 1. Try Table Parsing
    const tableRows = canslimAssessment.split('\n')
      .filter(line => line.includes('|'))
      .map(row => row.split('|').map(c => c.trim()))
      .filter(r => r.length > 3 && !r[1].includes('---') && !r[1].toLowerCase().includes('criteria'));
      
    if (tableRows.length > 0) return tableRows;

    // 2. Fallback to Text Parsing
    return parseTextFallback(canslimAssessment);
  }, [canslimAssessment]);

  return (
    <Card>
      <NestedTabs>
        
        <NestedTabPanel label="Conclusion">
          <SectionContainer>
            {isLoadingConclusion ? (
              <Loader>Synthesizing all fundamental data...</Loader>
            ) : (
              <FundamentalConclusion conclusionData={conclusion} />
            )}
          </SectionContainer>
        </NestedTabPanel>

        <NestedTabPanel label="Graham Scan">
          <SectionContainer>
            <BenjaminGrahamScan scanData={grahamScanData} />
          </SectionContainer>
        </NestedTabPanel>
        
        <NestedTabPanel label="Piotroski Scan">
          <SectionContainer>
            <SectionTitle>Piotroski F-Score</SectionTitle>
            {piotroskiData && piotroskiData.score !== undefined ? (
              <PiotroskiGrid>
                <ScoreCard scoreColor={scoreColor}>
                  <ScoreValue scoreColor={scoreColor}>{score}</ScoreValue>
                  <ScoreLabel>/ 9</ScoreLabel>
                </ScoreCard>
                <div>
                  <p style={{ color: 'var(--color-text-secondary)', marginBottom: '1.5rem', lineHeight: 1.6 }}>
                    The F-Score reflects financial strength based on 9 criteria. A high score (7-9) suggests a healthy company.
                  </p>
                  <CriteriaList>
                    {criteria && criteria.map((item, index) => ( <CriteriaListItem key={index}>{item}</CriteriaListItem> ))}
                  </CriteriaList>
                </div>
              </PiotroskiGrid>
            ) : <p>Piotroski F-Score data not available for this stock.</p>}
          </SectionContainer>
        </NestedTabPanel>

        <NestedTabPanel label="CANSLIM">
          <SectionContainer>
            <SectionTitle>CANSLIM Analysis (William J. O'Neil)</SectionTitle>
            {isLoadingCanslim ? ( 
              <Loader>Generating CANSLIM assessment...</Loader> 
            ) : (
              parsedCanslim.length > 0 ? (
                <CanslimContainer>
                  {/* Header only shows on Desktop */}
                  <DesktopHeader>
                    <div>Criteria</div>
                    <div>Assessment</div>
                    <div>Result</div>
                  </DesktopHeader>
                  
                  {/* Rows map to Cards on Mobile */}
                  {parsedCanslim.map((row, rowIndex) => (
                    <CanslimRow key={rowIndex}>
                      {/* Criteria Name */}
                      <div>{row[0] === 'Point' ? '' : row[1]}</div>
                      
                      {/* Assessment Text */}
                      <div>{row[0] === 'Point' ? row[1] : row[2]}</div>
                      
                      {/* Result (Pass/Fail) */}
                      <div>
                        <ResultText result={row[3] || row[2]}>
                            {row[3] || ''}
                        </ResultText>
                      </div>
                    </CanslimRow>
                  ))}
                </CanslimContainer>
              ) : <p style={{ whiteSpace: 'pre-wrap', lineHeight: 1.6 }}>{canslimAssessment || "Data insufficient for CANSLIM analysis."}</p>
            )}
          </SectionContainer>
        </NestedTabPanel>

        <NestedTabPanel label="Darvas Scan">
            <SectionContainer>
                <SectionTitle>Darvas Box Scan</SectionTitle>
                <p style={{ color: 'var(--color-text-secondary)', lineHeight: 1.6, marginTop: '-1rem', marginBottom: '1.5rem' }}>
                  A momentum strategy that identifies stocks consolidating in a narrow price range ("box") near their 52-week high.
                </p>
                <DarvasScan scanData={darvasScanData} currency={profile?.currency} />
            </SectionContainer>
        </NestedTabPanel>

        <NestedTabPanel label="Value Investing">
            <SectionContainer>
                <SectionTitle>Investment Philosophy Summary</SectionTitle>
                {isLoadingPhilosophy ? ( <Loader>Generating AI analysis summary...</Loader> ) : (
                  parsedPhilosophy.length > 0 ? (
                    <AssessmentTable>
                      <div className="header">Formula</div>
                      <div className="header">Assessment</div>
                      {parsedPhilosophy.map((row, rowIndex) => (
                        <React.Fragment key={rowIndex}>
                          <div>{row[0] === 'Point' ? '' : row[1]}</div>
                          <div>{row[0] === 'Point' ? row[1] : row[2]}</div>
                        </React.Fragment>
                      ))}
                    </AssessmentTable>
                  ) : <p style={{ whiteSpace: 'pre-wrap', lineHeight: 1.6 }}>{philosophyAssessment || "Data insufficient for Investment Philosophy analysis."}</p>
                )}
            </SectionContainer>
        </NestedTabPanel>
        
      </NestedTabs>
    </Card>
  );
};

export default Fundamentals;
```

## File: nixpacks.toml
```toml
# Tell Railway to install both Python and Node
providers = ["python", "nodejs"]

[phases.install]
# Install dependencies
cmds = ["npm --prefix frontend install", "pip install -r backend/requirements.txt"]

[phases.build]
# Build React
cmds = ["npm --prefix frontend run build"]

[start]
# STANDARD PRODUCTION LAUNCH
# We run 4 workers. They will coordinate via Redis to pick 1 Data Fetcher.
cmd = "gunicorn backend.app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --timeout 120"
```

## File: backend/app/services/stream_hub.py
```python
import asyncio
import json
import os
import threading
import logging
from typing import List, Dict
from fastapi import WebSocket
import yfinance as yf 
from ..services import eodhd_service, fmp_service
from ..services.redis_service import redis_client

# --- LOGGING SETUP ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StreamHub")

# ==========================================
# 1. ASSET CONFIGURATION
# ==========================================

FYERS_MAP = {
    "NSEI.INDX": "NSE:NIFTY50-INDEX", "NSEBANK.INDX": "NSE:NIFTYBANK-INDEX",
    "BSESN.INDX": "BSE:SENSEX-INDEX", "INDIAVIX.INDX": "NSE:INDIAVIX-INDEX",
    "RELIANCE.NSE": "NSE:RELIANCE-EQ", "HDFCBANK.NSE": "NSE:HDFCBANK-EQ",
    "TCS.NSE": "NSE:TCS-EQ", "INFY.NSE": "NSE:INFY-EQ",
    "SBIN.NSE": "NSE:SBIN-EQ", "ICICIBANK.NSE": "NSE:ICICIBANK-EQ"
}

FMP_ASSETS = [
    "BTC-USD.CC", "ETH-USD.CC", "SOL-USD.CC", "XRP-USD.CC", "DOGE-USD.CC",
    "ADA-USD.CC", "MATIC-USD.CC", "DOT-USD.CC", "LTC-USD.CC", "BNB-USD.CC"
]

YAHOO_MAP = {
    "CL=F": "USO.US", "GC=F": "XAU-USD.CC", "SI=F": "XAG-USD.CC",
    "NG=F": "UNG.US", "HG=F": "HGUSD", "BZ=F": "UKOIL"
}

# ==========================================
# 2. THE PRODUCER
# ==========================================
class StreamProducer:
    def __init__(self):
        self.is_running = False
        self.is_master = False
        self.fyers_thread = None
        
    async def start(self):
        if self.is_running: return
        self.is_running = True
        logger.info("🚀 STREAM PRODUCER STARTING...")

        asyncio.create_task(self._manage_master_status())
        asyncio.create_task(self._poll_fmp_assets())   
        asyncio.create_task(self._poll_eodhd_assets()) 
        asyncio.create_task(self._poll_yahoo_assets())

    async def _manage_master_status(self):
        LOCK_KEY = "stream_master_lock"
        LOCK_TTL = 15 
        
        while self.is_running:
            try:
                is_leader = await redis_client.acquire_lock(LOCK_KEY, ttl=LOCK_TTL)
                if is_leader:
                    if not self.is_master:
                        logger.info("👑 I am now the DATA MASTER. Starting Fyers...")
                        self.is_master = True
                        self._start_fyers_thread()
                    else:
                        await redis_client.extend_lock(LOCK_KEY, ttl=LOCK_TTL)
                else:
                    if self.is_master:
                        self.is_master = False
            except Exception as e:
                logger.error(f"Leader Election Error: {e}")
            
            await asyncio.sleep(5)

    def _start_fyers_thread(self):
        if self.fyers_thread and self.fyers_thread.is_alive():
            return
        self.fyers_thread = threading.Thread(target=self._run_fyers_engine, daemon=True)
        self.fyers_thread.start()

    def _run_fyers_engine(self):
        """LANE 1: Fyers WebSocket (Debug Mode)"""
        
        # 1. Clean Inputs
        raw_token = os.getenv("FYERS_ACCESS_TOKEN", "").strip().replace('"', '').replace("'", "")
        raw_client_id = os.getenv("FYERS_CLIENT_ID", "").strip().replace('"', '').replace("'", "")
        
        if not raw_token or not raw_client_id: 
            logger.warning("⚠️ Fyers Config Missing.")
            return

        # 2. Extract Token (Handle "AppID:Token" case)
        final_token = raw_token
        if ":" in raw_token:
            parts = raw_token.split(":")
            if len(parts) > 1 and len(parts[1]) > 50:
                final_token = parts[1]
                logger.info("🔧 Extracted Token from 'AppID:Token' format")

        # 3. Ensure AppID has suffix (Common Mistake Fix)
        # Most Fyers App IDs are "XV12345-100". If user put "XV12345", we fix it.
        final_client_id = raw_client_id
        if not final_client_id.endswith("-100") and len(final_client_id) < 15:
             # Heuristic: If it looks like a base ID, try appending -100
             # Only apply if it doesn't look like a different type of ID
             logger.info(f"🔧 AppID '{final_client_id}' might be missing '-100'. Attempting as-is first.")
        
        # 4. Construct Auth String
        auth_string = f"{final_client_id}:{final_token}"
        
        # --- DEBUG LOGS (COMPARE THESE WITH YOUR LOCAL ENV) ---
        logger.info(f"🔍 FYERS DEBUG INFO:")
        logger.info(f"   -> App ID (Used): {final_client_id}")
        logger.info(f"   -> Token Start:   {final_token[:6]}...")
        logger.info(f"   -> Token End:     ...{final_token[-6:]}")
        logger.info(f"   -> Token Length:  {len(final_token)}")
        # -----------------------------------------------------

        try:
            from fyers_apiv3.FyersWebsocket import data_ws
            
            def on_message(msg):
                if not self.is_master: return
                if isinstance(msg, dict) and 'symbol' in msg and 'ltp' in msg:
                    fyers_sym = msg['symbol']
                    internal_sym = next((k for k, v in FYERS_MAP.items() if v == fyers_sym), None)
                    if not internal_sym and fyers_sym.startswith("NSE:") and "-EQ" in fyers_sym:
                        internal_sym = fyers_sym.replace("NSE:", "").replace("-EQ", "") + ".NSE"
                    if internal_sym:
                        payload = {"price": msg.get('ltp'), "change": msg.get('ch', 0), "percent_change": msg.get('chp', 0), "timestamp": msg.get('exch_feed_time')}
                        asyncio.run(redis_client.publish_update(internal_sym, payload))
            
            def on_error(err):
                logger.error(f"❌ Fyers Error: {err}")
                # AUTO-HEAL: If token expired (-99), generate a new one immediately
                if isinstance(err, dict) and err.get('code') in [-99, -300]:
                    logger.info("♻️ Generating Fresh Token...")
                    from ..utils import auth_helper
                    new_token = auth_helper.get_fresh_fyers_token()
                    if new_token:
                        os.environ["FYERS_ACCESS_TOKEN"] = new_token
                        # Recursively restart with new token
                        self._run_fyers_engine()

            def on_open():
                logger.info("✅ Fyers WebSocket Connected! Subscribing...")
                fyers.subscribe(symbols=list(FYERS_MAP.values()), data_type="SymbolUpdate")

            fyers = data_ws.FyersDataSocket(
                access_token=auth_string, 
                log_path="", 
                litemode=True, 
                write_to_file=False, 
                reconnect=True, 
                on_connect=on_open, 
                on_message=on_message,
                on_error=on_error
            )
            fyers.connect()

        except Exception as e: 
            logger.error(f"Fyers Crash: {e}")

    async def _poll_yahoo_assets(self):
        yahoo_symbols = list(YAHOO_MAP.keys())
        while self.is_running:
            if not self.is_master: 
                await asyncio.sleep(3)
                continue
            try:
                tickers_str = " ".join(yahoo_symbols)
                data = await asyncio.to_thread(lambda: yf.Tickers(tickers_str))
                for y_sym in yahoo_symbols:
                    try:
                        info = data.tickers[y_sym].fast_info
                        price = info.last_price
                        prev = info.previous_close
                        if price and prev:
                            await redis_client.publish_update(YAHOO_MAP[y_sym], {
                                "price": price, "change": price - prev, "percent_change": ((price - prev) / prev) * 100, "timestamp": int(asyncio.get_event_loop().time())
                            })
                    except: continue
            except: pass
            await asyncio.sleep(3)

    async def _poll_fmp_assets(self):
        while self.is_running:
            if not self.is_master: 
                await asyncio.sleep(1)
                continue
            try:
                data = await asyncio.to_thread(fmp_service.get_crypto_real_time_bulk, FMP_ASSETS)
                if data:
                    for item in data:
                        fmp_sym = item.get('symbol')
                        internal_sym = next((s for s in FMP_ASSETS if fmp_sym in s.replace("-","").replace(".CC","").replace(".US","")), None)
                        if internal_sym:
                            await redis_client.publish_update(internal_sym, {
                                "price": item.get('price'), "change": item.get('change'), "percent_change": item.get('changesPercentage'), "timestamp": item.get('timestamp')
                            })
            except: pass
            await asyncio.sleep(1) 

    async def _poll_eodhd_assets(self):
        while self.is_running:
            if not self.is_master: 
                await asyncio.sleep(1.5)
                continue
            try:
                active_list = await redis_client.get_active_symbols()
                targets = [s for s in active_list if s not in FMP_ASSETS and s not in FYERS_MAP and s not in YAHOO_MAP.values()]
                if targets:
                    for i in range(0, len(targets), 50):
                        chunk = targets[i:i+50]
                        data = await asyncio.to_thread(eodhd_service.get_real_time_bulk, chunk)
                        if data:
                            for item in data:
                                code = item.get('code')
                                target_sym = next((t for t in chunk if code in t), None)
                                if target_sym:
                                    await redis_client.publish_update(target_sym, {
                                        "price": item.get('close'), "change": item.get('change'), "percent_change": item.get('change_p'), "timestamp": item.get('timestamp')
                                    })
            except: pass
            await asyncio.sleep(1.5) 

# ==========================================
# 3. THE CONSUMER
# ==========================================
class StreamConsumer:
    def __init__(self):
        self.active_sockets: Dict[str, List[WebSocket]] = {}
        self.is_listening = False

    async def connect(self, websocket: WebSocket, symbol: str):
        await websocket.accept()
        if symbol not in self.active_sockets: self.active_sockets[symbol] = []
        self.active_sockets[symbol].append(websocket)
        await redis_client.add_active_symbol(symbol)
        if not self.is_listening: asyncio.create_task(self._listen_to_bus())

    def disconnect(self, websocket: WebSocket, symbol: str):
        if symbol in self.active_sockets:
            if websocket in self.active_sockets[symbol]: self.active_sockets[symbol].remove(websocket)
            if not self.active_sockets[symbol]: del self.active_sockets[symbol]

    async def _listen_to_bus(self):
        self.is_listening = True
        subscriber = redis_client.get_subscriber()
        if hasattr(subscriber, "subscribe"): await subscriber.subscribe("market_feed")
        logger.info("🎧 Worker listening to Data Bus")
        
        try:
            async for message in subscriber.listen():
                if message["type"] == "message":
                    try:
                        payload = json.loads(message["data"])
                        symbol = payload["symbol"]
                        data = payload["data"]
                        if symbol in self.active_sockets: await self._broadcast_to_list(symbol, data)
                        is_banner = (symbol in FMP_ASSETS or symbol in FYERS_MAP or symbol in YAHOO_MAP.values())
                        if is_banner and "MARKET_OVERVIEW" in self.active_sockets:
                            await self._broadcast_to_list("MARKET_OVERVIEW", {**data, "symbol": symbol})
                    except: pass
        except:
            self.is_listening = False
            await asyncio.sleep(5)
            asyncio.create_task(self._listen_to_bus())

    async def _broadcast_to_list(self, key: str, data: dict):
        if key not in self.active_sockets: return
        msg = json.dumps(data)
        dead = []
        for ws in self.active_sockets[key]:
            try: await ws.send_text(msg)
            except: dead.append(ws)
        for ws in dead: self.disconnect(ws, key)

producer = StreamProducer()
consumer = StreamConsumer()
```

## File: backend/app/services/technical_service.py
```python
import pandas as pd
import pandas_ta as ta
import numpy as np

# ==========================================
# 1. CHART RESAMPLING ENGINE (High-End Speed)
# ==========================================

def resample_chart_data(chart_data: list, target_interval: str):
    """
    Mathematically converts 5-Minute (Base) candles into higher timeframes.
    This enables INSTANT switching between 5M -> 15M -> 1H -> 4H without API calls.
    
    Input: List of 5-min candles [{'time':..., 'open':...}, ...]
    Output: List of aggregated candles.
    """
    if not chart_data or len(chart_data) < 2: 
        return []

    try:
        # 1. Convert list of dicts to DataFrame
        df = pd.DataFrame(chart_data)
        
        # 2. Set Index to Datetime (Required for resampling)
        # We assume 'time' is Unix timestamp in seconds
        df['datetime'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('datetime', inplace=True)
        
        # 3. Map Frontend Timeframes to Pandas Offset Aliases
        # Frontend: 15m, 1H, 4H, 1D
        # Pandas: 15min, 1h, 4h, 1D
        mapping = {
            "15m": "15min", "15M": "15min",
            "30m": "30min", "30M": "30min",
            "1h": "1h", "1H": "1h",
            "4h": "4h", "4H": "4h",
            "1d": "1D", "1D": "1D",
            "1w": "1W", "1W": "1W"
        }
        
        rule = mapping.get(target_interval)
        
        # If no rule found or rule matches input (5M), return original
        if not rule or target_interval.upper() == "5M": 
            return chart_data

        # 4. Resample Logic (OHLCV Aggregation)
        # Open  = First price of the bucket
        # High  = Max price of the bucket
        # Low   = Min price of the bucket
        # Close = Last price of the bucket
        # Volume = Sum of volume in the bucket
        resampled = df.resample(rule).agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        })
        
        # 5. Cleanup
        # Remove rows with NaN (which happen during market close hours)
        resampled.dropna(inplace=True)
        
        # 6. Format back to Lightweight Charts format
        resampled.reset_index(inplace=True)
        
        # Convert timestamp back to Unix Seconds
        resampled['time'] = resampled['datetime'].astype('int64') // 10**9
        
        # Select and order columns
        final_data = resampled[['time', 'open', 'high', 'low', 'close', 'volume']].to_dict('records')
        
        return final_data

    except Exception as e:
        # print(f"Resampling Error: {e}")
        # On error, fallback to returning the original data to prevent crash
        return chart_data

# ==========================================
# 2. INDICATORS (RSI, MACD, STOCH, ADX)
# ==========================================

def calculate_technical_indicators(df: pd.DataFrame):
    """
    Calculates RSI, MACD, Stoch, ADX, ATR using Pandas TA.
    Expects DataFrame with lowercase columns: 'open', 'high', 'low', 'close', 'volume'
    """
    if df is None or df.empty or len(df) < 20:
        return {}
    
    try:
        # Create a copy to prevent SettingWithCopy warnings
        wdf = df.copy()
        
        # Calculate Indicators
        # We catch individual errors to prevent one indicator crashing the whole set
        try: wdf.ta.rsi(length=14, append=True)
        except: pass
        try: wdf.ta.macd(fast=12, slow=26, signal=9, append=True)
        except: pass
        try: wdf.ta.stoch(k=14, d=3, smooth_k=3, append=True)
        except: pass
        try: wdf.ta.adx(length=14, append=True)
        except: pass
        try: wdf.ta.atr(length=14, append=True)
        except: pass
        try: wdf.ta.willr(length=14, append=True)
        except: pass
        try: wdf.ta.bbands(length=20, std=2, append=True)
        except: pass

        # Get Latest Data Point
        latest = wdf.iloc[-1]
        prev = wdf.iloc[-2] if len(wdf) > 1 else latest
        
        # Helper to safely extract float values (Handles NaN/None)
        def get_val(key):
            try:
                val = latest.get(key)
                if val is None or pd.isna(val) or np.isnan(val):
                    return None
                return float(val)
            except: return None

        return {
            "rsi": get_val('RSI_14'),
            "macd": get_val('MACD_12_26_9'),
            "macdsignal": get_val('MACDs_12_26_9'),
            "stochasticsk": get_val('STOCHk_14_3_3'),
            "adx": get_val('ADX_14'),
            "atr": get_val('ATRr_14'),
            "williamsr": get_val('WILLR_14'),
            "bollingerBands": {
                "upperBand": get_val('BBU_20_2.0'),
                "middleBand": get_val('BBM_20_2.0'),
                "lowerBand": get_val('BBL_20_2.0'),
            },
            # Context for AI Analysis
            "price_action": {
                "current_close": get_val('close'),
                "prev_close": float(prev['close']),
                "trend": "UP" if get_val('close') > float(prev['close']) else "DOWN"
            }
        }
    except Exception as e:
        # print(f"Technical Indicator Calc Error: {e}")
        return {}

# ==========================================
# 3. MOVING AVERAGES (SMA)
# ==========================================

def calculate_moving_averages(df: pd.DataFrame):
    """
    Calculates Simple Moving Averages (5, 10, 20, 50, 100, 200).
    """
    if df is None or df.empty: return {}
    
    try:
        wdf = df.copy()
        mas = {}
        
        periods = [5, 10, 20, 50, 100, 200]
        
        for p in periods:
            if len(wdf) >= p:
                # Rolling mean is faster than pandas_ta for simple SMA
                val = wdf['close'].rolling(window=p).mean().iloc[-1]
                mas[str(p)] = float(val) if not pd.isna(val) else None
            else:
                mas[str(p)] = None
                
        return mas
    except Exception as e:
        return {}

# ==========================================
# 4. PIVOT POINTS (Classic, Fib, Camarilla)
# ==========================================

def calculate_pivot_points(df: pd.DataFrame):
    """
    Calculates Pivots based on the PREVIOUS candle (High/Low/Close).
    """
    if df is None or len(df) < 2: return {}
    
    try:
        # We need the previous completed candle
        prev = df.iloc[-2]
        
        h = float(prev['high'])
        l = float(prev['low'])
        c = float(prev['close'])
        
        # Classic Pivot
        pp = (h + l + c) / 3
        range_val = h - l
        
        classic = {
            "pp": pp,
            "r1": (2 * pp) - l,
            "s1": (2 * pp) - h,
            "r2": pp + range_val,
            "s2": pp - range_val,
            "r3": h + 2 * (pp - l),
            "s3": l - 2 * (h - pp)
        }
        
        # Fibonacci Pivot
        fib = {
            "pp": pp,
            "r1": pp + (0.382 * range_val),
            "s1": pp - (0.382 * range_val),
            "r2": pp + (0.618 * range_val),
            "s2": pp - (0.618 * range_val),
            "r3": pp + range_val,
            "s3": pp - range_val
        }
        
        # Camarilla Pivot
        cam = {
            "pp": pp,
            "r1": c + (range_val * 1.1 / 12),
            "s1": c - (range_val * 1.1 / 12),
            "r2": c + (range_val * 1.1 / 6),
            "s2": c - (range_val * 1.1 / 6),
            "r3": c + (range_val * 1.1 / 4),
            "s3": c - (range_val * 1.1 / 4)
        }

        return {
            "classic": classic,
            "fibonacci": fib,
            "camarilla": cam
        }
    except Exception as e:
        return {}

# ==========================================
# 5. DARVAS BOX SCAN
# ==========================================

def calculate_darvas_box(hist_df: pd.DataFrame, quote: dict, currency: str = "USD"):
    """
    Checks if stock is in a Darvas Box (Consolidation near Highs).
    """
    if hist_df is None or len(hist_df) < 30 or not quote:
        return {"status": "Neutral", "message": "Insufficient data for Darvas scan."}

    try:
        current_price = quote.get('price')
        # Use chart high if quote yearHigh is missing
        year_high = quote.get('yearHigh') or hist_df['high'].max()
        
        if not current_price or not year_high:
            return {"status": "Neutral", "message": "Price data unavailable."}

        # 1. Price Proximity Check (Must be within 15% of 52W High)
        if current_price < (year_high * 0.85):
            return {
                "status": "Not a Candidate",
                "message": f"Price is {((year_high - current_price)/year_high)*100:.1f}% below 52-week high."
            }

        # 2. Box Formation Check (Last 20 days)
        recent = hist_df.tail(20)
        box_top = recent['high'].max()
        box_bottom = recent['low'].min()
        
        # Is the box tight? (< 15% depth)
        box_depth = (box_top - box_bottom) / box_top
        if box_depth > 0.15:
             return {
                "status": "Volatile",
                "message": "Consolidation is too loose (>15% range)."
            }

        # 3. Breakout Status
        currency_sym = "₹" if currency == "INR" else "$"
        
        if current_price >= box_top:
            return {
                "status": "Breakout!",
                "message": f"Breaking out of box ({currency_sym}{box_top:.2f}).",
                "box_top": box_top, "box_bottom": box_bottom, "result": "Pass"
            }
        elif current_price <= box_bottom:
             return {
                "status": "Breakdown",
                "message": f"Falling below support ({currency_sym}{box_bottom:.2f}).",
                "box_top": box_top, "box_bottom": box_bottom, "result": "Fail"
            }
        else:
            return {
                "status": "In Box",
                "message": f"Consolidating between {currency_sym}{box_bottom:.2f} and {currency_sym}{box_top:.2f}.",
                "box_top": box_top, "box_bottom": box_bottom, "result": "Neutral"
            }

    except Exception as e:
        return {"status": "Error", "message": "Calculation failed."}

# ==========================================
# 6. EXTENDED TECHNICALS (Multi-Timeframe AI)
# ==========================================

def calculate_extended_technicals(df: pd.DataFrame):
    """
    Wraps standard calculation but flattens the structure for the AI prompt.
    """
    if df is None or df.empty: return None
    
    try:
        inds = calculate_technical_indicators(df)
        mas = calculate_moving_averages(df)
        pivots = calculate_pivot_points(df)
        
        # Add basic trend confirmation
        price = inds.get('price_action', {}).get('current_close')
        ema_200 = mas.get('200')
        trend = "Unknown"
        if price and ema_200:
            trend = "Bullish" if price > ema_200 else "Bearish"

        return {
            "price": price,
            "rsi": inds.get('rsi'),
            "macd": inds.get('macd'),
            "macd_signal": inds.get('macdsignal'),
            "stoch_k": inds.get('stochasticsk'),
            "adx": inds.get('adx'),
            "ema_20": mas.get('20'),
            "ema_50": mas.get('50'),
            "ema_200": ema_200,
            "trend_context": trend,
            "pivot": pivots.get('classic', {}).get('pp'),
            "support": {"s1": pivots.get('classic', {}).get('s1'), "s2": pivots.get('classic', {}).get('s2')},
            "resistance": {"r1": pivots.get('classic', {}).get('r1'), "r2": pivots.get('classic', {}).get('r2')}
        }
    except:
        return None
```

## File: Dockerfile
```dockerfile
# --- Stage 1: Build React Frontend ---
FROM node:18-alpine AS builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# --- Stage 2: Build Python Backend ---
# UPGRADE: Changed from 3.11 to 3.12 to fix pandas_ta error
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy Backend Code
COPY backend ./backend

# Copy Frontend Build
COPY --from=builder /app/frontend/build ./frontend/build

# Expose the port
EXPOSE 8000

# Start Command
CMD ["sh", "-c", "gunicorn backend.app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000} --timeout 120"]
```

## File: backend/requirements.txt
```
fastapi
uvicorn[standard]
python-dotenv
requests
google-generativeai
pandas
pandas_ta
pydantic
python-multipart
redis>=5.0.0
async-lru
beautifulsoup4
gunicorn
msgpack
fyers-apiv3
websockets
httpx
yfinance
# force rebuild
```

## File: backend/app/routers/charts.py
```python
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
# Import all services
from ..services import gemini_service, eodhd_service, technical_service, fmp_service
import asyncio
import pandas as pd
import json
from urllib.parse import unquote

router = APIRouter()

# Timeframes to fetch for "Deep Dive" analysis
TIMEFRAMES_TO_ANALYZE = ["5M", "1H", "4H", "1D"]

# ==========================================
# 1. SMART SYMBOL RESOLVER
# ==========================================


async def resolve_symbol_smart(ai_text: str, context_type: str):
    """
    Routes the AI-identified ticker to the Best Data Provider.
    Returns: (resolved_ticker, source_api)
    """
    symbol = ai_text.strip().upper()
    
    # Clean up common artifacts
    # Remove USD, USDT to isolate the coin symbol (e.g. BTCUSD -> BTC)
    clean_sym = symbol.replace("/", "").replace("-", "").replace(" ", "").replace("USDT", "").replace("USD", "").replace("=F", "")
    
    # --- A. COMMODITIES (Prioritize FMP) ---
    fmp_commodities = {
        "GOLD": "XAUUSD", "XAU": "XAUUSD", "XAUUSD": "XAUUSD", "GC": "XAUUSD",
        "SILVER": "XAGUSD", "XAG": "XAGUSD", "SI": "XAGUSD",
        "CRUDE": "CLUSD", "CRUDEOIL": "CLUSD", "OIL": "CLUSD", "WTI": "CLUSD", "USOIL": "CLUSD", "CL": "CLUSD",
        "BRENT": "UKOIL", "BRENTOIL": "UKOIL", "UKOIL": "UKOIL",
        "NATURALGAS": "NGUSD", "GAS": "NGUSD", "NATGAS": "NGUSD", "NG": "NGUSD", "UNG": "NGUSD",
        "COPPER": "HGUSD", "HG": "HGUSD",
        "PLATINUM": "PLUSD", "PALLADIUM": "PAUSD"
    }
    
    if clean_sym in fmp_commodities: return fmp_commodities[clean_sym], "FMP"
    if symbol in fmp_commodities: return fmp_commodities[symbol], "FMP"

    # --- B. CRYPTO (CRITICAL FIX) ---
    # We must return the Internal Format (BTC-USD.CC) so stocks.py recognizes it correctly
    crypto_shorts = ["BTC", "ETH", "SOL", "XRP", "DOGE", "ADA", "BNB", "MATIC", "AVAX", "LTC", "DOT", "SHIB"]
    
    if clean_sym in crypto_shorts:
        return f"{clean_sym}-USD.CC", "FMP"
        
    if "BTC" in symbol or "ETH" in symbol or "SOL" in symbol:
        # Fallback if cleaning missed it
        return f"{clean_sym}-USD.CC", "FMP"

    # --- C. INDICES (Prioritize EODHD) ---
    if context_type == 'index' or '^' in symbol or 'NIFTY' in symbol or 'SENSEX' in symbol or 'SPX' in symbol:
        if "BANK" in symbol: return "NSEBANK.INDX", "EODHD"
        if "NIFTY" in symbol: return "NSEI.INDX", "EODHD"
        if "SENSEX" in symbol: return "BSESN.INDX", "EODHD"
        if "SPX" in symbol or "S&P" in symbol: return "GSPC.INDX", "EODHD"
        if "NDX" in symbol or "NASDAQ" in symbol: return "NDX.INDX", "EODHD"
        if "DOW" in symbol or "DJI" in symbol: return "DJI.INDX", "EODHD"
        if "VIX" in symbol: return "INDIAVIX.INDX", "EODHD"
        if "DAX" in symbol: return "GDAXI.INDX", "EODHD"
        if "NIKKEI" in symbol: return "N225.INDX", "EODHD"

    # --- D. STOCKS (EODHD) ---
    if ".NS" in symbol: return symbol.replace(".NS", ".NSE"), "EODHD"
    if ".BO" in symbol: return symbol.replace(".BO", ".BSE"), "EODHD"
    if ".US" in symbol: return symbol, "EODHD"

    # Suffix Discovery Fallback
    candidates = [f"{symbol}.NSE", f"{symbol}.US"]
    for cand in candidates:
        try:
            check = await asyncio.to_thread(eodhd_service.get_live_price, cand)
            if check and 'price' in check and check['price'] > 0:
                return cand, "EODHD"
        except: continue
            
    return f"{symbol}.NSE", "EODHD"

# ==========================================
# 2. ENDPOINT: ANALYZE CHART
# ==========================================

@router.post("/analyze")
async def analyze_chart_image(
    chart_image: UploadFile = File(...),
    analysis_type: str = Form("stock")
):
    """
    Master AI Chart Analyst.
    1. AI Vision (Identify Ticker).
    2. Hybrid Resolution (Route to FMP or EODHD).
    3. Parallel Data Fetch (Vision + Math).
    4. Technical Calculation (Pandas).
    5. Synthesis & Response.
    """
    if not chart_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    image_bytes = await chart_image.read()

    # --- Step 1: AI Vision (Identify Ticker) ---
    # We ask Gemini to just tell us WHAT is in the image first.
    raw_symbol = await asyncio.to_thread(gemini_service.identify_ticker_from_image, image_bytes)

    if not raw_symbol or raw_symbol == "NOT_FOUND":
        return {
            "identified_symbol": "NOT_FOUND", 
            "analysis_data": "Could not identify symbol from image. Please ensure the ticker name is visible.", 
            "technical_data": None
        }
    
    # --- Step 2: Resolve & Normalize (Hybrid Engine) ---
    final_symbol, data_source = await resolve_symbol_smart(raw_symbol, analysis_type)
    print(f"Chart Upload: AI detected '{raw_symbol}' -> Resolved to '{final_symbol}' via {data_source}")

    # --- Step 3: Parallel Execution ---
    
    # Task A: AI Visual Strategy (Generates the text report)
    vision_task = asyncio.to_thread(gemini_service.analyze_chart_technicals_from_image, image_bytes)

    # Task B: Fetch Data for Multiple Timeframes (Math Engine)
    async def fetch_and_calc(tf):
        try:
            raw_data = []
            
            # --- HYBRID FETCHING LOGIC ---
            if data_source == "FMP":
                # Try Commodity First
                raw_data = await asyncio.to_thread(fmp_service.get_commodity_history, final_symbol, range_type=tf)
                # If Empty, Try Crypto
                if not raw_data:
                    raw_data = await asyncio.to_thread(fmp_service.get_crypto_history, final_symbol, range_type=tf)
            else:
                # Fetch Stocks/Indices from EODHD
                raw_data = await asyncio.to_thread(eodhd_service.get_historical_data, final_symbol, range_type=tf)
            
            # Validation
            if not raw_data or len(raw_data) < 20: 
                return tf, None
            
            # Convert to Pandas for Math
            df = pd.DataFrame(raw_data)
            
            # Calculate Indicators
            technicals = await asyncio.to_thread(technical_service.calculate_extended_technicals, df)
            
            return tf, technicals
        except Exception as e:
            print(f"Error analyzing {tf} for {final_symbol}: {e}")
            return tf, None

    # Run all data tasks in parallel
    data_tasks = [fetch_and_calc(tf) for tf in TIMEFRAMES_TO_ANALYZE]
    
    # Execute Vision + Data simultaneously
    results = await asyncio.gather(vision_task, *data_tasks)

    # Unpack Results
    analysis_text = results[0] # The text report from Gemini
    tech_results = results[1:] # The list of (tf, data) tuples

    # Structure Technical Data for Frontend
    technical_data = {tf: data for tf, data in tech_results if data is not None}

    # --- Step 4: Final Response Formatting ---
    frontend_symbol = final_symbol
    
    # Convert EODHD format back to Frontend format if it's a Stock
    if final_symbol.endswith(".NSE"): 
        frontend_symbol = final_symbol.replace(".NSE", ".NS")
    elif final_symbol.endswith(".BSE"): 
        frontend_symbol = final_symbol.replace(".BSE", ".BO")
    
    return {
        "identified_symbol": frontend_symbol,
        "analysis_data": analysis_text,
        "technical_data": technical_data
    }
@router.post("/analyze-pure")
async def analyze_pure_chart(chart_image: UploadFile = File(...)):
    """
    Pure AI Vision Endpoint. No APIs. No Data Feeds. Just Brains.
    """
    if not chart_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type.")

    image_bytes = await chart_image.read()
    
    # Direct call to the Vision Engine
    analysis_text = await asyncio.to_thread(gemini_service.analyze_pure_vision, image_bytes)
    
    return {
        "analysis": analysis_text
    }
```

## File: backend/app/services/fmp_service.py
```python
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

FMP_API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/api/v3"
BASE_URL_V4 = "https://financialmodelingprep.com/api/v4"

# --- HIGH-END OPTIMIZATION: PERSISTENT SESSION ---
# Reuses TCP connections to reduce latency/overhead on repeated requests
session = requests.Session()

def _fetch(url: str, params: dict = None):
    """
    Internal helper for high-performance fetching with error handling.
    """
    if not FMP_API_KEY: return None
    
    # Append API key to params
    if params is None: params = {}
    params['apikey'] = FMP_API_KEY
    
    try:
        # 4-second timeout prevents server hangs on slow external API calls
        response = session.get(url, params=params, timeout=4)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        # Silent fail to keep app running
        return None

# ==========================================
# 1. SEARCH & CORE (Optimized)
# ==========================================

def search_ticker(query: str, limit: int = 10):
    """
    Primary Search Engine.
    """
    endpoint = f"{BASE_URL}/search"
    params = {'query': query, 'limit': limit}
    res = _fetch(endpoint, params)
    return res if res else []

def get_company_profile(symbol: str):
    """
    Backup Profile Data (Description, Website, Sector).
    """
    endpoint = f"{BASE_URL}/profile/{symbol}"
    res = _fetch(endpoint)
    return res[0] if res and isinstance(res, list) else {}

# ==========================================
# 2. FINANCIALS (BACKUP ENGINE)
# ==========================================

def get_financial_statements(symbol: str, statement_type: str, period: str = "annual", limit: int = 5):
    """
    Fetches Income/Balance/CashFlow.
    Used if EODHD returns empty data.
    statement_type: 'income-statement', 'balance-sheet-statement', 'cash-flow-statement'
    """
    endpoint = f"{BASE_URL}/{statement_type}/{symbol}"
    params = {'period': period, 'limit': limit}
    res = _fetch(endpoint, params)
    return res if res else []

# ==========================================
# 3. ANALYSTS & NEWS (PRIMARY SOURCE)
# ==========================================

def get_analyst_ratings(symbol: str):
    """
    Fetches Buy/Sell/Hold ratings.
    """
    endpoint = f"{BASE_URL}/rating/{symbol}"
    params = {'limit': 1}
    res = _fetch(endpoint, params)
    return res if res else []

def get_price_target_consensus(symbol: str):
    """
    Fetches High/Low/Avg Price Targets.
    """
    endpoint = f"{BASE_URL}/price-target-consensus/{symbol}"
    res = _fetch(endpoint)
    return res[0] if res and isinstance(res, list) else {}

def get_shareholding_data(symbol: str):
    """
    Fetches Institutional Holders.
    """
    endpoint = f"{BASE_URL}/institutional-holder/{symbol}"
    res = _fetch(endpoint)
    return res if res else []

# ==========================================
# 4. PEERS & METRICS (V4 UPGRADE)
# ==========================================

def get_stock_peers(symbol: str):
    """
    Uses FMP V4 endpoint for better peer matching.
    """
    endpoint = f"{BASE_URL_V4}/stock_peers"
    params = {'symbol': symbol}
    res = _fetch(endpoint, params)
    # V4 returns: [{"symbol": "AAPL", "peersList": [...]}]
    if res and isinstance(res, list) and len(res) > 0 and 'peersList' in res[0]:
        return res[0]['peersList']
    return []

def get_peers_with_metrics(symbols: list):
    """
    BULK FETCH: Gets TTM Metrics for multiple stocks in ONE call.
    """
    if not symbols: return []
    
    # FMP format: RELIANCE.NS,TCS.NS
    # Remove any internal suffixes if necessary, but FMP usually handles .NS fine
    query = ",".join(symbols)
    
    # Endpoint: Key Metrics TTM
    endpoint = f"{BASE_URL}/key-metrics-ttm/{query}"
    res = _fetch(endpoint)
    return res if res else []

# ==========================================
# 5. CHARTING ENGINE (HIGH-SPEED PROCESSING)
# ==========================================

def process_fmp_candles(raw_list: list):
    """
    High-Speed Processor:
    1. Slices data (Max 750 candles) for instant loading.
    2. Parses dates safely.
    3. Sorts Oldest -> Newest.
    """
    if not raw_list: return []
    
    # --- SPEED FIX: SLICING ---
    # FMP returns Newest -> Oldest. We only need the recent data.
    # Limiting to 750 candles prevents the loop from running 5000+ times.
    sliced_list = raw_list[:750] 
    
    data = []
    for candle in sliced_list:
        date_str = candle.get('date')
        if not date_str: continue
        
        try:
            # Parse Date
            if ":" in date_str:
                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            else:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
            
            ts = int(dt.timestamp())
            
            # Safe Float Conversion
            o = float(candle.get('open') or 0)
            h = float(candle.get('high') or 0)
            l = float(candle.get('low') or 0)
            c = float(candle.get('close') or 0)
            v = float(candle.get('volume') or 0)
            
            if c > 0: 
                data.append({
                    "time": ts,
                    "open": o, "high": h, "low": l, "close": c, "volume": v
                })
        except: continue
    
    # Sort Oldest -> Newest (Required for Chart)
    data.sort(key=lambda x: x['time'])
    return data

def get_commodity_history(symbol: str, range_type: str = "1d"):
    """
    Fetches Commodity History from FMP (XAUUSD, CLUSD).
    """
    if not FMP_API_KEY: return []
    
    # Map Range to FMP Interval
    interval = "5min"
    if range_type in ["1H", "4H"]: interval = "1hour"
    elif range_type == "15M": interval = "15min"
    
    # API Endpoint
    # e.g. https://financialmodelingprep.com/api/v3/historical-chart/5min/CLUSD
    url = f"{BASE_URL}/historical-chart/{interval}/{symbol}?apikey={FMP_API_KEY}"
    
    # If Daily History, FMP uses a different endpoint structure
    if range_type in ["1W", "1M", "1D"] and interval == "5min":
        url = f"{BASE_URL}/historical-price-full/{symbol}?apikey={FMP_API_KEY}"

    res = _fetch(url)
    
    # Normalize Response: Daily returns { symbol:..., historical: [...] }
    raw_data = []
    if isinstance(res, dict) and 'historical' in res:
        raw_data = res['historical']
    elif isinstance(res, list):
        raw_data = res
    
    # Send to the Slicer for speed
    return process_fmp_candles(raw_data)

def get_crypto_history(symbol: str, range_type: str = "1D"):
    """
    Fetches Crypto Candles (BTCUSD).
    """
    if not FMP_API_KEY: return []
    
    # Intraday Logic
    interval = "5min"
    is_intraday = range_type in ["5M", "15M", "1H", "4H"]
    
    if range_type == "15M": interval = "15min"
    if range_type == "1H": interval = "1hour"
    if range_type == "4H": interval = "4hour"
    
    if is_intraday:
        url = f"{BASE_URL}/historical-chart/{interval}/{symbol}?apikey={FMP_API_KEY}"
    else:
        # Daily/Weekly
        url = f"{BASE_URL}/historical-price-full/{symbol}?apikey={FMP_API_KEY}"

    res = _fetch(url)
    
    raw_data = []
    if isinstance(res, dict) and 'historical' in res:
        raw_data = res['historical']
    elif isinstance(res, list):
        raw_data = res
    
    # Use the Slicer
    return process_fmp_candles(raw_data)
# ==========================================
# 6. REAL-TIME QUOTES (HIGH SPEED)
# ==========================================

def get_quote(symbol: str):
    """
    Fetches Live Price for Commodities/Stocks from FMP.
    Structure matches EODHD quote for seamless frontend integration.
    """
    if not FMP_API_KEY: return {}
    
    endpoint = f"{BASE_URL}/quote/{symbol}"
    res = _fetch(endpoint)
    
    if res and isinstance(res, list) and len(res) > 0:
        data = res[0]
        return {
            "price": data.get('price'),
            "change": data.get('change'),
            "changesPercentage": data.get('changesPercentage'),
            "dayLow": data.get('dayLow'),
            "dayHigh": data.get('dayHigh'),
            "yearHigh": data.get('yearHigh'),
            "yearLow": data.get('yearLow'),
            "volume": data.get('volume'),
            "previousClose": data.get('previousClose'),
            "open": data.get('open'),
            "timestamp": data.get('timestamp')
        }
    return {}

def get_crypto_real_time_bulk(symbols: list):
    """
    Fetches Live Prices for multiple Cryptos in 1 call.
    Used for the Stream Engine.
    """
    if not FMP_API_KEY or not symbols: return []
    
    # FMP format: BTCUSD,ETHUSD
    # Ensure symbols are clean (remove .CC or -USD if passed)
    clean_syms = [s.replace("-USD.CC", "USD").replace("-", "").replace(".CC", "") for s in symbols]
    query = ",".join(clean_syms)
    
    endpoint = f"{BASE_URL}/quote/{query}"
    return _fetch(endpoint) or []
```

## File: frontend/src/components/Chart/CustomChart.js
```javascript
import React, { useEffect, useRef, useState, useCallback } from 'react';
import { 
  createChart, 
  ColorType, 
  CrosshairMode, 
  CandlestickSeries, 
  HistogramSeries,
  LineSeries
} from 'lightweight-charts';
import styled from 'styled-components';
import axios from 'axios';
import { RSI, MACD, StochasticRSI, SMA, EMA, ADX, ATR, VWAP } from 'technicalindicators';
import { 
  FaLayerGroup, FaTimes, FaPlus, FaMousePointer, 
  FaMinus, FaSlash, FaVectorSquare, FaListOl, FaBalanceScale, FaEraser, FaUndo, FaPencilAlt, FaTrash, FaSpinner, FaExclamationTriangle, FaPlug, FaWifi
} from 'react-icons/fa';
import { FyersClientEngine } from '../../utils/FyersClientEngine';

// ==========================================
// 1. HIGH-END STYLED COMPONENTS
// ==========================================

const ChartWrapper = styled.div`
  position: relative;
  width: 100%;
  height: 650px;
  background-color: #0D1117;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
  display: flex;
  flex-direction: column;
`;

const Toolbar = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background-color: #161B22;
  border-bottom: 1px solid var(--color-border);
  flex-wrap: wrap;
  gap: 10px;
  z-index: 20;
`;

const DrawingSidebar = styled.div`
  position: absolute;
  top: 60px;
  left: 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: rgba(22, 27, 34, 0.95);
  backdrop-filter: blur(10px);
  padding: 8px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  z-index: 30;
  box-shadow: 4px 0 20px rgba(0,0,0,0.4);
`;

const ToolBtn = styled.button`
  width: 36px;
  height: 36px;
  border-radius: 6px;
  border: 1px solid ${({ active }) => active ? 'var(--color-primary)' : 'transparent'};
  background: ${({ active }) => active ? 'rgba(88, 166, 255, 0.2)' : 'transparent'};
  color: ${({ active }) => active ? 'var(--color-primary)' : 'var(--color-text-secondary)'};
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1rem;
  position: relative;

  &:hover {
    background: rgba(255,255,255,0.1);
    color: #fff;
  }
`;

const LayersPanel = styled.div`
  position: absolute;
  top: 60px;
  right: 10px;
  width: 260px;
  background: rgba(22, 27, 34, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 10px;
  z-index: 30;
  box-shadow: -4px 0 20px rgba(0,0,0,0.4);
  max-height: 400px;
  overflow-y: auto;
  
  &::-webkit-scrollbar { width: 4px; }
  &::-webkit-scrollbar-thumb { background: #30363D; border-radius: 2px; }
`;

const LayerHeader = styled.div`
  color: #8b949e;
  font-size: 0.75rem;
  margin-bottom: 8px;
  text-transform: uppercase;
  letter-spacing: 1px;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const LayerItem = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255,255,255,0.03);
  padding: 8px 10px;
  border-radius: 6px;
  margin-bottom: 6px;
  font-size: 0.85rem;
  border: 1px solid transparent;
  transition: all 0.2s;
  
  &:hover {
    border-color: var(--color-primary);
    background: rgba(255,255,255,0.05);
  }
`;

const LayerActions = styled.div`
  display: flex;
  gap: 8px;
`;

const IconButton = styled.button`
  background: transparent;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 2px;
  display: flex;
  &:hover { color: #fff; }
  &.delete:hover { color: #F85149; }
`;

const EditModal = styled.div`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: #1C2128;
  border: 1px solid var(--color-primary);
  padding: 20px;
  border-radius: 12px;
  z-index: 100;
  box-shadow: 0 20px 50px rgba(0,0,0,0.9);
  width: 320px;
`;

const ModalTitle = styled.h4`margin: 0 0 15px 0; color: #fff; font-size: 1.1rem;`;
const ModalInput = styled.div`
  margin-bottom: 12px;
  label { display: block; font-size: 0.75rem; color: #8b949e; margin-bottom: 4px; text-transform: uppercase; }
  input { width: 100%; background: #0D1117; border: 1px solid #30363D; color: #fff; padding: 8px; border-radius: 6px; font-family: 'Roboto Mono', monospace; }
  input:focus { border-color: var(--color-primary); outline: none; }
`;
const ModalActions = styled.div`display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px;`;

const LeftGroup = styled.div`display: flex; gap: 10px; align-items: center; flex-wrap: wrap;`;
const RangeButton = styled.button`background: ${({ active }) => active ? 'var(--color-primary)' : 'transparent'}; color: ${({ active }) => active ? '#fff' : 'var(--color-text-secondary)'}; border: 1px solid ${({ active }) => active ? 'var(--color-primary)' : 'transparent'}; padding: 4px 10px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: all 0.2s; &:hover { background: ${({ active }) => active ? 'var(--color-primary)' : 'rgba(255,255,255,0.05)'}; color: #fff; }`;
const IndicatorButton = styled.button`display: flex; align-items: center; gap: 6px; background: rgba(255,255,255,0.05); border: 1px solid var(--color-border); color: var(--color-text-primary); padding: 4px 12px; border-radius: 6px; font-size: 0.8rem; cursor: pointer; position: relative; &:hover { background: rgba(255,255,255,0.1); }`;
const Dropdown = styled.div`position: absolute; top: 40px; left: 0; background: #1C2128; border: 1px solid var(--color-border); border-radius: 8px; padding: 10px; z-index: 50; box-shadow: 0 4px 20px rgba(0,0,0,0.5); display: flex; flex-direction: column; gap: 8px; width: 220px;`;
const InputGroup = styled.div`display: flex; gap: 5px; align-items: center;`;
const StyledInput = styled.input`background: #0D1117; border: 1px solid var(--color-border); color: white; padding: 4px; border-radius: 4px; width: 60px; font-size: 0.8rem;`;
const AddButton = styled.button`background: var(--color-success); border: none; color: white; padding: 6px; border-radius: 4px; cursor: pointer; font-weight: 600; margin-top: 5px; font-size: 0.8rem; &:hover { opacity: 0.9; }`;
const ActiveIndicatorsList = styled.div`display: flex; gap: 8px; overflow-x: auto; padding: 4px 0; align-items: center; &::-webkit-scrollbar { display: none; }`;
const IndicatorTag = styled.div`background: rgba(56, 139, 253, 0.15); border: 1px solid var(--color-primary); color: var(--color-primary); padding: 2px 8px; border-radius: 4px; font-size: 0.7rem; display: flex; align-items: center; gap: 6px; white-space: nowrap;`;
const CloseIcon = styled(FaTimes)`cursor: pointer; &:hover { color: #fff; }`;
const ChartContainer = styled.div`flex-grow: 1; width: 100%; cursor: ${({ crosshair }) => crosshair ? 'crosshair' : 'default'};`;
const StatusText = styled.span`font-size: 0.75rem; color: ${({ isLive }) => isLive ? '#3FB950' : 'var(--color-text-secondary)'}; margin-left: auto; font-weight: 600; display: flex; align-items: center; gap: 6px;`;
const PulseDot = styled.div`width: 6px; height: 6px; border-radius: 50%; background-color: #3FB950; box-shadow: 0 0 5px #3FB950; animation: pulse 2s infinite; @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }`;
const HelperText = styled.div`position: absolute; top: 60px; left: 60px; background: rgba(0,0,0,0.7); color: #fff; padding: 5px 10px; border-radius: 4px; font-size: 0.8rem; pointer-events: none; z-index: 25;`;
const LoadingOverlay = styled.div`position: absolute; top: 50px; left: 0; right: 0; bottom: 0; background: rgba(13, 17, 23, 0.4); backdrop-filter: blur(2px); z-index: 15; display: flex; align-items: center; justify-content: center; color: var(--color-primary); font-size: 2rem;`;
const Spinner = styled(FaSpinner)`animation: spin 1s linear infinite; @keyframes spin { 100% { transform: rotate(360deg); } }`;
const NoDataOverlay = styled.div`position: absolute; top: 50px; left: 0; right: 0; bottom: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; color: var(--color-text-secondary); z-index: 10; font-size: 1.2rem; gap: 10px;`;

// ==========================================
// 2. MATH ALGORITHMS (Client-Side)
// ==========================================

const calculateSuperTrend = (data, period = 10, multiplier = 3) => {
    if (!data || data.length < period) return [];
    const atr = ATR.calculate({ period, high: data.map(d=>d.high), low: data.map(d=>d.low), close: data.map(d=>d.close) });
    const st = [];
    let prevFinalUpper = 0; let prevFinalLower = 0; let prevTrend = 1;
    for (let i = 0; i < data.length; i++) {
        const atrIndex = i - (period - 1);
        if (atrIndex < 0) continue;
        const curr = data[i]; const prev = data[i-1]; const currAtr = atr[atrIndex];
        const basicUpper = (curr.high + curr.low) / 2 + multiplier * currAtr;
        const basicLower = (curr.high + curr.low) / 2 - multiplier * currAtr;
        let finalUpper = basicUpper;
        if (prev && prevFinalUpper) { if (basicUpper < prevFinalUpper || prev.close > prevFinalUpper) finalUpper = basicUpper; else finalUpper = prevFinalUpper; }
        let finalLower = basicLower;
        if (prev && prevFinalLower) { if (basicLower > prevFinalLower || prev.close < prevFinalLower) finalLower = basicLower; else finalLower = prevFinalLower; }
        let trend = prevTrend;
        if (prevTrend === 1 && curr.close < finalLower) trend = -1; else if (prevTrend === -1 && curr.close > finalUpper) trend = 1;
        st.push({ time: curr.time, value: trend === 1 ? finalLower : finalUpper, color: trend === 1 ? '#00E676' : '#FF1744' });
        prevFinalUpper = finalUpper; prevFinalLower = finalLower; prevTrend = trend;
    }
    return st;
};

const calculateSMC = (data) => {
    const markers = []; const coloredCandles = []; const priceLines = []; 
    if (!data || data.length < 5) return { markers, coloredCandles, priceLines };
    for (let i = 2; i < data.length - 1; i++) {
        const curr = data[i]; const prev = data[i-1]; const prev2 = data[i-2];
        if (curr.low > prev2.high) {
            coloredCandles.push({ time: prev.time, color: '#FBBF24', wickColor: '#FBBF24', borderColor: '#FBBF24' });
            if (i > data.length - 80) priceLines.push({ price: prev2.high, color: '#FBBF24', title: 'DEMAND GAP' });
        }
        if (curr.high < prev2.low) {
            coloredCandles.push({ time: prev.time, color: '#D500F9', wickColor: '#D500F9', borderColor: '#D500F9' });
            if (i > data.length - 80) priceLines.push({ price: prev2.low, color: '#D500F9', title: 'SUPPLY GAP' });
        }
        const isRedPrev = prev.close < prev.open; const isGreenCurr = curr.close > curr.open; const engulfsBull = curr.close > prev.open; 
        if (isRedPrev && isGreenCurr && engulfsBull) markers.push({ time: prev.time, position: 'belowBar', color: '#3FB950', shape: 'arrowUp', text: 'OB', size: 1 });
        const isGreenPrev = prev.close > prev.open; const isRedCurr = curr.close < curr.open; const engulfsBear = curr.close < prev.open;
        if (isGreenPrev && isRedCurr && engulfsBear) markers.push({ time: prev.time, position: 'aboveBar', color: '#F85149', shape: 'arrowDown', text: 'OB', size: 1 });
    }
    return { markers, coloredCandles, priceLines };
};

// ==========================================
// 3. MAIN COMPONENT
// ==========================================

const CustomChart = ({ symbol }) => {
  const chartContainerRef = useRef();
  
  // Instance Refs
  const chartRef = useRef(null);
  const candleSeriesRef = useRef(null);
  const volumeSeriesRef = useRef(null);
  const abortControllerRef = useRef(null);
  const fyersEngineRef = useRef(null);

  // Drawing & State Refs
  const priceLinesRef = useRef([]); 
  const drawingLinesRef = useRef([]); 
  const drawingSeriesRef = useRef([]); 
  const previewObjectsRef = useRef([]); 
  const lastCandleRef = useRef(null); 
  const isMounted = useRef(true);
  
  // State
  const [timeframe, setTimeframe] = useState('1D'); 
  const [chartData, setChartData] = useState([]);
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeIndicators, setActiveIndicators] = useState([]);
  const [isLive, setIsLive] = useState(false);
  const [connectionType, setConnectionType] = useState("Server");
  const [isChartLoading, setIsChartLoading] = useState(false);
  const [hasError, setHasError] = useState(false);
  
  const [drawMode, setDrawMode] = useState('cursor'); 
  const [tempPoints, setTempPoints] = useState([]);
  const [userDrawings, setUserDrawings] = useState([]); 
  const [editingDrawing, setEditingDrawing] = useState(null);
  const [editValues, setEditValues] = useState({});
  const drawModeRef = useRef(drawMode); 
  const tempPointsRef = useRef(tempPoints);
  // --- CRITICAL FIX: Add userDrawingsRef
  const userDrawingsRef = useRef(userDrawings);

  const [selectedInd, setSelectedInd] = useState('SMC');
  const [param1, setParam1] = useState(20);
  const [param2, setParam2] = useState(26);
  const [param3, setParam3] = useState(9);

  // Constants
  const isIndian = symbol?.includes('.NS') || symbol?.includes('.BO') || symbol?.includes('NIFTY') || symbol?.includes('SENSEX') || symbol?.includes('BANK');

  // --- HELPER: Get Base API URL (Vercel Fix) ---
  const getBaseApiUrl = () => {
     // Use environment variable if set, otherwise default to localhost for dev
     return process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';
  };

  const istFormatter = (timestamp) => {
      const date = new Date(timestamp * 1000);
      if (isIndian) {
          if (!['1D', '1W', '1M'].includes(timeframe)) {
              return new Intl.DateTimeFormat('en-IN', { timeZone: 'Asia/Kolkata', hour: '2-digit', minute: '2-digit', hour12: false }).format(date);
          }
          return new Intl.DateTimeFormat('en-IN', { timeZone: 'Asia/Kolkata', day: '2-digit', month: 'short', year: '2-digit' }).format(date);
      }
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  useEffect(() => { drawModeRef.current = drawMode; if(drawMode === 'cursor') { setTempPoints([]); clearPreview(); } }, [drawMode]);
  useEffect(() => { tempPointsRef.current = tempPoints; }, [tempPoints]);
  useEffect(() => { userDrawingsRef.current = userDrawings; }, [userDrawings]);

  const mapData = (values, chartData) => {
    const output = [];
    for (let i = 0; i < values.length; i++) {
        const dIndex = chartData.length - 1 - i; const vIndex = values.length - 1 - i;
        if (dIndex >= 0) output.unshift({ time: chartData[dIndex].time, value: values[vIndex] });
    }
    return output;
  };

  // --- INITIALIZE CHART ---
  useEffect(() => {
    isMounted.current = true;
    if (!chartContainerRef.current) return;
    chartContainerRef.current.innerHTML = '';
    
    priceLinesRef.current = []; drawingLinesRef.current = []; drawingSeriesRef.current = []; previewObjectsRef.current = [];

    const chart = createChart(chartContainerRef.current, {
      layout: { background: { type: ColorType.Solid, color: '#0D1117' }, textColor: '#8B949E' },
      grid: { vertLines: { color: '#21262D' }, horzLines: { color: '#21262D' } },
      width: chartContainerRef.current.clientWidth,
      height: chartContainerRef.current.clientHeight,
      crosshair: { mode: CrosshairMode.Normal },
      timeScale: { borderColor: '#30363D', timeVisible: true, secondsVisible: false, tickMarkFormatter: (time) => istFormatter(time) },
      localization: { timeFormatter: (time) => istFormatter(time) },
      rightPriceScale: { borderColor: '#30363D' },
    });

    const candleSeries = chart.addSeries(CandlestickSeries, {
      upColor: '#3FB950', downColor: '#F85149', borderVisible: false, wickUpColor: '#3FB950', wickDownColor: '#F85149',
    });

    const volumeSeries = chart.addSeries(HistogramSeries, {
      color: '#26a69a', priceFormat: { type: 'volume' }, priceScaleId: '',
    });
    volumeSeries.priceScale().applyOptions({ scaleMargins: { top: 0.85, bottom: 0 } });

    // Click Listener
    chart.subscribeClick((param) => {
      // ZOMBIE CHECK
      if (!isMounted.current || !chartRef.current || !candleSeries) return;
      
      if (!param.point || !param.time) return;
      const price = candleSeries.coordinateToPrice(param.point.y);
      const time = param.time;
      const mode = drawModeRef.current;
      const id = Date.now();

      if (mode === 'cursor') return;
      if (mode === 'horizontal') { setUserDrawings(prev => [...prev, { id, type: 'horizontal', price, title: 'H-Line' }]); setDrawMode('cursor'); return; }
      if (mode === 'rect') { setUserDrawings(prev => [...prev, { id, type: 'rect', price, title: 'Zone' }]); return; }
      if (['fib', 'trend', 'longshort'].includes(mode)) {
          handleMultiClickTool(price, time, mode === 'longshort' ? 3 : 2, (points) => {
              const id = Date.now();
              setUserDrawings(prev => [...prev, { id, type: mode, points }]);
          });
      }
    });

    // Crosshair Listener
    chart.subscribeCrosshairMove((param) => {
        if (!isMounted.current || !chartRef.current) return;
        const mode = drawModeRef.current;
        const currentPoints = tempPointsRef.current;
        if (mode === 'cursor' || currentPoints.length === 0 || !param.point || !param.time) return;
        const currentPrice = candleSeries.coordinateToPrice(param.point.y);
        const currentTime = param.time;
        const start = currentPoints[0];
        if (currentTime === start.time) return; 
        drawPreviewShape(mode, start, { price: currentPrice, time: currentTime }, chart, candleSeries);
    });

    chartRef.current = chart;
    candleSeriesRef.current = candleSeries;
    volumeSeriesRef.current = volumeSeries;

    const resizeObserver = new ResizeObserver(entries => {
        if (!isMounted.current || !chartRef.current) return;
        const newRect = entries[0].contentRect;
        if (newRect.width > 0 && newRect.height > 0) {
            try {
                chartRef.current.applyOptions({ width: newRect.width, height: newRect.height });
                chartRef.current.timeScale().fitContent(); 
            } catch(e) {}
        }
    });
    resizeObserver.observe(chartContainerRef.current);

    return () => {
      isMounted.current = false;
      resizeObserver.disconnect();
      if (fyersEngineRef.current) fyersEngineRef.current.disconnect();
      if (chartRef.current) {
        try { chartRef.current.remove(); } catch(e) {}
        chartRef.current = null;
        candleSeriesRef.current = null;
        volumeSeriesRef.current = null;
      }
    };
  }, [symbol, timeframe]);

  // --- DRAWING HELPERS ---
  const handleMultiClickTool = (price, time, requiredClicks, callback) => { setTempPoints(prev => { const newPoints = [...prev, { price, time }]; if (newPoints.length === requiredClicks) { clearPreview(); callback(newPoints); setDrawMode('cursor'); return []; } return newPoints; }); };
  const clearPreview = () => { previewObjectsRef.current.forEach(obj => { if (obj.type === 'line' && candleSeriesRef.current) try{ candleSeriesRef.current.removePriceLine(obj.ref); } catch(e){} if (obj.type === 'series' && chartRef.current) try{ chartRef.current.removeSeries(obj.ref); } catch(e){} }); previewObjectsRef.current = []; };
  const drawPreviewShape = (type, p1, p2, chart, series) => { clearPreview(); if (type === 'trend') { const sorted = p1.time > p2.time ? [p2, p1] : [p1, p2]; const data = [{ time: sorted[0].time, value: sorted[0].price }, { time: sorted[1].time, value: sorted[1].price }]; const lineSeries = chart.addSeries(LineSeries, { color: '#ffffff', lineWidth: 1, lastValueVisible: false, priceLineVisible: false }); lineSeries.setData(data); previewObjectsRef.current.push({ type: 'series', ref: lineSeries }); } else if (type === 'fib') { const low = Math.min(p1.price, p2.price); const high = Math.max(p1.price, p2.price); const diff = high - low; const levels = [0, 0.5, 1]; levels.forEach(lvl => { const line = series.createPriceLine({ price: low + (diff * lvl), color: '#FFD700', lineWidth: 1, lineStyle: 2, axisLabelVisible: false }); previewObjectsRef.current.push({ type: 'line', ref: line }); }); } else if (type === 'longshort') { const l1 = series.createPriceLine({ price: p1.price, color: '#888', title: 'ENTRY' }); const l2 = series.createPriceLine({ price: p2.price, color: '#3FB950', title: 'TARGET' }); previewObjectsRef.current.push({ type: 'line', ref: l1 }, { type: 'line', ref: l2 }); } };
  const handleEdit = (d) => { setEditingDrawing(d.id); if (d.points) { setEditValues({ p1: d.points[0]?.price, p2: d.points[1]?.price, p3: d.points[2]?.price }); } else { setEditValues({ p1: d.price }); } };
  const saveEdit = () => { setUserDrawings(prev => prev.map(d => { if (d.id !== editingDrawing) return d; if (d.points) { const newPoints = [...d.points]; if (editValues.p1) newPoints[0].price = parseFloat(editValues.p1); if (editValues.p2) newPoints[1].price = parseFloat(editValues.p2); if (editValues.p3 && newPoints[2]) newPoints[2].price = parseFloat(editValues.p3); return { ...d, points: newPoints }; } else { return { ...d, price: parseFloat(editValues.p1) }; } })); setEditingDrawing(null); };
  const deleteDrawing = (id) => setUserDrawings(prev => prev.filter(d => d.id !== id));
  const clearDrawings = () => { setUserDrawings([]); };
  const undoLastDrawing = () => { if (userDrawings.length > 0) setUserDrawings(prev => prev.slice(0, -1)); };

  useEffect(() => { if (!isMounted.current || !candleSeriesRef.current) return; drawingLinesRef.current.forEach(item => { try { candleSeriesRef.current.removePriceLine(item.ref); } catch(e){} }); drawingLinesRef.current = []; drawingSeriesRef.current.forEach(item => { try { chartRef.current.removeSeries(item.ref); } catch(e){} }); drawingSeriesRef.current = []; userDrawings.forEach(d => { if (d.type === 'horizontal') { const line = candleSeriesRef.current.createPriceLine({ price: d.price, color: '#38bdf8', lineWidth: 2, lineStyle: 0, axisLabelVisible: true, title: d.title }); drawingLinesRef.current.push({ type: 'line', ref: line }); } else if (d.type === 'rect') { const line = candleSeriesRef.current.createPriceLine({ price: d.price, color: '#FBBF24', lineWidth: 3, lineStyle: 2, axisLabelVisible: false, title: d.title }); drawingLinesRef.current.push({ type: 'line', ref: line }); } else if (d.type === 'fib') { const p1 = d.points[0]; const p2 = d.points[1]; const low = Math.min(p1.price, p2.price); const high = Math.max(p1.price, p2.price); const diff = high - low; const levels = [{l:0,c:'#fff',w:1},{l:0.382,c:'#FFD700',w:2},{l:0.5,c:'#3FB950',w:2},{l:0.618,c:'#FFD700',w:2},{l:1,c:'#fff',w:1}]; levels.forEach(lvl => { const line = candleSeriesRef.current.createPriceLine({ price: low + (diff * lvl.l), color: lvl.c, lineWidth: lvl.w, lineStyle: 2, axisLabelVisible: true, title: `Fib ${lvl.l}` }); drawingLinesRef.current.push({ type: 'line', ref: line }); }); } else if (d.type === 'trend') { const sorted = d.points[0].time > d.points[1].time ? [d.points[1], d.points[0]] : [d.points[0], d.points[1]]; const data = [{ time: sorted[0].time, value: sorted[0].price }, { time: sorted[1].time, value: sorted[1].price }]; const series = chartRef.current.addSeries(LineSeries, { color: '#ffffff', lineWidth: 2, lastValueVisible: false, priceLineVisible: false }); series.setData(data); drawingSeriesRef.current.push({ type: 'series', ref: series }); } else if (d.type === 'longshort') { const entry = d.points[0].price; const stop = d.points[1].price; const target = d.points[2].price; const rr = Math.abs((target - entry) / (entry - stop)).toFixed(2); const l1 = candleSeriesRef.current.createPriceLine({ price: entry, color: '#888', title: 'ENTRY' }); const l2 = candleSeriesRef.current.createPriceLine({ price: stop, color: '#F85149', title: 'STOP' }); const l3 = candleSeriesRef.current.createPriceLine({ price: target, color: '#3FB950', title: `TARGET R:R ${rr}` }); drawingLinesRef.current.push({ type: 'line', ref: l1 }, { type: 'line', ref: l2 }, { type: 'line', ref: l3 }); } }); }, [userDrawings]);

  const updateLayout = () => { if (!isMounted.current || !chartRef.current || !volumeSeriesRef.current) return; const paneIndicators = activeIndicators.filter(i => ['RSI', 'MACD', 'StochRSI', 'ADX', 'ATR'].includes(i.type)); const paneCount = paneIndicators.length; const PANE_HEIGHT = 0.2; const mainChartHeight = 1.0 - (paneCount * PANE_HEIGHT); chartRef.current.priceScale('right').applyOptions({ scaleMargins: { top: 0.05, bottom: paneCount * PANE_HEIGHT } }); volumeSeriesRef.current.priceScale().applyOptions({ scaleMargins: { top: mainChartHeight - 0.15, bottom: paneCount * PANE_HEIGHT } }); paneIndicators.forEach((ind, index) => { const bottomPos = index * PANE_HEIGHT; const topPos = 1.0 - ((index + 1) * PANE_HEIGHT); if (ind.paneId) chartRef.current.priceScale(ind.paneId).applyOptions({ scaleMargins: { top: topPos, bottom: bottomPos } }); }); };
  useEffect(() => { updateLayout(); }, [activeIndicators]);

  // --- FETCH DATA ---
  const fetchData = useCallback(async (isSilent = false) => {
    if (!symbol) return;
    if (!isSilent && abortControllerRef.current) abortControllerRef.current.abort();
    if (!isSilent) abortControllerRef.current = new AbortController();

    try {
      if (!isSilent) { setIsChartLoading(true); setHasError(false); }
      // Use Dynamic Base URL
      const baseUrl = getBaseApiUrl();
      const response = await axios.get(`${baseUrl}/api/stocks/${symbol}/chart?range=${timeframe}`, { signal: !isSilent ? abortControllerRef.current.signal : undefined });
      const data = response.data;
      const validData = (data || []).filter(d => d && d.time && typeof d.open === 'number');

      if (isMounted.current && chartRef.current && candleSeriesRef.current) {
          if (validData.length > 0) {
              setChartData(validData);
              lastCandleRef.current = validData[validData.length - 1];
              
              const isSMC = activeIndicators.some(i => i.type === 'SMC');
              if (isSMC) applySMC(validData); 
              else candleSeriesRef.current.setData(validData);
              
              if (volumeSeriesRef.current) volumeSeriesRef.current.setData(validData.map(d => ({ time: d.time, value: d.volume || 0, color: d.close >= d.open ? 'rgba(63, 185, 80, 0.4)' : 'rgba(248, 81, 73, 0.4)' })));
              if (!isSilent) chartRef.current.timeScale().fitContent();
              setIsLive(true);
          } else { setHasError(true); setChartData([]); }
      }
    } catch (err) { if (!axios.isCancel(err)) setHasError(true); setIsLive(false); } finally { if (!isSilent && isMounted.current) setIsChartLoading(false); }
  }, [symbol, timeframe]);
  useEffect(() => { fetchData(false); }, [symbol, timeframe]);

  // --- HYBRID SOCKET ENGINE ---
  useEffect(() => {
    if (!symbol) return;
    const userToken = localStorage.getItem('fyers_token');
    let pingInterval = null;
    let ws = null;
    
    // A. DIRECT BROKER CONNECTION
    if (userToken && isIndian && window.FyersSocket) {
        setConnectionType("Broker");
        const fyersSymbol = `NSE:${symbol.replace('.NS', '-EQ').replace('.BO', '-EQ')}`;
        try {
            const fyersSocket = new window.FyersSocket(userToken);
            fyersSocket.onmessage = (msg) => {
                const tick = msg.d?.[0] || msg[0];
                if (tick && tick.v && tick.v.lp) {
                     const price = parseFloat(tick.v.lp);
                     if (lastCandleRef.current && candleSeriesRef.current) {
                         const last = lastCandleRef.current;
                         const updatedCandle = { ...last, close: price, high: Math.max(last.high, price), low: Math.min(last.low, price) };
                         lastCandleRef.current = updatedCandle;
                         try { candleSeriesRef.current.update(updatedCandle); } catch(e){}
                     }
                }
            };
            fyersSocket.connect();
            fyersSocket.subscribe([fyersSymbol]);
            fyersEngineRef.current = { disconnect: () => fyersSocket.close() }; 
        } catch(e) {}
        
    } else {
        // B. SERVER BROADCAST
        setConnectionType("Server");
        
        // --- DYNAMIC WSS URL ---
        const getWsUrl = () => {
             const apiUrl = getBaseApiUrl();
             const wsProtocol = apiUrl.includes('https') ? 'wss://' : 'ws://';
             const host = apiUrl.replace(/^https?:\/\//, '').replace(/^http?:\/\//, '');
             return `${wsProtocol}${host}/ws/live/${symbol}`;
        };

        const connect = () => {
            try {
                ws = new WebSocket(getWsUrl());
                ws.onopen = () => { pingInterval = setInterval(() => { if (isMounted.current && ws.readyState === WebSocket.OPEN) { ws.send("ping"); } }, 10000); };
                ws.onmessage = (event) => {
                    if (!chartRef.current || !candleSeriesRef.current || !isMounted.current) return;
                    try {
                        const data = JSON.parse(event.data);
                        const currentPrice = data.price;
                        if (currentPrice && lastCandleRef.current) {
                            const last = lastCandleRef.current;
                            const updatedCandle = { ...last, close: currentPrice, high: Math.max(last.high, currentPrice), low: Math.min(last.low, currentPrice) };
                            lastCandleRef.current = updatedCandle;
                            try { candleSeriesRef.current.update(updatedCandle); } catch(e){}
                        }
                    } catch(e) {}
                };
                ws.onclose = () => { if (pingInterval) clearInterval(pingInterval); if (isMounted.current) setTimeout(connect, 3000); };
            } catch (e) {}
        };
        connect();
    }
    return () => { 
        if (pingInterval) clearInterval(pingInterval);
        if (ws) ws.close();
        if (fyersEngineRef.current) fyersEngineRef.current.disconnect();
    };
  }, [symbol, isIndian]);

  // --- INDICATORS ---
  const applySMC = (data) => { if (!isMounted.current || !candleSeriesRef.current) return; const { markers, coloredCandles, priceLines } = calculateSMC(data); const coloredData = data.map(d => { const override = coloredCandles.find(c => c.time === d.time); return override ? { ...d, ...override } : d; }); candleSeriesRef.current.setData(coloredData); if (candleSeriesRef.current.setMarkers) candleSeriesRef.current.setMarkers(markers); priceLinesRef.current.forEach(line => { try { candleSeriesRef.current.removePriceLine(line); } catch(e){} }); priceLinesRef.current = []; priceLines.slice(-5).forEach(lineData => { if (candleSeriesRef.current.createPriceLine) { const lineObj = candleSeriesRef.current.createPriceLine({ price: lineData.price, color: lineData.color, lineWidth: 2, lineStyle: 0, axisLabelVisible: true, title: lineData.title, }); priceLinesRef.current.push(lineObj); } }); };
  useEffect(() => { if (!isMounted.current || !chartRef.current || chartData.length === 0) return; const isSMC = activeIndicators.some(i => i.type === 'SMC'); if (isSMC) applySMC(chartData); else { candleSeriesRef.current.setData(chartData); if (candleSeriesRef.current.setMarkers) candleSeriesRef.current.setMarkers([]); priceLinesRef.current.forEach(line => { try { candleSeriesRef.current.removePriceLine(line); } catch(e){} }); priceLinesRef.current = []; } }, [chartData, activeIndicators]);

  const addIndicator = () => {
    if (!isMounted.current || !chartData.length || !chartRef.current) return;
    const closePrices = chartData.map(d => d.close);
    const highs = chartData.map(d => d.high);
    const lows = chartData.map(d => d.low);
    const volumes = chartData.map(d => d.volume);
    const id = Date.now();
    let newSeries = [];
    let paneId = ['RSI', 'MACD', 'StochRSI', 'ADX', 'ATR'].includes(selectedInd) ? `pane_${id}` : undefined;
    let paramsLabel = '';

    try {
        if (selectedInd === 'SMC') {} 
        else if (selectedInd === 'SMA') {
            const period = parseInt(param1);
            const res = SMA.calculate({period, values: closePrices});
            const series = chartRef.current.addSeries(LineSeries, { color: '#FF9800', lineWidth: 2, title: `SMA ${period}` });
            series.setData(mapData(res, chartData));
            newSeries.push(series);
            paramsLabel = `${period}`;
        }
        else if (selectedInd === 'EMA') {
            const period = parseInt(param1);
            const res = EMA.calculate({period, values: closePrices});
            const series = chartRef.current.addSeries(LineSeries, { color: '#2962FF', lineWidth: 2, title: `EMA ${period}` });
            series.setData(mapData(res, chartData));
            newSeries.push(series);
            paramsLabel = `${period}`;
        }
        else if (selectedInd === 'SuperTrend') {
            const period = parseInt(param1);
            const mult = parseFloat(param3);
            const stData = calculateSuperTrend(chartData, period, mult);
            const series = chartRef.current.addSeries(LineSeries, { color: '#00E676', lineWidth: 2, title: `ST ${period}/${mult}` });
            series.setData(stData);
            newSeries.push(series);
            paramsLabel = `${period}, ${mult}`;
        }
        else if (selectedInd === 'VWAP') {
            const res = VWAP.calculate({ high: highs, low: lows, close: closePrices, volume: volumes });
            const series = chartRef.current.addSeries(LineSeries, { color: '#FFD700', lineWidth: 2, title: `VWAP` });
            series.setData(mapData(res, chartData));
            newSeries.push(series);
        }
        else if (selectedInd === 'RSI') {
            const res = RSI.calculate({ values: closePrices, period: parseInt(param1) });
            const series = chartRef.current.addSeries(LineSeries, { color: '#A855F7', lineWidth: 2, priceScaleId: paneId, title: `RSI (${param1})` });
            series.setData(mapData(res, chartData));
            newSeries.push(series);
            chartRef.current.priceScale(paneId).applyOptions({ scaleMargins: { top: 0.8, bottom: 0 } });
            paramsLabel = `${param1}`;
        }
        else if (selectedInd === 'MACD') {
            const macdInput = { values: closePrices, fastPeriod: parseInt(param1), slowPeriod: parseInt(param2), signalPeriod: parseInt(param3), SimpleMAOscillator: false, SimpleMASignal: false };
            const res = MACD.calculate(macdInput);
            const mLine = []; const sLine = []; const hLine = [];
            for(let i=0; i<res.length; i++){ const dIndex = chartData.length - 1 - i; const rIndex = res.length - 1 - i; if (dIndex >= 0){ const t = chartData[dIndex].time; const m = res[rIndex]; mLine.unshift({ time: t, value: m.MACD }); sLine.unshift({ time: t, value: m.signal }); hLine.unshift({ time: t, value: m.histogram, color: m.histogram >= 0 ? '#26a69a' : '#ef5350' }); } }
            const hSeries = chartRef.current.addSeries(HistogramSeries, { priceScaleId: paneId });
            const mSeries = chartRef.current.addSeries(LineSeries, { color: '#2962FF', lineWidth: 2, priceScaleId: paneId });
            const sSeries = chartRef.current.addSeries(LineSeries, { color: '#FF6D00', lineWidth: 2, priceScaleId: paneId });
            hSeries.setData(hLine); mSeries.setData(mLine); sSeries.setData(sLine);
            newSeries = [hSeries, mSeries, sSeries];
            chartRef.current.priceScale(paneId).applyOptions({ scaleMargins: { top: 0.8, bottom: 0 } });
            paramsLabel = `${param1},${param2},${param3}`;
        }
        else if (selectedInd === 'StochRSI') {
            const stochInput = { values: closePrices, rsiPeriod: parseInt(param1), stochasticPeriod: parseInt(param2), kPeriod: 3, dPeriod: 3 };
            const res = StochasticRSI.calculate(stochInput);
            const kLine = []; const dLine = [];
            for(let i=0; i<res.length; i++){ const dIndex = chartData.length - 1 - i; const sIndex = res.length - 1 - i; if (dIndex >= 0) { kLine.unshift({ time: chartData[dIndex].time, value: res[sIndex].k }); dLine.unshift({ time: chartData[dIndex].time, value: res[sIndex].d }); } }
            const kSeries = chartRef.current.addSeries(LineSeries, { color: '#2962FF', title: '%K', priceScaleId: paneId });
            const dSeries = chartRef.current.addSeries(LineSeries, { color: '#FF6D00', title: '%D', priceScaleId: paneId });
            kSeries.setData(kLine); dSeries.setData(dLine);
            newSeries = [kSeries, dSeries];
            chartRef.current.priceScale(paneId).applyOptions({ scaleMargins: { top: 0.8, bottom: 0 } });
            paramsLabel = `${param1},${param2}`;
        }
        else if (selectedInd === 'ADX') {
            const res = ADX.calculate({ high: highs, low: lows, close: closePrices, period: parseInt(param1) });
            const series = chartRef.current.addSeries(LineSeries, { color: '#FF0055', lineWidth: 2, priceScaleId: paneId, title: `ADX (${param1})` });
            series.setData(mapData(res.map(r=>r.adx), chartData));
            newSeries.push(series);
            paramsLabel = `${param1}`;
        }
        else if (selectedInd === 'ATR') {
            const res = ATR.calculate({ high: highs, low: lows, close: closePrices, period: parseInt(param1) });
            const series = chartRef.current.addSeries(LineSeries, { color: '#AB47BC', lineWidth: 2, priceScaleId: paneId, title: `ATR (${param1})` });
            series.setData(mapData(res, chartData));
            newSeries.push(series);
            paramsLabel = `${param1}`;
        }
        else if (selectedInd === 'Combo_9_21') {
             const ema1 = EMA.calculate({ period: 9, values: closePrices });
             const ema2 = EMA.calculate({ period: 21, values: closePrices });
             const s1 = chartRef.current.addSeries(LineSeries, { color: '#2962FF', lineWidth: 2, title: `EMA 9` });
             const s2 = chartRef.current.addSeries(LineSeries, { color: '#FF6D00', lineWidth: 2, title: `EMA 21` });
             s1.setData(mapData(ema1, chartData));
             s2.setData(mapData(ema2, chartData));
             newSeries.push(s1, s2);
             paramsLabel = `9, 21`;
        }
        else if (selectedInd === 'Combo_12_21') {
             const ema1 = EMA.calculate({ period: 12, values: closePrices });
             const ema2 = EMA.calculate({ period: 21, values: closePrices });
             const s1 = chartRef.current.addSeries(LineSeries, { color: '#2962FF', lineWidth: 2, title: `EMA 12` });
             const s2 = chartRef.current.addSeries(LineSeries, { color: '#FF6D00', lineWidth: 2, title: `EMA 21` });
             s1.setData(mapData(ema1, chartData));
             s2.setData(mapData(ema2, chartData));
             newSeries.push(s1, s2);
             paramsLabel = `12, 21`;
        }

        setActiveIndicators([...activeIndicators, { id, type: selectedInd, series: newSeries, paneId, params: paramsLabel }]);
        setIsMenuOpen(false);
    } catch (e) {
        console.error("Indicator Error", e);
    }
  };

  const handleDropdownChange = (e) => { const val = e.target.value; setSelectedInd(val); if (val === 'Combo_9_21') { setParam1(9); setParam2(21); } else if (val === 'Combo_12_21') { setParam1(12); setParam2(21); } };
  const removeIndicator = (id) => { const indToRemove = activeIndicators.find(i => i.id === id); if (!indToRemove) return; if (indToRemove.type !== 'SMC') { if (chartRef.current) indToRemove.series.forEach(s => chartRef.current.removeSeries(s)); } setActiveIndicators(activeIndicators.filter(i => i.id !== id)); };

  const timeframesList = ['5M', '15M', '1H', '4H', '1D', '1W', '1M'];
  let helpText = ''; if (drawMode === 'fib') helpText = 'Click Low then High'; if (drawMode === 'trend') helpText = 'Click Start then End'; if (drawMode === 'longshort') helpText = 'Click Entry, Stop, Target';

  return (
    <ChartWrapper>
      {/* ... (UI Components - Same as previous, ensured complete) ... */}
      <DrawingSidebar><ToolBtn active={drawMode === 'cursor'} onClick={() => setDrawMode('cursor')} title="Cursor"><FaMousePointer /></ToolBtn><ToolBtn active={drawMode === 'horizontal'} onClick={() => setDrawMode('horizontal')} title="Horizontal Line"><FaMinus /></ToolBtn><ToolBtn active={drawMode === 'trend'} onClick={() => setDrawMode('trend')} title="Trend Line"><FaSlash /></ToolBtn><ToolBtn active={drawMode === 'fib'} onClick={() => setDrawMode('fib')} title="Fibonacci Retracement"><FaListOl /></ToolBtn><ToolBtn active={drawMode === 'rect'} onClick={() => setDrawMode('rect')} title="Zone (Box)"><FaVectorSquare /></ToolBtn><ToolBtn active={drawMode === 'longshort'} onClick={() => setDrawMode('longshort')} title="Long/Short Tool"><FaBalanceScale /></ToolBtn><ToolBtn onClick={undoLastDrawing} title="Undo Last"><FaUndo /></ToolBtn><ToolBtn onClick={clearDrawings} title="Clear All" style={{color: '#F85149'}}><FaEraser /></ToolBtn></DrawingSidebar>
      {userDrawings.length > 0 && (<LayersPanel><LayerHeader><span>Drawing Layers</span></LayerHeader>{userDrawings.map((d, i) => (<LayerItem key={d.id}><span>{d.type === 'horizontal' ? 'H-Line' : d.type === 'rect' ? 'Zone' : d.type === 'fib' ? 'Fibonacci' : d.type.toUpperCase()}</span><LayerActions><IconButton onClick={() => handleEdit(d)}><FaPencilAlt size={10} /></IconButton><IconButton className="delete" onClick={() => deleteDrawing(d.id)}><FaTrash size={10} /></IconButton></LayerActions></LayerItem>))}</LayersPanel>)}
      {editingDrawing && (<EditModal><ModalTitle>Edit Drawing</ModalTitle><ModalInput><label>Price / Level 1</label><input type="number" value={editValues.p1} onChange={e=>setEditValues({...editValues, p1: e.target.value})} /></ModalInput>{editValues.p2 !== undefined && <ModalInput><label>Price / Level 2</label><input type="number" value={editValues.p2} onChange={e=>setEditValues({...editValues, p2: e.target.value})} /></ModalInput>}{editValues.p3 !== undefined && <ModalInput><label>Price / Level 3</label><input type="number" value={editValues.p3} onChange={e=>setEditValues({...editValues, p3: e.target.value})} /></ModalInput>}<ModalActions><AddButton onClick={() => setEditingDrawing(null)} style={{background:'#30363D'}}>Cancel</AddButton><AddButton onClick={saveEdit}>Save Changes</AddButton></ModalActions></EditModal>)}
      <Toolbar>
        <LeftGroup>
            <div style={{display:'flex', gap:'4px'}}>
            {timeframesList.map((tf) => (
                <RangeButton key={tf} active={timeframe === tf} onClick={() => setTimeframe(tf)}>{tf}</RangeButton>
            ))}
            </div>
            <div style={{position: 'relative'}}>
                <IndicatorButton onClick={() => setIsMenuOpen(!isMenuOpen)}><FaLayerGroup /> Indicators <FaPlus size={10}/></IndicatorButton>
                {isMenuOpen && (
                    <Dropdown>
                        <select style={{background: '#0D1117', color:'white', padding:'5px', borderRadius:'4px', width:'100%'}} value={selectedInd} onChange={handleDropdownChange}>
                            <option value="SMC">⚡ SMC</option><option value="Combo_9_21">🚀 9/21 EMA</option><option value="Combo_12_21">🚀 12/21 EMA</option><option value="SuperTrend">SuperTrend</option><option value="VWAP">VWAP</option><option value="SMA">SMA</option><option value="EMA">EMA</option><option value="RSI">RSI</option><option value="MACD">MACD</option><option value="StochRSI">Stoch RSI</option><option value="ADX">ADX</option><option value="ATR">ATR</option>
                        </select>
                        {selectedInd !== 'SMC' && selectedInd !== 'VWAP' && ( <><div style={{fontSize:'0.8rem', color:'#8b949e'}}>Settings:</div><InputGroup><StyledInput type="number" value={param1} onChange={e=>setParam1(e.target.value)} title="Period/Fast" />{['MACD', 'StochRSI'].includes(selectedInd) && (<><StyledInput type="number" value={param2} onChange={e=>setParam2(e.target.value)} title="Slow" /><StyledInput type="number" value={param3} onChange={e=>setParam3(e.target.value)} title="Signal" /></>)}{selectedInd === 'SuperTrend' && ( <StyledInput type="number" value={param3} onChange={e=>setParam3(e.target.value)} title="Multiplier" /> )}</InputGroup></> )}
                        <AddButton onClick={addIndicator}>Add {selectedInd}</AddButton>
                    </Dropdown>
                )}
            </div>
        </LeftGroup>
        <div style={{display:'flex', gap:'5px', overflowX:'auto'}}>
            {activeIndicators.map(ind => (
                <IndicatorTag key={ind.id}>{ind.type} {ind.params && `(${ind.params})`}<CloseIcon onClick={() => removeIndicator(ind.id)} /></IndicatorTag>
            ))}
        </div>
        <StatusText isLive={isLive}>
            {isLive ? (
                <>
                    <PulseDot /> {connectionType === "Broker" ? "BROKER FEED" : "LIVE"}
                    {connectionType === "Broker" && <FaPlug style={{marginLeft:'5px'}} />}
                </>
            ) : <><FaSpinner className="fa-spin" style={{fontSize:'0.8rem'}}/> LOADING...</>}
        </StatusText>
      </Toolbar>
      
      {isChartLoading && ( <LoadingOverlay><FaSpinner className="fa-spin" /></LoadingOverlay> )}
      {hasError && !isChartLoading && (
          <NoDataOverlay>
              <FaExclamationTriangle style={{fontSize: '2rem', marginBottom: '10px'}} />
              <span>Chart Data Unavailable</span>
          </NoDataOverlay>
      )}
      {drawMode !== 'cursor' && <HelperText>{helpText}</HelperText>}
      <ChartContainer ref={chartContainerRef} crosshair={drawMode !== 'cursor'} />
    </ChartWrapper>
  );
};

export default CustomChart;
```

## File: frontend/src/pages/HomePage.js
```javascript
import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import styled, { keyframes, css } from 'styled-components';
import axios from 'axios';
import { 
  FaSearch, FaChartBar, FaGlobeAmericas, FaSpinner, 
  FaBitcoin, FaBrain, FaMicrochip, FaFileUpload 
} from 'react-icons/fa';

// --- COMPONENTS ---
import IndicesBanner from '../components/Indices/IndicesBanner';
import ChartUploader from '../components/HomePage/ChartUploader';

// --- CONFIG ---
// This connects Vercel Frontend to Railway Backend
const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

// ==========================================
// 1. CINEMATIC ANIMATIONS
// ==========================================

const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
`;

const float = keyframes`
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
`;

const floatReverse = keyframes`
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(-30px, 50px) scale(0.9); }
  66% { transform: translate(20px, -20px) scale(1.1); } 
  100% { transform: translate(0px, 0px) scale(1); }
`;

const scanBeam = keyframes`
  0% { left: -100%; opacity: 0; }
  50% { opacity: 1; }
  100% { left: 100%; opacity: 0; }
`;

const pulseGlow = keyframes`
  0% { box-shadow: 0 0 5px rgba(88, 166, 255, 0.4); }
  50% { box-shadow: 0 0 20px rgba(88, 166, 255, 0.8); }
  100% { box-shadow: 0 0 5px rgba(88, 166, 255, 0.4); }
`;

// ==========================================
// 2. HIGH-END STYLED COMPONENTS
// ==========================================

const HomePageContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  padding: 1rem;
  width: 100%;
  position: relative;
  overflow-x: hidden;
  background-color: var(--color-background);
  
  @media (min-width: 768px) {
    padding: 2rem;
  }
`;

const BackgroundLayer = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
`;

const GlowingBlob = styled.div`
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.25;
  animation: ${float} 15s ease-in-out infinite;
`;

const BlobOne = styled(GlowingBlob)`
  top: -10%;
  left: -10%;
  width: 60vw;
  height: 60vw;
  background: var(--color-primary);
`;

const BlobTwo = styled(GlowingBlob)`
  bottom: -10%;
  right: -10%;
  width: 70vw;
  height: 70vw;
  background: #7c3aed; /* Deep Purple */
  animation: ${floatReverse} 18s ease-in-out infinite;
`;

const MainContent = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    width: 100%;
    margin-top: 5vh;
    z-index: 1;
    position: relative;
    
    @media (min-width: 768px) {
        margin-top: 8vh;
    }
`;

const Title = styled.h1`
  font-size: 2.8rem;
  font-weight: 900;
  background: linear-gradient(to right, #fff, #a5b4fc);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1rem;
  animation: ${fadeIn} 1s ease-out;
  letter-spacing: -1.5px;
  text-shadow: 0 10px 40px rgba(0,0,0,0.5);
  
  @media (min-width: 768px) {
    font-size: 4.5rem;
  }
`;

const Subtitle = styled.p`
  font-size: 1rem;
  color: var(--color-text-secondary);
  margin-bottom: 3.5rem;
  max-width: 650px;
  animation: ${fadeIn} 1.5s ease-out;
  padding: 0 1.5rem;
  line-height: 1.8;
  font-weight: 400;
  
  @media (min-width: 768px) {
    font-size: 1.25rem;
  }
`;

// --- SEARCH BAR (GLASS) ---

const SearchSection = styled.div`
  width: 100%;
  max-width: 700px;
  position: relative;
  animation: ${fadeIn} 1.8s ease-out;
  z-index: 50;
`;

const SearchWrapper = styled.div`
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
  transition: transform 0.3s ease;

  &:hover {
    transform: scale(1.01);
  }
`;

const SearchInput = styled.input`
  width: 100%;
  padding: 20px 30px;
  padding-right: 80px;
  font-size: 1.1rem;
  color: #fff;
  background: rgba(22, 27, 34, 0.6); 
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 60px;
  outline: none;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4);

  &::placeholder {
    color: rgba(255, 255, 255, 0.4);
  }

  &:focus {
    border-color: var(--color-primary);
    box-shadow: 0 0 30px rgba(88, 166, 255, 0.3);
    background: rgba(22, 27, 34, 0.9);
  }
`;

const SearchButton = styled.button`
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: linear-gradient(135deg, var(--color-primary), #3b82f6);
  color: white;
  border: none;
  border-radius: 50%;
  width: 54px;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 5px 20px rgba(59, 130, 246, 0.5);

  &:hover {
    transform: translateY(-50%) scale(1.1);
    box-shadow: 0 8px 25px rgba(59, 130, 246, 0.7);
  }
  
  &:active {
    transform: translateY(-50%) scale(0.95);
  }

  &:disabled {
    filter: grayscale(1);
    cursor: default;
  }
`;

// --- AUTOCOMPLETE ---

const SuggestionsList = styled.ul`
  position: absolute;
  top: 110%;
  left: 15px;
  right: 15px;
  background: rgba(22, 27, 34, 0.95);
  backdrop-filter: blur(25px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  box-shadow: 0 25px 50px rgba(0,0,0,0.6);
  list-style: none;
  padding: 5px;
  max-height: 400px;
  overflow-y: auto;
  z-index: 100;
  
  &::-webkit-scrollbar { width: 6px; }
  &::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
`;

const SuggestionItem = styled.li`
  padding: 16px 20px;
  border-radius: 12px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.2s ease;
  margin-bottom: 2px;

  &:hover { 
    background-color: rgba(88, 166, 255, 0.15); 
  }
`;

const SuggestionSymbol = styled.span`
  font-weight: 700;
  font-size: 1rem;
  color: var(--color-primary);
  font-family: 'Roboto Mono', monospace;
  display: flex;
  align-items: center;
  gap: 8px;
`;

const SuggestionName = styled.span`
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 250px;
`;

const SuggestionBadge = styled.span`
  font-size: 0.7rem;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.1);
  padding: 4px 10px;
  border-radius: 20px;
  color: var(--color-text-secondary);
  font-weight: 600;
  text-transform: uppercase;
`;

const LoadingText = styled.p`
  color: var(--color-primary); 
  margin-top: 1.5rem; 
  height: 24px; 
  font-weight: 600;
  letter-spacing: 0.5px;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 10px;
`;

// --- GRID & SECTIONS ---

const SectionLabel = styled.div`
  display: flex;
  align-items: center;
  gap: 15px;
  color: var(--color-text-secondary);
  margin: 4rem 0 2rem 0;
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  width: 100%;
  max-width: 1200px;
  
  &::before, &::after {
    content: '';
    height: 1px;
    flex-grow: 1;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
  }
`;

const UploadGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  width: 100%;
  max-width: 1200px;
  padding: 0 1rem;
  animation: ${fadeIn} 2s ease-out;

  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    max-width: 500px;
  }
`;

// --- QUANTUM VISION SECTION (NEW) ---

const VisionContainer = styled.div`
  width: 100%;
  max-width: 1200px;
  margin-bottom: 4rem;
  padding: 0 1rem;
  animation: ${fadeIn} 2.2s ease-out;
`;

const VisionCard = styled.div`
  background: linear-gradient(165deg, rgba(22, 27, 34, 0.8), rgba(13, 17, 23, 0.95));
  border: 1px solid rgba(88, 166, 255, 0.3);
  border-radius: 24px;
  padding: 4rem 2rem;
  text-align: center;
  position: relative;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0,0,0,0.4);
  transition: all 0.4s ease;

  &:hover {
    border-color: #58A6FF;
    box-shadow: 0 20px 60px rgba(88, 166, 255, 0.15);
  }
`;

const VisionGlow = styled.div`
  position: absolute;
  top: -50%;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 100%;
  background: radial-gradient(circle, rgba(88, 166, 255, 0.15) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
`;

const ScanBeam = styled.div`
  position: absolute;
  top: 0;
  left: -100%;
  width: 50%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
  transform: skewX(-20deg);
  animation: ${scanBeam} 4s infinite linear;
  pointer-events: none;
`;

const VisionTitle = styled.h2`
  font-size: 2.2rem;
  margin-bottom: 1rem;
  color: #fff;
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;

  svg { color: #58A6FF; }
`;

const VisionDesc = styled.p`
  color: #8B949E;
  font-size: 1.1rem;
  max-width: 700px;
  margin: 0 auto 3rem auto;
  line-height: 1.7;
  position: relative;
  z-index: 1;
`;

const DeepScanButton = styled.label`
  background: #58A6FF;
  color: #0D1117;
  padding: 16px 40px;
  border-radius: 50px;
  font-weight: 800;
  font-size: 1.1rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 12px;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  z-index: 2;
  box-shadow: 0 0 25px rgba(88, 166, 255, 0.4);

  &:hover {
    transform: translateY(-3px) scale(1.05);
    background: #fff;
    box-shadow: 0 0 40px rgba(255, 255, 255, 0.6);
  }

  &:active {
    transform: translateY(0) scale(0.98);
  }
`;

// ==========================================
// 3. MAIN COMPONENT LOGIC
// ==========================================

const HomePage = () => {
  const [query, setQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isAutoCompleting, setIsAutoCompleting] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [isVisionLoading, setIsVisionLoading] = useState(false);
  const [error, setError] = useState('');
  
  const navigate = useNavigate();
  const searchRef = useRef(null);

  // --- AUTOCOMPLETE ENGINE ---
  useEffect(() => {
    if (query.length < 2) {
      setSuggestions([]);
      setShowSuggestions(false);
      return;
    }

    setIsAutoCompleting(true);
    const delayDebounceFn = setTimeout(async () => {
      try {
        // FIX: Use API_URL
        const response = await axios.get(`${API_URL}/api/stocks/autocomplete?query=${query}`);
        if (Array.isArray(response.data) && response.data.length > 0) {
            setSuggestions(response.data);
            setShowSuggestions(true);
        } else {
            setSuggestions([]);
            setShowSuggestions(false);
        }
      } catch (error) {
        console.warn("Autocomplete silent fail");
      } finally {
        setIsAutoCompleting(false);
      }
    }, 250); 

    return () => clearTimeout(delayDebounceFn);
  }, [query]);

  // --- SEARCH HANDLER ---
  const performSearch = async (searchQuery = query) => {
    const target = searchQuery.trim();
    if (!target) return;

    setIsSearching(true);
    setError('');
    setShowSuggestions(false);
    
    try {
      // FIX: Use API_URL
      const response = await axios.get(`${API_URL}/api/stocks/search?query=${target}`);
      navigate(`/stock/${response.data.symbol}`);
    } catch (err) {
      setError('Ticker not found. Please try a valid symbol.');
    } finally {
      setIsSearching(false);
    }
  };

  // --- QUANTUM VISION HANDLER ---
  const handleVisionUpload = async (e) => {
      const file = e.target.files[0];
      if (!file) return;

      setIsVisionLoading(true);
      setError("");

      const formData = new FormData();
      formData.append('chart_image', file);

      try {
          // FIX: Use API_URL
          const res = await axios.post(`${API_URL}/api/charts/analyze-pure`, formData);
          
          navigate('/vision-result', { 
              state: { 
                  analysis: res.data.analysis, 
                  image: URL.createObjectURL(file) 
              } 
          });
      } catch (err) {
          console.error("Vision Error:", err);
          setError("Vision Scan Failed. Please try a clearer image.");
          setIsVisionLoading(false);
      }
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [searchRef]);

  return (
    <HomePageContainer>
      <BackgroundLayer><BlobOne /><BlobTwo /></BackgroundLayer>
      <IndicesBanner />
      
      <MainContent>
        <Title>Stellar Stock Screener</Title>
        <Subtitle>The Ultimate Financial Intelligence Platform.<br />Leveraging Neural Networks & Quantitative Models for Real-Time Analysis.</Subtitle>
        
        <SearchSection ref={searchRef}>
          <SearchWrapper>
            <SearchInput
              type="text"
              placeholder="Search (e.g. Reliance, Bitcoin, Gold, Apple)..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && performSearch()}
              onFocus={() => query.length >= 2 && setShowSuggestions(true)}
              disabled={isSearching}
              spellCheck={false}
            />
            <SearchButton onClick={() => performSearch()} disabled={isSearching || isAutoCompleting}>
              {isSearching ? <FaSpinner className="fa-spin" size={20} /> : <FaSearch size={20} />}
            </SearchButton>
          </SearchWrapper>

          {showSuggestions && (
            <SuggestionsList>
              {suggestions.map((item) => (
                <SuggestionItem key={item.symbol} onClick={() => { setQuery(item.symbol); performSearch(item.symbol); }}>
                  <div style={{display:'flex', flexDirection:'column'}}>
                    <SuggestionSymbol>{item.symbol}</SuggestionSymbol>
                    <SuggestionName>{item.name}</SuggestionName>
                  </div>
                  <SuggestionBadge>
                     {item.exchangeShortName || (item.symbol.includes('.') ? 'INTL' : 'US')}
                  </SuggestionBadge>
                </SuggestionItem>
              ))}
            </SuggestionsList>
          )}
        </SearchSection>

        <LoadingText>{isSearching && <><FaSpinner className="fa-spin"/> Establishing Data Uplink...</>}{error && <span style={{color:'#F85149'}}>{error}</span>}</LoadingText>
        
        <SectionLabel>AI Analyst Suite</SectionLabel>
        <UploadGrid>
            <ChartUploader type="stock" title="Stocks" description="Equities & ETFs (NSE, BSE, NASDAQ)." color="#58A6FF" icon={<FaChartBar />} />
            <ChartUploader type="index" title="Indices" description="Macro Analysis (Nifty 50, SPX)." color="#EBCB8B" icon={<FaGlobeAmericas />} />
            <ChartUploader type="crypto" title="Crypto / Commodities" description="Bitcoin, Gold, Oil & Global Assets." color="#D500F9" icon={<FaBitcoin />} />
        </UploadGrid>

        <SectionLabel>Pure Vision Labs</SectionLabel>
        <VisionContainer>
            <VisionCard>
                <VisionGlow /><ScanBeam />
                <VisionTitle><FaBrain /> Quantum Vision Engine<FaMicrochip style={{fontSize:'1.5rem', opacity:0.5}}/></VisionTitle>
                <VisionDesc>Upload any financial chart image. Our proprietary Vision Model will perform a <strong>Geometric & Mathematical Breakdown</strong> of price action, identifying hidden liquidity zones and institutional footprints <strong>without needing any external data feed</strong>.</VisionDesc>
                <DeepScanButton htmlFor="vision-upload">
                    {isVisionLoading ? (<><FaSpinner className="fa-spin"/> PROCESSING PIXELS...</>) : (<><FaFileUpload /> PERFORM DEEP SCAN</>)}
                </DeepScanButton>
                <input id="vision-upload" type="file" style={{display: 'none'}} accept="image/*" onChange={handleVisionUpload} disabled={isVisionLoading}/>
            </VisionCard>
        </VisionContainer>
      </MainContent>
    </HomePageContainer>
  );
};

export default HomePage;
```

## File: backend/app/services/gemini_service.py
```python
import os
import google.generativeai as genai
from dotenv import load_dotenv
import itertools

load_dotenv()

# --- 1. API KEY ROTATOR (CRITICAL FOR STABILITY) ---
try:
    GEMINI_API_KEYS_STR = os.getenv("GEMINI_API_KEYS")
    if not GEMINI_API_KEYS_STR:
        # Fallback to single key if list is not found
        single_key = os.getenv("GEMINI_API_KEY") 
        if single_key:
            GEMINI_API_KEYS = [single_key]
        else:
            raise ValueError("GEMINI_API_KEYS not found in .env file.")
    else:
        # Clean and split the keys
        GEMINI_API_KEYS = [key.strip() for key in GEMINI_API_KEYS_STR.split(',')]
    
    # Create a cycle iterator that loops forever
    key_cycler = itertools.cycle(GEMINI_API_KEYS)
    print(f"Successfully loaded and initialized rotator for {len(GEMINI_API_KEYS)} Gemini API keys.")

except Exception as e:
    print(f"CRITICAL ERROR: Could not load Gemini API keys. AI features will fail. Error: {e}")
    GEMINI_API_KEYS = []
    key_cycler = None

def configure_gemini_for_request():
    """Configures the genai library with the next available key from the pool."""
    if not key_cycler:
        raise ValueError("No Gemini API keys are configured or available.")
    
    # Rotate to the next key
    api_key = next(key_cycler)
    genai.configure(api_key=api_key)


# --- 2. TEXT ANALYSIS FUNCTIONS ---

def get_ticker_from_query(query: str):
    """Identifies the stock ticker from a natural language query."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        prompt = f"""Analyze the following user query: "{query}". Return ONLY the official stock ticker symbol (e.g., "AAPL" for Apple, "RELIANCE.NS" for Reliance Industries). If a clear ticker cannot be found, return the text "NOT_FOUND"."""
        response = model.generate_content(prompt)
        return response.text.strip().replace("`", "").upper()
    except Exception as e:
        print(f"Error in get_ticker_from_query: {e}")
        return "ERROR"

def generate_swot_analysis(company_name: str, description: str, news_headlines: list):
    """Generates a SWOT analysis."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        news_string = "\n- ".join(news_headlines)
        prompt = f"""Generate a 4-section SWOT analysis for {company_name}. Use the following data for context. Structure the output with clear headers for Strengths, Weaknesses, Opportunities, and Threats, each followed by bullet points.\n\n**Company Description:**\n{description}\n\n**Recent News Headlines:**\n- {news_string}"""
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in generate_swot_analysis: {e}")
        return "Could not generate SWOT analysis."

def generate_forecast_analysis(company_name: str, analyst_ratings: list, price_target: dict, key_stats: dict, news_headlines: list, currency: str = "USD"):
    """Generates a summary of analyst forecasts with correct currency."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        ratings_summary = "\n".join([f"- {r.get('ratingStrongBuy', 0)} Strong Buy, {r.get('ratingBuy', 0)} Buy, {r.get('ratingHold', 0)} Hold, {r.get('ratingSell', 0)} Sell, {r.get('ratingStrongSell', 0)} Strong Sell" for r in analyst_ratings[:1]])
        news_string = "\n- ".join(news_headlines)
        
        # Determine symbol for prompt context
        curr_symbol = "₹" if currency == "INR" else "$" if currency == "USD" else currency

        prompt = f"""Act as a professional financial analyst. For {company_name} (Currency: {currency}), write a two-paragraph summary of the analyst forecast.
        
        **Instructions:**
        - STRICTLY use the currency symbol '{curr_symbol}' for ALL monetary values.
        - Do not use '$' if the currency is INR.
        
        **Data:**
        - **Analyst Ratings:** {ratings_summary}
        - **Price Target:** High {curr_symbol}{price_target.get('targetHigh')}, Average {curr_symbol}{price_target.get('targetConsensus')}, Low {curr_symbol}{price_target.get('targetLow')}
        - **Recent News:**\n- {news_string}"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in generate_forecast_analysis: {e}")
        return "Could not generate AI forecast analysis."

def generate_investment_philosophy_assessment(company_name: str, key_metrics: dict):
    """
    Generates assessment. 
    HYBRID MODE: Tries AI first. If AI fails (429/Quota), falls back to Algorithmic Logic.
    """
    # 1. Prepare Data Safe Variables
    pe = key_metrics.get('peRatioTTM')
    ey = key_metrics.get('earningsYieldTTM')
    roc = key_metrics.get('returnOnCapitalEmployedTTM')
    
    # Numeric values for math (Default to 0)
    pe_val = float(pe) if pe is not None else 0.0
    ey_val = float(ey) if ey is not None else 0.0
    roc_val = float(roc) if roc is not None else 0.0
    
    # String formatting for display
    pe_str = f"{pe_val:.2f}" if pe is not None else "N/A"
    ey_str = f"{ey_val:.2%}" if ey is not None else "N/A"
    roc_str = f"{roc_val:.2%}" if roc is not None else "N/A"

    try:
        # --- PLAN A: ASK AI ---
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        data_summary = (
            f"- Price to Earnings (P/E): {pe_str}\n"
            f"- Earnings Yield (Greenblatt): {ey_str}\n"
            f"- Return on Capital (ROC/ROE): {roc_str}"
        )
        
        prompt = f"""
        Act as a Value Investor. Analyze {company_name} based on:
        {data_summary}
        
        Evaluate against:
        1. Greenblatt's Magic Formula (High Yield + High ROC)
        2. Warren Buffett's Moat (High ROC)
        3. Ben Graham Value (Low P/E)
        
        Output a 2-column Markdown table with headers "Formula" and "Assessment".
        Assessment should be 1 short sentence.
        """
        
        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        print(f"Gemini 429/Error (Philosophy): {e}")
        
        # --- PLAN B: ALGORITHMIC FALLBACK (The Crash Fix) ---
        # We calculate the verdict manually so the user NEVER sees an error text.
        
        # 1. Magic Formula Logic
        if ey_val > 0.05 and roc_val > 0.15:
            magic_text = f"**Pass**. Attractive Yield ({ey_str}) and High Efficiency ({roc_str})."
        else:
            magic_text = f"**Fail**. Requires Earnings Yield > 5% and ROC > 15%."
            
        # 2. Buffett Moat Logic
        if roc_val > 0.15:
            buffett_text = f"**Wide Moat**. Consistent high ROC ({roc_str}) suggests competitive advantage."
        elif roc_val > 0.10:
            buffett_text = "**Narrow Moat**. Decent returns, but not exceptional."
        else:
            buffett_text = "**No Moat**. Low capital efficiency ({roc_str})."
            
        # 3. Graham Value Logic
        if pe_val > 0 and pe_val < 15:
            graham_text = f"**Undervalued**. P/E of {pe_str} is below defensive target of 15."
        elif pe_val < 25:
            graham_text = f"**Fair Value**. P/E of {pe_str} is reasonable."
        else:
            graham_text = f"**Expensive**. P/E of {pe_str} implies high growth expectations."

        # Return a perfectly formatted Markdown table that the Frontend can read
        return f"""
| Formula | Assessment |
|---|---|
| **Greenblatt Magic Formula** | {magic_text} |
| **Buffett Moat Indicator** | {buffett_text} |
| **Ben Graham Valuation** | {graham_text} |
| *System Status* | *AI Quota Limit. Showing smart algorithmic analysis.* |
"""       

def generate_canslim_assessment(company_name: str, quote: dict, quarterly_earnings: list, annual_earnings: list, institutional_holders: int):
    """Generates a CANSLIM checklist."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        c_growth, a_growth, is_new_high, is_high_demand = "N/A", "N/A", "No", "No"
        if len(quarterly_earnings) > 4:
            latest_q_eps = quarterly_earnings[0].get('eps', 0)
            previous_q_eps = quarterly_earnings[4].get('eps', 0)
            if previous_q_eps not in [0, None]: c_growth = f"{((latest_q_eps - previous_q_eps) / abs(previous_q_eps)) * 100:.2f}% (YoY)"
        if len(annual_earnings) >= 2:
            latest_y_eps = annual_earnings[0].get('eps', 0)
            previous_y_eps = annual_earnings[1].get('eps', 0)
            if previous_y_eps not in [0, None]: a_growth = f"{((latest_y_eps - previous_y_eps) / abs(previous_y_eps)) * 100:.2f}%"
        price = quote.get('price'); year_high = quote.get('yearHigh')
        if price and year_high:
            percent_from_high = ((price - year_high) / year_high) * 100
            if percent_from_high >= -15: is_new_high = f"Yes, within {abs(percent_from_high):.2f}% of 52-week high"
        volume = quote.get('volume'); avg_volume = quote.get('avgVolume')
        if volume and avg_volume and volume > avg_volume:
            is_high_demand = f"Yes, volume is {((volume - avg_volume) / avg_volume) * 100:.2f}% above average"
        i_sponsorship = f"{institutional_holders} institutions hold this stock."

        prompt = f"""Act as an analyst applying CANSLIM to {company_name}. Based *only* on the data, create a 7-point checklist. Output a 3-column Markdown table: "Criteria", "Assessment", "Result" (Pass/Fail/Neutral). DATA: C={c_growth}, A={a_growth}, N={is_new_high}, S={is_high_demand}, L=Infer leadership, I={i_sponsorship}, M=Infer market direction."""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in generate_canslim_assessment: {e}")
        return "Could not generate CANSLIM assessment."

def generate_fundamental_conclusion(company_name: str, piotroski_data: dict, graham_data: dict, darvas_data: dict, key_stats: dict, news_headlines: list):
    """Performs a meta-analysis summary."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        p_score = piotroski_data.get('score', 'N/A') if piotroski_data else 'N/A'
        g_score = graham_data.get('score', 'N/A') if graham_data else 'N/A'
        d_status = darvas_data.get('status', 'N/A') if darvas_data else 'N/A'
        pe = key_stats.get('peRatio', 'N/A')
        
        news_str = "- " + "\n- ".join(news_headlines[:3]) if news_headlines else "No recent news."

        prompt = f"""Act as a Senior Portfolio Manager. Analyze {company_name}.
        **Hard Numbers:** Piotroski: {p_score}/9, Graham Scan: {g_score}/7, Darvas Status: {d_status}, P/E: {pe}.
        **News Context:** {news_str}
        Synthesize into: GRADE: [A-F], THESIS: [Sentence], TAKEAWAYS: [3 bullets]."""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in fundamental conclusion: {e}")
        return "GRADE: N/A\nTHESIS: Analysis unavailable."

def find_peer_tickers_by_industry(company_name: str, sector: str, industry: str, country: str):
    """Uses Gemini AI to find competitor tickers."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        prompt = f"""Act as an expert financial data analyst. The company is {company_name}, in the "{industry}" industry within the "{sector}" sector in {country}. Identify top 5 publicly traded competitors. Return comma-separated tickers ONLY. US: AAPL, MSFT. India: RELIANCE.NS, TCS.NS."""
        response = model.generate_content(prompt)
        peers_str = response.text.strip().replace(" ", "").upper()
        return peers_str.split(',')
    except Exception as e:
        print(f"Error finding peers: {e}")
        return []


# --- 3. CHART AI (IMAGE) ANALYSIS (OPTIMIZED) ---

def identify_ticker_from_image(image_bytes: bytes):
    """Identifies ticker from chart image, supports Stocks & Indices."""
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        prompt = """
        Analyze this financial chart image. Identify the symbol/ticker.
        
        RULES:
        1. If it's a specific company, return the Yahoo symbol (e.g., "RELIANCE.NS", "AAPL").
        2. If it's an INDEX, map it correctly:
           - Nifty 50 -> "^NSEI"
           - Bank Nifty -> "^NSEBANK"
           - Sensex -> "^BSESN"
           - S&P 500 -> "^GSPC"
           - Nasdaq -> "^IXIC"
           - Bitcoin -> "BTC-USD"
           - Gold -> "GC=F"
        3. If you are not 100% sure, return "NOT_FOUND".
        4. Return ONLY the symbol string. No text.
        """
        
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_bytes}])
        return response.text.strip().upper().replace("`", "")
    except Exception as e:
        print(f"Error identifying ticker: {e}")
        return "NOT_FOUND"


def analyze_chart_technicals_from_image(image_bytes: bytes):
    """
    Uses Gemini Vision to analyze chart images.
    Updated with STRICT PROMPTS to prevent verbose output in the Trade Ticket.
    """
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')
        image_part = {"mime_type": "image/jpeg", "data": image_bytes}
        
        prompt = """
        Act as an expert Chartered Market Technician. Analyze this stock chart image.
        Provide a professional technical analysis and a precision trade setup.

        STRICT RESPONSE FORMAT (Do not deviate):

        TREND: [Uptrend / Downtrend / Sideways]
        PATTERNS: [List key patterns like Head & Shoulders, Flags, or "None"]
        LEVELS: [List key Support and Resistance price levels]
        VOLUME: [Describe volume behavior: "High volume breakout", "Low volume pullback", etc.]
        INDICATORS: [Mention visible indicators like MA, RSI, MACD]
        CONCLUSION: [A professional 2-sentence summary]
        
        -- TRADE TICKET --
        ACTION: [BUY / SELL / WAIT]
        ENTRY_ZONE: [Price range ONLY. e.g., "150.00 - 152.50"]
        STOP_LOSS: [Price ONLY. e.g., "145.00"]
        TARGET_1: [Price ONLY. e.g., "160.00"]
        TARGET_2: [Price ONLY. e.g., "165.00"]
        RISK_REWARD: [Ratio. e.g., "1:3"]
        CONFIDENCE: [High / Medium / Low]
        RATIONALE: [One clear sentence explaining the strategy.]
        """
        
        response = model.generate_content([prompt, image_part])
        return response.text.strip()
        
    except Exception as e:
        print(f"AI Image Analysis Error: {e}")
        return "TREND: Error\nACTION: WAIT\nRATIONALE: Server could not process image."


# --- 4. CHART AI (TIMEFRAME) ANALYSIS (SAFE MATH & STRICT FORMAT) ---

def generate_timeframe_analysis(symbol: str, timeframe: str, technicals: dict, pivots: dict, mas: dict):
    """
    Generates a trade setup based on Mathematical Indicators.
    """
    try:
        configure_gemini_for_request()
        model = genai.GenerativeModel('gemini-3-flash-preview')

        # --- SAFE DATA EXTRACTION ---
        def safe_get(d, keys, default='N/A'):
            """Deep get for nested dictionaries."""
            val = d
            for key in keys:
                if isinstance(val, dict):
                    val = val.get(key)
                else:
                    return default
            return f"{val:.2f}" if isinstance(val, (int, float)) else str(val)

        # Extract values safely
        price = safe_get(technicals, ['price_action', 'current_close'])
        rsi = safe_get(technicals, ['rsi'])
        macd = safe_get(technicals, ['macd'])
        adx = safe_get(technicals, ['adx'])
        
        # Pivots
        pp = safe_get(pivots, ['classic', 'pp'])
        s1 = safe_get(pivots, ['classic', 's1'])
        r1 = safe_get(pivots, ['classic', 'r1'])
        
        # MAs
        ema20 = safe_get(mas, ['20'])
        ema50 = safe_get(mas, ['50'])

        # --- HEURISTIC TREND ---
        trend_hint = "Neutral"
        try:
            p_val = float(price)
            ma_val = float(ema50)
            if p_val > ma_val: trend_hint = "Bullish"
            elif p_val < ma_val: trend_hint = "Bearish"
        except: pass

        # --- PROMPT ---
        prompt = f"""
        Act as an Algorithmic Trader. Analyze {symbol} on {timeframe} timeframe.
        
        **HARD DATA (Computed):**
        - Price: {price}
        - Trend Bias: {trend_hint}
        - Indicators: RSI={rsi}, ADX={adx}, MACD={macd}
        - Key Levels: Pivot={pp}, Support={s1}, Resistance={r1}
        - Averages: EMA20={ema20}, EMA50={ema50}

        **Instructions:**
        Based ONLY on these numbers, provide a trading strategy.
        
        **STRICT RESPONSE FORMAT:**
        TREND: [Uptrend / Downtrend / Range]
        PATTERNS: [Identify structure based on levels]
        MOMENTUM: [Bullish / Bearish / Neutral]
        LEVELS: [Key S/R from data]
        INDICATORS: [Interpret the RSI/MACD values]
        CONCLUSION: [Brief summary]

        -- TRADE TICKET --
        ACTION: [BUY / SELL / WAIT]
        ENTRY_ZONE: [Price Range]
        STOP_LOSS: [Price]
        TARGET_1: [Price]
        TARGET_2: [Price]
        RISK_REWARD: [Ratio]
        CONFIDENCE: [High / Medium / Low]
        RATIONALE: [Explain why based on the math provided]
        """

        response = model.generate_content(prompt)
        text = response.text.strip()
        
        if "ACTION:" not in text:
             return f"TREND: {trend_hint}\nACTION: WAIT\nRATIONALE: Market data unclear ({text[:50]}...)"
            
        return text

    except Exception as e:
        print(f"AI Math Error: {e}")
        # Return a fallback that looks like a valid response so frontend parses it
        return f"TREND: {trend_hint if 'trend_hint' in locals() else 'Neutral'}\nACTION: WAIT\nRATIONALE: AI Analysis interrupted. Please retry."

def analyze_pure_vision(image_bytes: bytes):
    """
    Performs 'Pure Vision' analysis without external data feeds.
    Focuses on Geometry, Price Action Math, and Institutional Psychology.
    """
    try:
        configure_gemini_for_request()
        # Using 1.5 Pro or Flash for better vision reasoning
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        prompt = """
        Act as a Quantitative Technical Analyst with X-Ray Vision. 
        Analyze this chart image strictly based on Price Action, Geometry, and Mathematics.
        DO NOT generic stuff. Give me precision.

        **MATHEMATICAL & GEOMETRIC ANALYSIS:**
        1. **Trend Math:** Identify the slope and strength of the trend (e.g., "45-degree aggressive uptrend" or "Decaying momentum").
        2. **Structure:** Identify Higher Highs/Lows or Lower Highs/Lows logic.
        3. **Candlestick Math:** Analyze the ratio of wicks to bodies in the last 5 candles. Who is winning? Buyers or Sellers?
        4. **Key Zones:** Identify exact price levels for Support/Resistance visible in the image.

        **STRICT OUTPUT FORMAT:**
        
        **VERDICT:** [BULLISH / BEARISH / NEUTRAL]
        
        **MARKET STRUCTURE:**
        [Explain the market phase: Accumulation, Markup, Distribution, or Decline]
        
        **GEOMETRIC SIGNALS:**
        - [Pattern identified]
        - [Trendline angle/slope observation]
        - [Volatility contraction/expansion observation]

        **INSTITUTIONAL FOOTPRINTS:**
        [Where is the Smart Money entering/exiting based on candle size?]

        -- TRADE SETUP (Visual Estimation) --
        **DIRECTION:** [LONG / SHORT]
        **ENTRY:** [Price Level]
        **STOP LOSS:** [Price Level]
        **TARGET:** [Price Level]
        **WIN PROBABILITY:** [High/Medium]
        """
        
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_bytes}])
        return response.text.strip()
    except Exception as e:
        return f"**VERDICT:** ERROR\n**ANALYSIS:** System blinded. Cause: {str(e)}"
```

## File: frontend/src/components/Header/StockHeader.js
```javascript
import React, { useState, useEffect, useRef } from 'react';
import styled, { keyframes, css } from 'styled-components';
import ConnectBroker from './ConnectBroker';

// ==========================================
// 1. HIGH-END ANIMATIONS
// ==========================================

const flashGreen = keyframes`
  0% { color: var(--color-text-primary); text-shadow: none; }
  10% { color: #3FB950; text-shadow: 0 0 15px rgba(63, 185, 80, 0.8); transform: scale(1.05); }
  100% { color: var(--color-text-primary); text-shadow: none; transform: scale(1); }
`;

const flashRed = keyframes`
  0% { color: var(--color-text-primary); text-shadow: none; }
  10% { color: #F85149; text-shadow: 0 0 15px rgba(248, 81, 73, 0.8); transform: scale(1.05); }
  100% { color: var(--color-text-primary); text-shadow: none; transform: scale(1); }
`;

const pulse = keyframes`
  0% { opacity: 1; box-shadow: 0 0 0 0 rgba(63, 185, 80, 0.7); }
  70% { opacity: 1; box-shadow: 0 0 0 6px rgba(63, 185, 80, 0); }
  100% { opacity: 1; box-shadow: 0 0 0 0 rgba(63, 185, 80, 0); }
`;

// ==========================================
// 2. STYLED COMPONENTS (Glassmorphism)
// ==========================================

const HeaderContainer = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background: linear-gradient(145deg, #161B22, #0D1117);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  gap: 1rem;
  width: 100%;
  box-sizing: border-box;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3); 
  backdrop-filter: blur(10px);
  
  @media (min-width: 768px) {
    flex-direction: row;
    align-items: center;
    gap: 0;
  }
`;

const CompanyInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 1.2rem;
  max-width: 100%;
  min-width: 0; 
`;

const CompanyLogo = styled.img`
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background-color: #fff;
  padding: 4px;
  object-fit: contain;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  flex-shrink: 0;
  border: 1px solid rgba(255,255,255,0.1);
  
  @media (min-width: 768px) {
      width: 64px;
      height: 64px;
  }
`;

const TextContainer = styled.div`
  display: flex;
  flex-direction: column;
  min-width: 0; 
`;

const TopRow = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
`;

const CompanyName = styled.h1`
  font-size: 1.4rem;
  font-weight: 800;
  margin: 0;
  line-height: 1.2;
  color: var(--color-text-primary);
  white-space: normal; 
  word-wrap: break-word;
  letter-spacing: -0.5px;

  @media (min-width: 768px) {
    font-size: 2.2rem;
    white-space: nowrap;
  }
`;

const CompanySymbol = styled.span`
  font-size: 0.85rem;
  color: var(--color-text-secondary);
  font-weight: 600;
  background: rgba(255,255,255,0.05);
  padding: 2px 8px;
  border-radius: 6px;
  display: inline-block;
  font-family: 'Roboto Mono', monospace;
  border: 1px solid rgba(255,255,255,0.05);
  
  @media (min-width: 768px) {
      font-size: 1rem;
  }
`;

const PriceInfo = styled.div`
  text-align: left;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  
  @media (min-width: 768px) {
    text-align: right;
    align-items: flex-end;
  }
`;

const CurrentPrice = styled.div`
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 0.25rem;
  font-family: 'Roboto Mono', monospace;
  color: var(--color-text-primary);
  
  ${({ flash }) => flash === 'up' && css`animation: ${flashGreen} 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;`}
  ${({ flash }) => flash === 'down' && css`animation: ${flashRed} 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94) both;`}

  @media (min-width: 768px) {
      font-size: 2.8rem;
  }
`;

const PriceChange = styled.div`
  font-size: 1.1rem;
  font-weight: 600;
  color: ${({ isPositive }) => (isPositive ? '#3FB950' : '#F85149')};
  display: flex;
  align-items: center;
  gap: 8px;
  background: ${({ isPositive }) => (isPositive ? 'rgba(63, 185, 80, 0.1)' : 'rgba(248, 81, 73, 0.1)')};
  padding: 4px 12px;
  border-radius: 20px;
  border: 1px solid ${({ isPositive }) => (isPositive ? 'rgba(63, 185, 80, 0.2)' : 'rgba(248, 81, 73, 0.2)')};
  
  @media (min-width: 768px) {
      font-size: 1.2rem;
  }
`;

const LiveDot = styled.div`
  width: 8px;
  height: 8px;
  background-color: #3FB950;
  border-radius: 50%;
  animation: ${pulse} 2s infinite;
`;

const ConnectionStatus = styled.div`
    font-size: 0.65rem;
    color: var(--color-text-secondary);
    margin-top: 5px;
    display: flex;
    align-items: center;
    gap: 4px;
    opacity: 0.7;
`;

// ==========================================
// 3. INTELLIGENT HELPER FUNCTIONS
// ==========================================

const getCurrencySymbol = (currencyCode, symbol) => {
    // 1. Priority: Explicit Symbol Check for India
    if (symbol) {
        const s = symbol.toUpperCase();
        if (s.includes('.NS') || s.includes('.BO') || s.includes('NIFTY') || s.includes('SENSEX') || s.includes('BANKNIFTY')) {
            return '₹';
        }
    }
    
    // 2. Fallback: Currency Code
    switch (currencyCode) {
        case 'INR': return '₹';
        case 'USD': return '$';
        case 'JPY': return '¥';
        case 'EUR': return '€';
        case 'GBP': return '£';
        default: return '$';
    }
};

// ==========================================
// 4. MAIN COMPONENT LOGIC
// ==========================================

const StockHeader = ({ profile, quote: initialQuote }) => {
  // State for Real-Time Data
  const [liveData, setLiveData] = useState({
    price: 0,
    change: 0,
    pct: 0
  });
  
  const [flash, setFlash] = useState(null); // 'up', 'down', or null
  const [isConnected, setIsConnected] = useState(false);
  const prevPriceRef = useRef(0);
  const wsRef = useRef(null);

  // --- SAFE INITIALIZATION ---
  useEffect(() => {
    if (initialQuote) {
        setLiveData({ 
            price: Number(initialQuote.price) || 0, 
            change: Number(initialQuote.change) || 0, 
            pct: Number(initialQuote.changesPercentage) || 0 
        });
        prevPriceRef.current = Number(initialQuote.price) || 0;
    }
  }, [initialQuote]);
  
  // --- REAL WEBSOCKET ENGINE WITH HEARTBEAT ---
  useEffect(() => {
    // Crash Guard: Don't run if symbol is missing
    const symbol = profile?.symbol;
    if (!symbol) return;

    // 1. Construct WebSocket URL Dynamically (Local vs Production)
    const apiUrl = process.env.REACT_APP_API_URL;
    let wsUrl = "";
    
    if (apiUrl) {
         // Production (Vercel -> Railway)
         const host = apiUrl.replace(/^https?:\/\//, '');
         const proto = apiUrl.includes('https') ? 'wss://' : 'ws://';
         wsUrl = `${proto}${host}/ws/live/${symbol}`;
    } else {
         // Default Localhost
         const isLocal = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
         const wsHost = isLocal ? '127.0.0.1:8000' : window.location.host;
         const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
         wsUrl = `${protocol}//${wsHost}/ws/live/${symbol}`;
    }

    let pingInterval = null;

    const connect = () => {
        try {
            // Close existing connection if any
            if (wsRef.current) wsRef.current.close();
            
            const ws = new WebSocket(wsUrl);
            wsRef.current = ws;

            ws.onopen = () => {
                setIsConnected(true);
                // --- HEARTBEAT ENGINE ---
                // Send "ping" every 10s to keep connection alive on Railway
                pingInterval = setInterval(() => {
                    if (ws.readyState === WebSocket.OPEN) {
                        ws.send("ping");
                    }
                }, 10000); 
            };

            ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    const newPrice = Number(data.price); // Force Number
                    
                    if (newPrice && newPrice !== prevPriceRef.current) {
                        // Flash Logic
                        if (newPrice > prevPriceRef.current) setFlash('up');
                        else if (newPrice < prevPriceRef.current) setFlash('down');
                        
                        setTimeout(() => setFlash(null), 800);

                        setLiveData({
                            price: newPrice,
                            change: Number(data.change) || 0,
                            pct: Number(data.percent_change) || 0
                        });
                        prevPriceRef.current = newPrice;
                    }
                } catch (e) {
                    // Ignore parsing errors
                }
            };

            ws.onclose = () => {
                setIsConnected(false);
                if (pingInterval) clearInterval(pingInterval);
                // Auto Reconnect if connection drops
                setTimeout(connect, 3000);
            };
        } catch(e) {
            console.error("WS Connect Error", e);
        }
    };

    connect();

    // Cleanup on unmount
    return () => {
        if (pingInterval) clearInterval(pingInterval);
        if (wsRef.current) wsRef.current.close();
    };
  }, [profile?.symbol]);

  // --- RENDER SAFEGUARDS ---
  if (!profile) return null; // Don't render until data exists
  
  const symbol = profile.symbol || "";
  const currencySymbol = getCurrencySymbol(profile.currency, symbol);
  
  // Safe Formatting (Prevents .toFixed crash)
  const safePrice = Number(liveData.price) || 0;
  const safeChange = Number(liveData.change) || 0;
  const safePct = Number(liveData.pct) || 0;

  const isPositive = safeChange >= 0;
  const formattedPrice = safePrice.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  const formattedChange = safeChange.toFixed(2);
  const formattedPct = safePct.toFixed(2);

  // Check if Indian stock (to show button)
  const isIndian = symbol.includes('.NS') || symbol.includes('.BO') || symbol.includes('NIFTY') || symbol.includes('SENSEX');

  return (
    <HeaderContainer>
      <CompanyInfo>
        {profile.image ? (
            <CompanyLogo 
                src={profile.image} 
                alt={`${profile.companyName} logo`} 
                onError={(e) => e.target.style.display='none'} 
            />
        ) : null}
        <TextContainer>
          <TopRow>
            <CompanyName>
                {profile.companyName}
            </CompanyName>
            {/* --- CONNECT BROKER BUTTON --- */}
            {isIndian && <ConnectBroker />} 
          </TopRow>
          
          <div style={{display:'flex', alignItems:'center', gap:'10px'}}>
             <CompanySymbol>{symbol}</CompanySymbol>
             {isConnected && (
                  <ConnectionStatus>
                      <LiveDot style={{width:'6px', height:'6px'}}/> Live
                  </ConnectionStatus>
             )}
          </div>
        </TextContainer>
      </CompanyInfo>
      
      <PriceInfo>
        <CurrentPrice flash={flash}>
          {currencySymbol}{formattedPrice}
        </CurrentPrice>
        <PriceChange isPositive={isPositive}>
            {isPositive ? '▲' : '▼'}
            {formattedChange} ({isPositive ? '+' : ''}{formattedPct}%)
        </PriceChange>
      </PriceInfo>
    </HeaderContainer>
  );
};

export default StockHeader;
```

## File: frontend/src/pages/StockDetailPage.js
```javascript
import React, { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import styled, { keyframes } from 'styled-components';
import axios from 'axios';

// --- COMPONENTS ---
import StockHeader from '../components/Header/StockHeader';
import { Tabs, TabPanel } from '../components/common/Tabs/Tabs';
import CustomChart from '../components/Chart/CustomChart';
import SwotAnalysis from '../components/SWOT/SwotAnalysis';
import OverallSentiment from '../components/Sentiment/OverallSentiment';
import PriceLevels from '../components/Overview/PriceLevels';
import NewsList from '../components/News/NewsList';
import ChartAnalysis from '../components/StockDetailPage/ChartAnalysis';
import Fundamentals from '../components/Fundamentals/Fundamentals';
import Financials from '../components/Financials/Financials';
import Forecasts from '../components/Forecasts/Forecasts';
import PeersComparison from '../components/Peers/PeersComparison';
import Shareholding from '../components/Shareholding/Shareholding';
import Technicals from '../components/Technicals/Technicals';
import { FaArrowLeft } from 'react-icons/fa';

// --- CONFIGURATION ---
// This connects your Vercel Frontend to your Railway Backend
const API_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

// --- ANIMATIONS ---
const fadeIn = keyframes`
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
`;

// --- STYLED COMPONENTS ---
const PageContainer = styled.div`
  padding: 2rem 3rem;
  max-width: 1800px;
  margin: 0 auto;
  animation: ${fadeIn} 0.4s ease-out;
  
  @media (max-width: 768px) {
    padding: 1rem;
  }
`;

const TabGrid = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr; /* Chart takes 66%, Info takes 33% */
  gap: 2rem;

  @media (max-width: 1200px) {
    grid-template-columns: 1fr; /* Stack on mobile */
  }
`;

const LeftCol = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const RightCol = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const LoadingBox = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 80vh;
  color: var(--color-primary);
  font-size: 1.2rem;
  font-weight: 500;
  gap: 1rem;
`;

const ErrorBox = styled(LoadingBox)`
  color: var(--color-danger);
`;

const BackBtn = styled.button`
  background: none;
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 0.9rem;
  margin-bottom: 2rem;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;

  &:hover {
    background-color: var(--color-secondary);
    color: var(--color-text-primary);
    border-color: var(--color-primary);
  }
`;

const StockDetailPage = () => {
  const { symbol } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  
  // Data passed from "Deep Scan" or "Chart Analysis" upload
  const chartAnalysisData = location.state?.chartAnalysis;
  const chartTechnicalData = location.state?.technicalData;

  // --- STATE ---
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // AI Analysis States
  const [swot, setSwot] = useState('');
  const [loadingSwot, setLoadingSwot] = useState(true);
  const [philosophy, setPhilosophy] = useState('');
  const [canslim, setCanslim] = useState('');
  const [conclusion, setConclusion] = useState('');
  const [loadingFundAI, setLoadingFundAI] = useState(true);

  // --- ASSET DETECTION ---
  const isCrypto = symbol.includes('.CC') || symbol.includes('BTC') || symbol.includes('ETH') || (symbol.includes('USD') && !symbol.includes('.'));
  const isIndex = symbol.includes('.INDX') || symbol.includes('^');
  const isCommodity = symbol.includes('GOLD') || symbol.includes('OIL') || symbol.includes('XAU') || symbol.includes('USO') || symbol.includes('CLUSD');
  
  // Logic: Stocks have financials. Crypto/Indices/Commodities do not.
  const isStock = !isCrypto && !isIndex && !isCommodity;

  // --- 1. MASTER DATA FETCH ---
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      // Reset AI states on symbol change
      setSwot(''); setPhilosophy(''); setCanslim(''); setConclusion('');
      
      try {
        // Use the Vercel-Compatible API_URL
        const res = await axios.get(`${API_URL}/api/stocks/${symbol}/all`);
        
        if (!res.data || !res.data.profile) {
            throw new Error("Incomplete Data");
        }
        setData(res.data);
      } catch (err) {
        console.error("Fetch Error:", err);
        setError("Unable to retrieve market data. Please try again.");
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [symbol]);

  // --- 2. AI HANDLERS (LAZY LOADING) ---
  
  // SWOT Analysis (Runs for everything)
  const fetchSwot = useCallback(() => {
      if (!data?.profile?.companyName) { 
          setLoadingSwot(false); 
          return; 
      }
      setLoadingSwot(true);
      
      const payload = { 
          companyName: data.profile.companyName, 
          description: data.profile.description || "Financial Asset"
      };
      
      axios.post(`${API_URL}/api/stocks/${symbol}/swot`, payload)
        .then(res => setSwot(res.data.swot_analysis))
        .catch(() => setSwot("Analysis currently unavailable."))
        .finally(() => setLoadingSwot(false));
  }, [data, symbol]);

  // Fundamental Analysis (Runs ONLY for Stocks)
  useEffect(() => {
    if (!data) return;

    // Trigger SWOT
    fetchSwot();

    if (isStock) {
        setLoadingFundAI(true);
        
        // Parallel Execution for Speed
        const req1 = axios.post(`${API_URL}/api/stocks/${symbol}/fundamental-analysis`, { 
            companyName: data.profile.companyName, 
            keyMetrics: data.key_metrics 
        }).then(r => setPhilosophy(r.data.assessment)).catch(() => setPhilosophy("N/A"));

        const req2 = axios.post(`${API_URL}/api/stocks/${symbol}/canslim-analysis`, {
            companyName: data.profile.companyName, 
            quote: data.quote, 
            quarterlyEarnings: data.quarterly_income_statements,
            annualEarnings: data.annual_revenue_and_profit, 
            institutionalHolders: data.shareholding ? data.shareholding.length : 0
        }).then(r => setCanslim(r.data.assessment)).catch(() => setCanslim("N/A"));

        const req3 = axios.post(`${API_URL}/api/stocks/${symbol}/conclusion-analysis`, {
            companyName: data.profile.companyName, 
            piotroskiData: data.piotroski_f_score,
            grahamData: data.graham_scan, 
            darvasData: data.darvas_scan,
            canslimAssessment: "Generated", 
            philosophyAssessment: "Generated",
            keyStats: data.keyStats,
            newsHeadlines: data.news ? data.news.slice(0, 5).map(n => n.title) : []
        }).then(r => setConclusion(r.data.conclusion)).catch(() => setConclusion("N/A"));

        Promise.allSettled([req1, req2, req3]).finally(() => setLoadingFundAI(false));
    } else {
        setLoadingFundAI(false); // Skip for non-stocks
    }
  }, [data, symbol, isStock, fetchSwot]);

  // --- RENDER STATES ---
  if (loading) return (
      <LoadingBox>
          <div className="spinner" />
          <p>Accessing Global Data Feeds...</p>
      </LoadingBox>
  );

  if (error || !data) return (
      <ErrorBox>
          <h2>Connection Interrupted</h2>
          <p>{error}</p>
          <BackBtn onClick={() => navigate('/')}><FaArrowLeft /> Return Home</BackBtn>
      </ErrorBox>
  );

  // --- MAIN RENDER ---
  return (
    <PageContainer>
      <BackBtn onClick={() => navigate('/')}><FaArrowLeft /> Back to Command Center</BackBtn>
      
      {/* 1. Header (Live Price & Broker Connect Button) */}
      <StockHeader profile={data.profile} quote={data.quote} />
      
      <Tabs>
        
        {/* Tab: Chart AI (Only if uploaded) */}
        {chartAnalysisData && (
          <TabPanel label="Chart Insight">
            <ChartAnalysis analysisData={chartAnalysisData} technicalData={chartTechnicalData} />
          </TabPanel>
        )}

        {/* Tab: Overview (The Main Dashboard) */}
        <TabPanel label="Overview">
          <TabGrid>
            <LeftCol>
              <CustomChart symbol={symbol} />
              <SwotAnalysis analysisText={swot} isLoading={loadingSwot} onRegenerate={fetchSwot} />
            </LeftCol>
            <RightCol>
              {isStock && <OverallSentiment sentimentData={data.overall_sentiment} />}
              <PriceLevels pivotPoints={data.pivot_points} quote={data.quote} profile={data.profile} />
              <NewsList newsArticles={data.news} />
            </RightCol>
          </TabGrid>
        </TabPanel>
        
        {/* Tab: Fundamentals (Stocks Only) */}
        {isStock && (
            <TabPanel label="Fundamentals">
                <Fundamentals
                    symbol={symbol} profile={data.profile} quote={data.quote} keyMetrics={data.key_metrics}
                    piotroskiData={data.piotroski_f_score} darvasScanData={data.darvas_scan}
                    grahamScanData={data.graham_scan} quarterlyEarnings={data.quarterly_income_statements}
                    annualEarnings={data.annual_revenue_and_profit} shareholding={data.shareholding}
                    delay={0} 
                    philosophyAssessment={philosophy} canslimAssessment={canslim} conclusion={conclusion}
                    isLoadingPhilosophy={loadingFundAI} isLoadingCanslim={loadingFundAI} isLoadingConclusion={loadingFundAI}
                />
            </TabPanel>
        )}

        {/* Tab: Financials (Stocks Only) */}
        {isStock && (
          <TabPanel label="Financials">
            <Financials 
              profile={data.profile} keyStats={data.keyStats}
              financialData={data.annual_revenue_and_profit} balanceSheetData={data.annual_balance_sheets}
              annualCashFlow={data.annual_cash_flow_statements} quarterlyIncome={data.quarterly_income_statements}
              quarterlyBalance={data.quarterly_balance_sheets} quarterlyCashFlow={data.quarterly_cash_flow_statements}
            />
          </TabPanel>
        )}
        
        {/* Tab: Forecasts (Universal) */}
        <TabPanel label="Forecasts">
            <Forecasts 
                symbol={symbol} quote={data.quote} analystRatings={data.analyst_ratings}
                priceTarget={data.price_target_consensus} keyStats={data.keyStats}
                news={data.news} delay={0} currency={data.profile?.currency}
            />
        </TabPanel>

        {/* Tab: Peers (Stocks Only) */}
        {isStock && (
            <TabPanel label="Peers">
                <PeersComparison symbol={symbol} />
            </TabPanel>
        )}
        
        {/* Tab: Shareholding (Stocks Only) */}
        {isStock && (
            <TabPanel label="Shareholding">
                <Shareholding 
                    shareholdingData={data.shareholding}
                    historicalStatements={data.annual_revenue_and_profit}
                    shareholdingBreakdown={data.shareholding_breakdown}
                />
            </TabPanel>
        )}
        
        {/* Tab: Technicals (Universal) */}
        <TabPanel label="Technicals">
            <Technicals 
              analystRatings={data.analyst_ratings} technicalIndicators={data.technical_indicators}
              movingAverages={data.moving_averages} pivotPoints={data.pivot_points}
              quote={data.quote}
            />
        </TabPanel>

      </Tabs>
    </PageContainer>
  );
};

export default StockDetailPage;
```

## File: backend/app/main.py
```python
from . import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os
from .routers import stocks, indices, charts, stream, auth # <--- Add auth

# Import Routers
from .routers import stocks, indices, charts, stream 

# Create App
app = FastAPI(
    title="Stellar Stock Screener API",
    description="High-performance backend for stock analysis.",
    version="2.0.0"
)

# ==========================================
# 1. SECURITY & CONFIGURATION
# ==========================================

# CORS is vital for stability, even in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for maximum compatibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# 2. API ROUTERS (Priority 1)
# ==========================================

app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(indices.router, prefix="/api/indices", tags=["indices"])
app.include_router(charts.router, prefix="/api/charts", tags=["charts"])
app.include_router(stream.router, prefix="/ws", tags=["stream"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

# ==========================================
# 3. HEALTH CHECK (Critical for Railway)
# ==========================================

@app.get("/health")
async def health_check():
    """Railway uses this to check if the app is alive."""
    return {"status": "healthy", "mode": "production"}

# ==========================================
# 4. STATIC FILE SERVING (Smart Engine)
# ==========================================

# A. Define the path to the React Build folder
# In Docker, this is usually at /app/frontend/build
BUILD_DIR = "frontend/build"

# B. Mount the 'static' folder (JS/CSS)
# This handles requests like /static/js/main.js
if os.path.exists(os.path.join(BUILD_DIR, "static")):
    app.mount("/static", StaticFiles(directory=os.path.join(BUILD_DIR, "static")), name="static_assets")

# C. The "Smart Catch-All" Route
# This handles:
# 1. Root files (manifest.json, favicon.ico, logo192.png) -> Serves the FILE
# 2. App Routes (/stock/AAPL, /index/NSE) -> Serves index.html (React App)
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    
    # 1. Safety: Don't trap API calls
    if full_path.startswith("api/"):
        return JSONResponse({"error": "API endpoint not found"}, status_code=404)

    # 2. Check if a specific file exists in the build folder (e.g. manifest.json)
    # This fixes the PWA/Icon bug
    file_path = os.path.join(BUILD_DIR, full_path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)

    # 3. Default: Serve index.html for React Router to handle
    index_path = os.path.join(BUILD_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
        
    return JSONResponse({"error": "Frontend build not found. Please check Dockerfile."}, status_code=500)
```

## File: backend/app/routers/stocks.py
```python
import asyncio
import math
import pandas as pd
import json
from urllib.parse import unquote
from fastapi import APIRouter, HTTPException, Query, Body
# ROBUST SERVICE IMPORTS
from ..services import (
    fmp_service, 
    eodhd_service, 
    news_service, 
    gemini_service, 
    fundamental_service, 
    technical_service, 
    sentiment_service, 
    redis_service
)
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter()

# ==========================================
# 1. STRICT DATA MODELS
# ==========================================

class SwotRequest(BaseModel):
    companyName: str
    description: str

class ForecastRequest(BaseModel):
    companyName: str
    analystRatings: List[Dict[str, Any]]
    priceTarget: Dict[str, Any]
    keyStats: Dict[str, Any]
    newsHeadlines: List[str]
    currency: str = "USD"

class FundamentalRequest(BaseModel):
    companyName: str
    keyMetrics: Dict[str, Any]

class CanslimRequest(BaseModel):
    companyName: str
    quote: Dict[str, Any]
    quarterlyEarnings: List[Dict[str, Any]]
    annualEarnings: List[Dict[str, Any]]
    institutionalHolders: int

class ConclusionRequest(BaseModel):
    companyName: str
    piotroskiData: Dict[str, Any]
    grahamData: Dict[str, Any]
    darvasData: Dict[str, Any]
    canslimAssessment: str
    philosophyAssessment: str
    keyStats: Dict[str, Any]
    newsHeadlines: List[str]

class TimeframeRequest(BaseModel):
    timeframe: str

# TradingView Symbol Mapping
TRADINGVIEW_OVERRIDE_MAP = {
    "TATAPOWER.NS": "NSE:TATAPOWER",
    "RELIANCE.NS": "NSE:RELIANCE",
    "BAJFINANCE.NS": "NSE:BAJFINANCE",
    "HDFCBANK.NS": "NSE:HDFCBANK",
    "SBIN.NS": "NSE:SBIN",
    "INFY.NS": "NSE:INFY",
    "TCS.NS": "NSE:TCS",
    "BTC-USD": "BINANCE:BTCUSD",
    "ETH-USD": "BINANCE:ETHUSD",
    "XAU-USD.CC": "OANDA:XAUUSD",
    "USO.US": "TVC:USOIL"
}

# ==========================================
# 2. INTELLIGENT ASSET RECOGNITION
# ==========================================

def identify_asset_class(symbol: str):
    """
    Maps ANY ticker format (Yahoo, TradingView, Colloquial) to our Internal Data Sources.
    Returns: (Source_System, Clean_Ticker)
    """
    s = unquote(symbol).upper().strip()
    
    # --- A. COMMODITIES (Yahoo/TV -> FMP) ---
    if s in ["CL=F", "CL%3DF", "USOIL", "WTI", "CRUDE", "CRUDEOIL", "OIL", "CLUSD"]: return "FMP", "CLUSD"
    if s in ["BZ=F", "BRENT", "UKOIL", "BRENTOIL"]: return "FMP", "UKOIL"
    if s in ["GC=F", "GOLD", "XAU", "XAUUSD"]: return "FMP", "XAUUSD"
    if s in ["SI=F", "SILVER", "XAG", "XAGUSD"]: return "FMP", "XAGUSD"
    if s in ["NG=F", "GAS", "NATGAS", "NGUSD", "UNG", "UNG.US"]: return "FMP", "NGUSD"
    if s in ["HG=F", "COPPER", "HGUSD"]: return "FMP", "HGUSD"
    if s in ["PL=F", "PLATINUM", "PLUSD"]: return "FMP", "PLUSD"

    # --- B. CRYPTO (Coinbase/Yahoo -> FMP) ---
    if ".CC" in s or s in ["BTC", "ETH", "SOL", "XRP", "DOGE", "ADA", "MATIC", "DOT", "LTC"]:
        clean = s.replace("-USD.CC", "USD").replace(".CC", "")
        if not clean.endswith("USD"): clean += "USD"
        return "FMP", clean

    # --- C. STOCKS / INDICES (Default -> EODHD) ---
    return "EODHD", s

# ==========================================
# 3. AI & SEARCH ENDPOINTS
# ==========================================

@router.get("/autocomplete")
async def get_stock_autocomplete(query: str = Query(..., min_length=1)):
    """High-Speed Autocomplete Engine."""
    cache_key = f"autocomplete_v3_{query.lower().strip()}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached

    results = await asyncio.to_thread(fmp_service.search_ticker, query, limit=25)
    if not results: return []

    nse_stocks, bse_stocks, us_stocks, others = [], [], [], []
    for stock in results:
        sym = stock.get('symbol', '').upper()
        exch = stock.get('exchangeShortName', '').upper()
        
        is_nse = sym.endswith('.NS') or exch == 'NSE'
        is_bse = sym.endswith('.BO') or exch == 'BSE'
        is_us = not (is_nse or is_bse) and ('.' not in sym) 

        if is_nse: nse_stocks.append(stock)
        elif is_bse: bse_stocks.append(stock)
        elif is_us: us_stocks.append(stock)
        else: others.append(stock)

    final_list = (nse_stocks + bse_stocks + us_stocks + others)[:10]
    await redis_service.redis_client.set_cache(cache_key, final_list, 86400)
    return final_list

@router.get("/search")
async def search_stock_ticker(query: str = Query(..., min_length=2)):
    cache_key = f"search_v4_{query.lower().strip()}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached
    
    source, ticker = identify_asset_class(query)
    if source == "FMP" and ticker in ["XAUUSD", "XAGUSD", "CLUSD", "NGUSD", "UKOIL"]:
        return {"symbol": ticker} 

    results = fmp_service.search_ticker(query)
    if results: 
        res = {"symbol": results[0]['symbol']}
        await redis_service.redis_client.set_cache(cache_key, res, 86400) 
        return res

    ticker = gemini_service.get_ticker_from_query(query)
    if ticker not in ["NOT_FOUND", "ERROR"]:
        res = {"symbol": ticker}
        await redis_service.redis_client.set_cache(cache_key, res, 86400)
        return res
    raise HTTPException(status_code=404, detail="Ticker not found")

# --- AI ANALYSIS WRAPPERS ---

@router.post("/{symbol}/swot")
async def get_swot_analysis(symbol: str, request_data: SwotRequest = Body(...)):
    cache_key = f"swot_v2_{symbol}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached
    news_articles = await asyncio.to_thread(news_service.get_company_news, request_data.companyName)
    news_headlines = [a.get('title', '') for a in news_articles[:10]]
    swot_analysis = await asyncio.to_thread(gemini_service.generate_swot_analysis, request_data.companyName, request_data.description, news_headlines)
    res = {"swot_analysis": swot_analysis}
    await redis_service.redis_client.set_cache(cache_key, res, 3600)
    return res

@router.post("/{symbol}/forecast-analysis")
async def get_forecast_analysis(symbol: str, d: ForecastRequest = Body(...)):
    cache_key = f"fc_v2_{symbol}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached
    analysis = await asyncio.to_thread(gemini_service.generate_forecast_analysis, d.companyName, d.analystRatings, d.priceTarget, d.keyStats, d.newsHeadlines, d.currency)
    res = {"analysis": analysis}; await redis_service.redis_client.set_cache(cache_key, res, 3600); return res

@router.post("/{symbol}/fundamental-analysis")
async def get_fundamental_analysis(symbol: str, d: FundamentalRequest = Body(...)):
    cache_key = f"fa_v2_{symbol}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached
    analysis = await asyncio.to_thread(gemini_service.generate_investment_philosophy_assessment, d.companyName, d.keyMetrics)
    res = {"assessment": analysis}; await redis_service.redis_client.set_cache(cache_key, res, 86400); return res

@router.post("/{symbol}/canslim-analysis")
async def get_canslim_analysis(symbol: str, d: CanslimRequest = Body(...)):
    cache_key = f"can_v2_{symbol}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached
    analysis = await asyncio.to_thread(gemini_service.generate_canslim_assessment, d.companyName, d.quote, d.quarterlyEarnings, d.annualEarnings, d.institutionalHolders)
    res = {"assessment": analysis}; await redis_service.redis_client.set_cache(cache_key, res, 3600); return res

@router.post("/{symbol}/conclusion-analysis")
async def get_conclusion_analysis(symbol: str, d: ConclusionRequest = Body(...)):
    cache_key = f"conc_v2_{symbol}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached
    conclusion = await asyncio.to_thread(gemini_service.generate_fundamental_conclusion, d.companyName, d.piotroskiData, d.grahamData, d.darvasData, {k: v for k, v in d.keyStats.items() if v is not None}, d.newsHeadlines)
    res = {"conclusion": conclusion}; await redis_service.redis_client.set_cache(cache_key, res, 3600); return res

# ==========================================
# 4. TECHNICAL ANALYSIS & CHART ENGINE
# ==========================================

@router.post("/{symbol}/timeframe-analysis")
async def get_timeframe_analysis(symbol: str, request_data: TimeframeRequest = Body(...)):
    """
    AI Chart Analysis with Mathematical Resampling.
    Fetches 5M data ONCE, then computes 15M/1H/4H locally for the AI.
    """
    source, ticker = identify_asset_class(symbol)
    
    # 1. Determine "Master" Timeframe
    # If user wants Intraday (15M, 1H, 4H), we fetch 5M Base Data
    is_intraday_request = request_data.timeframe.upper() in ["5M", "15M", "30M", "1H", "4H"]
    lookup_range = "5M" if is_intraday_request else request_data.timeframe

    # 2. Check Cache for the MASTER Data (e.g., 5M)
    # Note: Cache key matches get_stock_chart so they share the data pool
    cache_key = f"chart_base_v16_{symbol}_{lookup_range}" 
    chart_list = await redis_service.redis_client.get_cache(cache_key)
    
    # 3. If Cache Miss, Fetch from API
    if not chart_list:
        if source == "FMP":
            chart_list = await asyncio.to_thread(fmp_service.get_commodity_history, ticker, range_type=lookup_range)
            if not chart_list: chart_list = await asyncio.to_thread(fmp_service.get_crypto_history, ticker, range_type=lookup_range)
        else:
            chart_list = await asyncio.to_thread(eodhd_service.get_historical_data, ticker, range_type=lookup_range)
        
        # Save Master Data
        if chart_list:
            await redis_service.redis_client.set_cache(cache_key, chart_list, 300)

    if not chart_list: return {"analysis": f"Market data unavailable for {request_data.timeframe}."}
    
    # 4. MATHEMATICAL RESAMPLING (The Optimization)
    # If we have 5M data but the AI needs 1H, we compute it here.
    if is_intraday_request and request_data.timeframe.upper() != "5M":
         chart_list = technical_service.resample_chart_data(chart_list, request_data.timeframe)

    # 5. Calculate Indicators on the RESAMPLED data
    df = pd.DataFrame(chart_list)
    technicals = technical_service.calculate_technical_indicators(df)
    pivots = technical_service.calculate_pivot_points(df)
    mas = technical_service.calculate_moving_averages(df)
    
    # 6. AI Insight
    analysis = await asyncio.to_thread(gemini_service.generate_timeframe_analysis, symbol, request_data.timeframe, technicals, pivots, mas)
    
    return {"analysis": analysis}


@router.post("/{symbol}/technicals-data")
async def get_technicals_data(symbol: str, request_data: TimeframeRequest = Body(...)):
    """
    Returns Raw Technical Data using Math Resampling.
    Used for the Gauge and Table UI.
    """
    source, ticker = identify_asset_class(symbol)
    
    is_intraday_request = request_data.timeframe.upper() in ["5M", "15M", "30M", "1H", "4H"]
    lookup_range = "5M" if is_intraday_request else request_data.timeframe
    
    # Check Cache for Master Data
    cache_key = f"chart_base_v16_{symbol}_{lookup_range}"
    chart_list = await redis_service.redis_client.get_cache(cache_key)

    if not chart_list:
        if source == "FMP":
            chart_list = await asyncio.to_thread(fmp_service.get_commodity_history, ticker, range_type=lookup_range)
            if not chart_list: chart_list = await asyncio.to_thread(fmp_service.get_crypto_history, ticker, request_data.timeframe)
        else:
            chart_list = await asyncio.to_thread(eodhd_service.get_historical_data, ticker, range_type=lookup_range)
        
        if chart_list:
             await redis_service.redis_client.set_cache(cache_key, chart_list, 300)

    if not chart_list: return {"error": "No data available"}
    
    # Math Resampling
    if is_intraday_request and request_data.timeframe.upper() != "5M":
         chart_list = technical_service.resample_chart_data(chart_list, request_data.timeframe)

    df = pd.DataFrame(chart_list)
    return {
        "technicalIndicators": technical_service.calculate_technical_indicators(df),
        "pivotPoints": technical_service.calculate_pivot_points(df),
        "movingAverages": technical_service.calculate_moving_averages(df)
    }

# ==========================================
# 4. MASTER DATA ENDPOINTS (ROBUST PEERS)
# ==========================================

@router.get("/{symbol}/peers")
async def get_peers_comparison(symbol: str):
    """
    High-Performance Peers Engine.
    1. Gets Peer List.
    2. Normalizes Tickers (Adds .NS/.BO).
    3. Uses FMP Bulk Quote for instant data.
    """
    cache_key = f"peers_v9_{symbol}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached
    
    # 1. Identify Asset Class to handle Suffixes
    source, ticker = identify_asset_class(symbol)
    
    # Skip peers for commodities/crypto as data is often sparse
    if source == "FMP" and "USD" in ticker: return []

    # 2. Get Peer List
    # Try FMP first
    peers = await asyncio.to_thread(fmp_service.get_stock_peers, ticker)
    
    # Fallback to AI if FMP returns empty
    if not peers:
        base_profile = await asyncio.to_thread(eodhd_service.get_company_fundamentals, ticker)
        general = base_profile.get('General', {})
        name = general.get('Name', ticker)
        sector = general.get('Sector', '')
        industry = general.get('Industry', '')
        country = "India" if ".NS" in ticker or ".BO" in ticker else "US"
        
        peers_str = await asyncio.to_thread(gemini_service.find_peer_tickers_by_industry, name, sector, industry, country)
        if peers_str:
            peers = [p.strip() for p in peers_str.split(',')]

    if not peers: return []

    # 3. NORMALIZE TICKERS (The Fix)
    # If we are looking at an Indian stock, ensure all peers have .NS
    clean_peers = []
    suffix = ""
    if ".NS" in symbol: suffix = ".NS"
    elif ".BO" in symbol: suffix = ".BO"
    
    # Add Main Symbol to the list for comparison
    all_symbols = [ticker]
    
    for p in peers:
        p_clean = p.strip().upper()
        # If main symbol has suffix but peer doesn't, append it
        if suffix and not p_clean.endswith(suffix) and "." not in p_clean:
            p_clean += suffix
        all_symbols.append(p_clean)

    # Limit to top 6 to save bandwidth
    target_symbols = list(set(all_symbols))[:6]

    # 4. BULK FETCH (Using Quote Endpoint - Most Reliable)
    # We use get_crypto_real_time_bulk because it is a generic quote fetcher in our FMP service
    # It works for stocks too!
    raw_data = await asyncio.to_thread(fmp_service.get_crypto_real_time_bulk, target_symbols)
    
    if not raw_data:
        return []

    # 5. Format Data
    final_data = []
    for item in raw_data:
        # FMP Quote returns 'price', 'pe', 'marketCap'
        # We map it to what the Frontend expects
        final_data.append({
            "symbol": item.get('symbol'),
            "marketCap": item.get('marketCap'), # Frontend expects raw number
            "peRatioTTM": item.get('pe'),       # Quote endpoint uses 'pe'
            "revenueGrowth": item.get('changesPercentage'), # Proxy for growth in this view
            "grossMargins": 0 # Not available in simple quote, set 0 to avoid N/A crash
        })

    # Cache result
    await redis_service.redis_client.set_cache(cache_key, final_data, 86400)
    return final_data
    
@router.get("/{symbol}/chart")
async def get_stock_chart(symbol: str, range: str = "1D"):
    source, fmp_ticker = identify_asset_class(symbol)
    
    # Timeframe logic
    is_intraday_derived = range in ["5M", "15M", "30M", "1H", "4H"]
    lookup_range = "5M" if is_intraday_derived else range
    
    cache_key = f"chart_base_v16_{symbol}_{lookup_range}"
    ttl = 300 if is_intraday_derived else 43200
    
    chart_data = await redis_service.redis_client.get_cache(cache_key)
    if not chart_data:
        if source == "FMP":
            chart_data = await asyncio.to_thread(fmp_service.get_commodity_history, fmp_ticker, range_type=lookup_range)
            if not chart_data:
                 chart_data = await asyncio.to_thread(fmp_service.get_crypto_history, fmp_ticker, range_type=lookup_range)
            if not chart_data:
                chart_data = await asyncio.to_thread(eodhd_service.get_historical_data, symbol, range_type=lookup_range)
        else:
            chart_data = await asyncio.to_thread(eodhd_service.get_historical_data, symbol, range_type=lookup_range)
        if chart_data:
            await redis_service.redis_client.set_cache(cache_key, chart_data, ttl)
    
    if not chart_data: return []
    final_data = chart_data
    
    # Resample for Display
    if is_intraday_derived and range != "5M":
        resampled = technical_service.resample_chart_data(chart_data, range)
        if resampled: final_data = resampled

    # Live Price Stitching
    try:
        current_price = 0
        if source == "FMP":
            q = await asyncio.to_thread(fmp_service.get_quote, fmp_ticker)
            current_price = q.get('price')
        else:
            q = await asyncio.to_thread(eodhd_service.get_live_price, symbol)
            current_price = q.get('price')
        if current_price and final_data:
            last = final_data[-1]
            last['close'] = current_price
            if current_price > last['high']: last['high'] = current_price
            if current_price < last['low']: last['low'] = current_price
    except Exception: pass 

    return final_data

@router.get("/{symbol}/all")
async def get_all_stock_data(symbol: str):
    cache_key = f"all_data_v27_{symbol}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached

    source, fmp_ticker = identify_asset_class(symbol)
    tasks = { "news": asyncio.to_thread(news_service.get_company_news, symbol) }

    if source == "FMP":
        tasks.update({
            "fmp_quote": asyncio.to_thread(fmp_service.get_quote, fmp_ticker),
            "chart_data": asyncio.to_thread(fmp_service.get_commodity_history, fmp_ticker, "1D") 
        })
    else:
        tasks.update({
            "eod_fund": asyncio.to_thread(eodhd_service.get_company_fundamentals, symbol),
            "eod_live": asyncio.to_thread(eodhd_service.get_live_price, symbol),
            "fmp_prof": asyncio.to_thread(fmp_service.get_company_profile, symbol),
            "fmp_rating": asyncio.to_thread(fmp_service.get_analyst_ratings, symbol),
            "fmp_target": asyncio.to_thread(fmp_service.get_price_target_consensus, symbol),
            "shareholding": asyncio.to_thread(fmp_service.get_shareholding_data, symbol),
            "chart_data": asyncio.to_thread(eodhd_service.get_historical_data, symbol, "1D")
        })

    try:
        results = await asyncio.gather(*tasks.values(), return_exceptions=True)
        raw = dict(zip(tasks.keys(), results))
    except: raw = {}

    def safe(k, d=None):
        val = raw.get(k)
        if isinstance(val, Exception) or val is None: return d
        return val

    final_data = {}

    if source == "FMP":
        q = safe('fmp_quote', {})
        if not q: q = await asyncio.to_thread(eodhd_service.get_live_price, symbol)

        final_data['profile'] = {
            "companyName": q.get('name') or symbol, 
            "symbol": symbol, "description": f"Real-Time Market Data for {symbol}.",
            "image": "", "currency": "USD", "sector": "Commodity/Crypto",
            "tradingview_symbol": TRADINGVIEW_OVERRIDE_MAP.get(symbol, symbol)
        }
        final_data['quote'] = q
        
        chart_data = safe('chart_data', [])
        if not chart_data:
             chart_data = await asyncio.to_thread(fmp_service.get_crypto_history, fmp_ticker, "1D")
        if not chart_data:
             chart_data = await asyncio.to_thread(eodhd_service.get_historical_data, symbol, "1D")

        # --- SAFE INITIALIZATION ---
        final_data['key_metrics'] = {} 
        final_data['annual_revenue_and_profit'] = []
        final_data['annual_balance_sheets'] = []
        final_data['annual_cash_flow_statements'] = []
        final_data['quarterly_income_statements'] = []
        final_data['quarterly_balance_sheets'] = []
        final_data['quarterly_cash_flow_statements'] = []
        final_data['shareholding'] = []
        final_data['shareholding_breakdown'] = {}
        eod_ratings, eod_targets, fmp_ratings, fmp_targets = [], {}, [], {}
        
    else:
        # STOCK LOGIC
        eod_fund = safe('eod_fund', {})
        eod_p = eodhd_service.parse_profile_from_fundamentals(eod_fund, symbol)
        fmp_p = safe('fmp_prof', {}) or {}
        tv_symbol = symbol
        if symbol in TRADINGVIEW_OVERRIDE_MAP: tv_symbol = TRADINGVIEW_OVERRIDE_MAP[symbol]
        elif symbol.endswith(".NS"): tv_symbol = "NSE:" + symbol.replace(".NS", "")
        
        final_data['profile'] = {**eod_p, "description": fmp_p.get("description") or eod_p.get("description"), "image": fmp_p.get("image") or eod_p.get("image"), "tradingview_symbol": tv_symbol}
        final_data['key_metrics'] = eodhd_service.parse_metrics_from_fundamentals(eod_fund)
        final_data['quote'] = safe('eod_live', {})
        final_data['annual_revenue_and_profit'] = eodhd_service.parse_financials(eod_fund, 'Financials::Income_Statement', 'yearly')
        final_data['annual_balance_sheets'] = eodhd_service.parse_financials(eod_fund, 'Financials::Balance_Sheet', 'yearly')
        final_data['annual_cash_flow_statements'] = eodhd_service.parse_financials(eod_fund, 'Financials::Cash_Flow', 'yearly')
        final_data['quarterly_income_statements'] = eodhd_service.parse_financials(eod_fund, 'Financials::Income_Statement', 'quarterly')
        final_data['quarterly_balance_sheets'] = eodhd_service.parse_financials(eod_fund, 'Financials::Balance_Sheet', 'quarterly')
        final_data['quarterly_cash_flow_statements'] = eodhd_service.parse_financials(eod_fund, 'Financials::Cash_Flow', 'quarterly')
        chart_data = safe('chart_data', [])
        share_bd = eodhd_service.parse_shareholding_breakdown(eod_fund)
        shares = eodhd_service.parse_holders(eod_fund)
        if share_bd.get('promoter') == 0:
            fmp_s = safe('shareholding', [])
            if fmp_s:
                t = sum(h.get('shares', 0) for h in fmp_s)
                share_bd = {"promoter": 0, "fii": t*0.6, "dii": t*0.4, "public": 0}
                shares = fmp_s
        final_data['shareholding'] = shares
        final_data['shareholding_breakdown'] = share_bd
        eod_ratings, eod_targets = eodhd_service.parse_analyst_data(eod_fund) if hasattr(eodhd_service, 'parse_analyst_data') else ([], {})
        fmp_ratings, fmp_targets = safe('fmp_rating', []), safe('fmp_target', {})

    tech_inds, mas, pivots, darvas = {}, {}, {}, {}
    if chart_data and len(chart_data) > 20:
        try:
            df = pd.DataFrame(chart_data)
            tech_inds = technical_service.calculate_technical_indicators(df)
            mas = technical_service.calculate_moving_averages(df)
            pivots = technical_service.calculate_pivot_points(df)
            if source != "FMP" and final_data['quote']:
                darvas = technical_service.calculate_darvas_box(df, final_data['quote'], final_data['profile'].get('currency', 'USD'))
        except: pass

    final_data['technical_indicators'] = tech_inds
    final_data['moving_averages'] = mas
    final_data['pivot_points'] = pivots
    final_data['darvas_scan'] = darvas

    piotroski, graham = {}, {}
    if source != "FMP":
        piotroski = fundamental_service.calculate_piotroski_f_score(final_data['annual_revenue_and_profit'], final_data['annual_balance_sheets'], final_data['annual_cash_flow_statements'])
        graham = fundamental_service.calculate_graham_scan(final_data['profile'], final_data.get('key_metrics', {}), final_data['annual_revenue_and_profit'], final_data['annual_cash_flow_statements'])
    
    final_data['piotroski_f_score'] = piotroski
    final_data['graham_scan'] = graham
    
    # SAFE CALL
    final_data['overall_sentiment'] = sentiment_service.calculate_overall_sentiment(
        piotroski.get('score'), 
        final_data.get('key_metrics', {}), 
        tech_inds, 
        safe('fmp_rating', [])
    )
    final_data['news'] = safe('news', [])

    def has_votes(r): return r and isinstance(r, list) and len(r)>0 and (r[0].get('ratingBuy',0)+r[0].get('ratingHold',0)+r[0].get('ratingSell',0) > 0)
    
    if source != "FMP" and has_votes(eod_ratings):
        final_data['analyst_ratings'] = eod_ratings; final_data['price_target_consensus'] = eod_targets
    elif source != "FMP" and has_votes(fmp_ratings):
        final_data['analyst_ratings'] = fmp_ratings; final_data['price_target_consensus'] = fmp_targets
    else:
        price = final_data['quote'].get('price') or 0
        if price == 0 and chart_data: price = chart_data[-1]['close']
        rsi = tech_inds.get('rsi', 50)
        syn = {"ratingStrongBuy": 0, "ratingBuy": 0, "ratingHold": 0, "ratingSell": 0, "ratingStrongSell": 0}
        if rsi < 30: syn["ratingStrongBuy"] = 12; syn["ratingBuy"] = 8
        elif rsi < 45: syn["ratingBuy"] = 10; syn["ratingHold"] = 10
        elif rsi < 55: syn["ratingHold"] = 20
        elif rsi < 70: syn["ratingSell"] = 10; syn["ratingHold"] = 10
        else: syn["ratingStrongSell"] = 12; syn["ratingSell"] = 8
        target = price if price > 0 else 100
        if price > 0:
            pc = pivots.get('classic', {})
            target = pc.get('r1') if rsi < 50 else pc.get('s1') or price
        final_data['analyst_ratings'] = [syn]
        final_data['price_target_consensus'] = {"targetHigh": target*1.1, "targetLow": target*0.9, "targetConsensus": target}

    pt = final_data.get('price_target_consensus', {})
    if not pt.get('targetConsensus'):
        p = final_data['quote'].get('price') or 100
        final_data['price_target_consensus'] = {"targetHigh": p*1.1, "targetLow": p*0.9, "targetConsensus": p}

    km = final_data.get('key_metrics', {})
    kq = final_data.get('quote', {})
    def n(v): return None if isinstance(v, float) and (math.isnan(v) or math.isinf(v)) else v

    final_data['keyStats'] = {
        "marketCap": n(km.get('marketCap')), "peRatio": n(km.get('peRatioTTM')), 
        "dividendYield": n(km.get('dividendYieldTTM')), "basicEPS": n(km.get('epsTTM')),
        "sharesFloat": n(km.get('sharesOutstanding')), "beta": n(km.get('beta')),
        "netIncome": n(km.get('epsTTM')), "revenue": n(km.get('revenueGrowth')),
        "dayLow": n(kq.get('dayLow') or kq.get('low')), 
        "dayHigh": n(kq.get('dayHigh') or kq.get('high')), 
        "yearHigh": n(kq.get('yearHigh') or kq.get('high')),
        "nextReportDate": None, "epsEstimate": None, "revenueEstimate": None
    }

    def clean_json(obj):
        if isinstance(obj, float): return None if math.isnan(obj) or math.isinf(obj) else obj
        if isinstance(obj, dict): return {k: clean_json(v) for k, v in obj.items()}
        if isinstance(obj, list): return [clean_json(v) for v in obj]
        return obj

    final = clean_json(final_data)
    await redis_service.redis_client.set_cache(cache_key, final, 300)
    return final


# ==========================================
# 5. THE "OMNI-ANALYST" ENGINE (ALL TIMEFRAMES AT ONCE)
# ==========================================

@router.post("/{symbol}/all-timeframe-analysis")
async def get_all_timeframe_analysis(symbol: str):
    """
    Generates AI Analysis for 5M, 15M, 1H, 4H, and 1D in a SINGLE request.
    Uses Mathematical Resampling to avoid extra API calls.
    """
    cache_key = f"omni_analysis_v1_{symbol}"
    cached = await redis_service.redis_client.get_cache(cache_key)
    if cached: return cached

    # 1. Identify Asset
    source, ticker = identify_asset_class(symbol)
    
    # 2. Fetch MASTER Data (5 Minute)
    # We use 5M because we can build 15M, 1H, 4H, 1D from it mathematically.
    if source == "FMP":
        chart_data = await asyncio.to_thread(fmp_service.get_commodity_history, ticker, range_type="5M")
        if not chart_data: chart_data = await asyncio.to_thread(fmp_service.get_crypto_history, ticker, range_type="5M")
    else:
        chart_data = await asyncio.to_thread(eodhd_service.get_historical_data, ticker, range_type="5M")

    if not chart_data or len(chart_data) < 50:
        return {"error": "Insufficient market data for analysis."}

    # 3. Define Targets
    timeframes = ["15M", "1H", "4H", "1D"]
    tasks = []

    # Helper function to process one timeframe
    async def process_timeframe(tf):
        try:
            # A. Resample (Math)
            # If tf is 5M, use original. Else resample.
            data = chart_data if tf == "5M" else technical_service.resample_chart_data(chart_data, tf)
            
            # B. Calculate Technicals (Math)
            df = pd.DataFrame(data)
            techs = technical_service.calculate_technical_indicators(df)
            pivots = technical_service.calculate_pivot_points(df)
            mas = technical_service.calculate_moving_averages(df)
            
            # C. Generate AI Insight
            analysis = await asyncio.to_thread(
                gemini_service.generate_timeframe_analysis, 
                symbol, tf, techs, pivots, mas
            )
            return tf.lower(), analysis # Return key like "1h"
        except:
            return tf.lower(), "Analysis unavailable."

    # 4. Execute Parallel Processing
    # We run 5 AI Models simultaneously. This takes ~3 seconds total instead of 15s.
    results = await asyncio.gather(
        process_timeframe("5M"),
        process_timeframe("15M"),
        process_timeframe("1H"),
        process_timeframe("4H"),
        process_timeframe("1D")
    )

    # 5. Construct Final Response
    response_map = {k: v for k, v in results}
    
    # Cache the heavy result
    await redis_service.redis_client.set_cache(cache_key, response_map, 300) # 5 min cache
    
    return response_map
```
