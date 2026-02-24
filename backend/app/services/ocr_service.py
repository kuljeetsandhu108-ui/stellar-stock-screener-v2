import pytesseract
from PIL import Image
import io
import re
import os

# Point to the Windows installation of Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR	esseract.exe"

def extract_ticker_fast(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        # Crop the top-left 30% of the image to speed up scanning and find the ticker
        width, height = image.size
        crop_area = (0, 0, int(width * 0.3), int(height * 0.2))
        cropped_img = image.crop(crop_area)
        
        # Read the text
        text = pytesseract.image_to_string(cropped_img)
        
        # Find the first uppercase word that looks like a ticker (e.g. RELIANCE, AAPL, NIFTY)
        matches = re.findall(r'\b[A-Z]{2,12}\b', text)
        if matches:
            return matches[0]
        return "NOT_FOUND"
    except Exception as e:
        print(f"OCR Error: {e}")
        return "NOT_FOUND"
