from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services import gemini_service
import asyncio

router = APIRouter()

@router.post("/analyze")
async def analyze_chart_image(chart_image: UploadFile = File(...)):
    """
    This is the master endpoint for our AI Chart Analysis feature.
    It receives an uploaded image and performs a two-step AI analysis:
    1. Identify the stock symbol.
    2. Perform a professional technical analysis and generate a trade setup.
    """
    print("Received chart image for analysis...")

    # Ensure the uploaded file is an image
    if not chart_image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    # Read the image content into memory
    image_bytes = await chart_image.read()

    # --- Step 1: First AI Task - Identify the Ticker Symbol ---
    print("Task 1: Asking AI to identify the ticker symbol from the image...")
    
    # We run this in a separate thread to not block the server
    identified_symbol = await asyncio.to_thread(
        gemini_service.identify_ticker_from_image,
        image_bytes
    )

    if not identified_symbol or identified_symbol == "NOT_FOUND":
        print("AI could not identify a ticker symbol.")
        return {
            "identified_symbol": "NOT_FOUND", 
            "analysis_data": None
        }
    
    print(f"AI successfully identified ticker: {identified_symbol}")

    # --- Step 2: Second AI Task - Perform In-Depth Technical Analysis ---
    print("Task 2: Asking AI for in-depth technical analysis of the image...")
    
    # This function calls the 'gemini-1.5-flash' model with the image
    analysis_data = await asyncio.to_thread(
        gemini_service.analyze_chart_technicals_from_image,
        image_bytes
    )

    # --- Step 3: Return both results to the frontend ---
    return {
        "identified_symbol": identified_symbol,
        "analysis_data": analysis_data
    }