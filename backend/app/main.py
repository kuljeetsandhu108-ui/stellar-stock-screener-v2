from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import os

# Import Routers
from .routers import stocks, indices, charts, live

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
app.include_router(live.router, prefix="/ws", tags=["live"])


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