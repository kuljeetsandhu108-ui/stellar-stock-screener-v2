from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# We must import both of our routers to make their endpoints available.
from .routers import stocks, indices, charts

# Create the main FastAPI application instance.
app = FastAPI(
    title="Stellar Stock Screener API",
    description="A high-performance API serving financial data for the stock screener frontend.",
    version="1.0.0"
)

# --- ROUTER INCLUSION ---
# It is critical that the API routers are included BEFORE the static file routes.
# This ensures that a request like '/api/stocks/AAPL/all' is handled by our API logic
# and not misinterpreted as a request for a file on the server.

# Include the stocks router for all company-specific API calls.
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])

# Include the indices router for all market index API calls.
app.include_router(indices.router, prefix="/api/indices", tags=["indices"])

# Include the charts router for our AI chart analysis feature.
app.include_router(charts.router, prefix="/api/charts", tags=["charts"])


# --- STATIC FILE SERVING (FOR REACT FRONTEND) ---
# This code block tells our single Python server to also act as a web server
# for our compiled React application when in production.

# 1. Mount the '/static' directory from our React 'build' folder.
# This is where all the compiled JavaScript, CSS, and other assets are located.
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static_assets")


# 2. Create the "catch-all" route. This MUST BE THE LAST route defined in the file.
# This route is the key to making a Single-Page Application (SPA) like React work correctly.
# It matches ANY path that was not matched by the API routers or the /static mount above.
# For any such path (e.g., '/', '/stock/AAPL'), it will always serve the main 'index.html' file.
# React Router then takes over on the frontend to display the correct page.
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    index_path = os.path.join("frontend/build", "index.html")

    if not os.path.exists(index_path):
        return {"error": "index.html not found in build directory"}, 500

    return FileResponse(index_path)