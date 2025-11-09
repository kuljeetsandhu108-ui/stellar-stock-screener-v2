from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .routers import stocks

app = FastAPI(
    title="Stellar Stock Screener API",
    description="A high-performance API serving financial data for the stock screener frontend.",
    version="1.0.0"
)

# 1. First, we include our API router.
# Any request starting with /api will be handled by our stocks.py file.
app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])

# 2. Next, we mount the specific '/static' directory from our React build.
# This is where all the compiled JavaScript and CSS files live.
# This ensures that requests for these files are handled correctly.
app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static_assets")

# 3. Finally, we create a "catch-all" route that MUST BE LAST.
# This route will match ANY other path that is not /api/... or /static/...
# For any such path (like /stock/TSLA or / or /financials), it will
# always serve the main index.html file. React Router will then handle the rest.
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    return FileResponse("frontend/build/index.html")