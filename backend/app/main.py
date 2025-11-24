from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# We must import ALL our routers
from .routers import stocks, indices, charts

# Create the main FastAPI application instance.
app = FastAPI(
    title="Stellar Stock Screener API",
    description="A high-performance API serving financial data for the stock screener frontend.",
    version="1.0.0"
)

# --- ROUTER INCLUSION ---
# Include all specific API routers BEFORE the static file routes.

# 1. Stocks Router (Search, Details, Fundamentals, AI)
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])

# 2. Indices Router (Market Banner, Index Details)
app.include_router(indices.router, prefix="/api/indices", tags=["indices"])

# 3. Charts Router (AI Image Analysis)
app.include_router(charts.router, prefix="/api/charts", tags=["charts"])


# --- STATIC FILE SERVING (FOR REACT FRONTEND) ---
# This code block tells our single Python server to also act as a web server
# for our compiled React application when in production.

# 1. Mount the '/static' directory from our React 'build' folder.
# This handles CSS, JS, and images.
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static_assets")


# 2. Create the "catch-all" route. This MUST BE THE LAST route.
# It ensures that any request not matched by an API endpoint returns the React app.
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    # Construct the path to the index.html file within the container
    index_path = os.path.join("frontend/build", "index.html")

    # Safety check
    if not os.path.exists(index_path):
        return {"error": "index.html not found in build directory"}, 500

    return FileResponse(index_path)