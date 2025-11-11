from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .routers import stocks, indices

app = FastAPI(
    title="Stellar Stock Screener API",
    description="A high-performance API serving financial data for the stock screener frontend.",
    version="1.0.0"
)

# We include both of our API routers first.
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(indices.router, prefix="/api/indices", tags=["indices"])

# This serves the compiled JavaScript and CSS files.
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static_assets")

# This catch-all route is the key for a Single-Page Application.
# It ensures that any request not matching the API or static files
# will be served the main index.html file, allowing React Router to work.
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    return FileResponse("frontend/build/index.html")