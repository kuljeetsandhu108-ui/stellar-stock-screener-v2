from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# --- UNCOMMENTED FOR PRODUCTION ---
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .routers import stocks

app = FastAPI(
    title="Stellar Stock Screener API",
    description="A high-performance API serving financial data for the stock screener frontend.",
    version="1.0.0"
)

origins = [
    # This is not strictly needed in production when serving from the same domain,
    # but it doesn't hurt to have it.
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])

# --- UNCOMMENTED FOR PRODUCTION ---
# This tells FastAPI to serve the React app's static files.
app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")

# This catch-all route ensures that refreshing a page like /stock/AAPL works correctly.
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    return FileResponse("frontend/build/index.html")