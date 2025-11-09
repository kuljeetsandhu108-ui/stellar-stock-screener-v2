from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# These imports are now active for production.
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .routers import stocks

# Create the main FastAPI application instance
app = FastAPI(
    title="Stellar Stock Screener API",
    description="A high-performance API serving financial data for the stock screener frontend.",
    version="1.0.0"
)

# Define the list of allowed origins. While not strictly necessary when serving
# the frontend from the same domain, it's good practice to keep it.
origins = [
    "http://localhost:3000",
]

# Add the CORSMiddleware to the application.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the stocks router. All API endpoints defined in `routers/stocks.py`
# will be available under the `/api/stocks` prefix.
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])


# --- PRODUCTION-ONLY CODE ---
# This code block tells FastAPI to also act as a web server for our
# compiled React application.

# 1. Mount the 'build' directory from the frontend.
# This serves all the static files like CSS, JavaScript, and images.
# The `html=True` flag is essential for single-page applications.
app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")


# 2. Create a "catch-all" route.
# This is a crucial piece for React Router. If a user refreshes the page
# at a URL like '/stock/AAPL', the browser makes a request to the server for that specific path.
# This route catches that request and always responds with the main 'index.html' file.
# React Router then takes over on the frontend to display the correct page.
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    return FileResponse("frontend/build/index.html")