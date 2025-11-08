from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# --- NEW IMPORTS ---
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
    # In production, we don't need localhost, but it's good for testing.
    # The Railway domain will be added here later if needed, but serving static files
    # often makes complex CORS unnecessary.
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- NEW: Serve API Routes First ---
# It's crucial that the API router is included BEFORE the static files mount.
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])

# --- NEW: Mount the static files from the React build ---
# This tells FastAPI to serve the 'build' folder from the frontend.
# The `html=True` part is key for Single-Page Applications like React.
app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")

# This ensures that any path not caught by the API will be handled by React Router
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    return FileResponse("frontend/build/index.html")