import pandas as pd

def calculate_darvas_box(hist_df: pd.DataFrame, quote: dict):
    """
    Analyzes historical price data to identify a Darvas Box pattern.
    Returns the status and key levels of the box if found.
    """
    # --- Step 1: Basic Data Validation ---
    # We need at least 30 days of data and the latest quote.
    if hist_df is None or len(hist_df) < 30 or not quote:
        return {"status": "Insufficient Data", "message": "Not enough historical data to perform scan."}

    try:
        current_price = quote.get('price')
        year_high = quote.get('yearHigh')
        avg_volume = quote.get('avgVolume')
        current_volume = quote.get('volume')

        if not all([current_price, year_high, avg_volume, current_volume]):
             return {"status": "Insufficient Data", "message": "Missing key price or volume data."}

        # --- Step 2: Core Darvas Criteria - Near 52-Week High ---
        # A true Darvas stock should be within ~10% of its yearly high.
        if current_price < (year_high * 0.90):
            return {
                "status": "Not a Candidate",
                "message": f"Stock price (${current_price:.2f}) is not within 10% of its 52-week high (${year_high:.2f})."
            }

        # --- Step 3: Identify the "Box" ---
        # We'll look at the last 15 trading days to define the box.
        recent_period = hist_df.tail(15)
        box_top = recent_period['high'].max()
        box_bottom = recent_period['low'].min()

        # A valid box should have a narrow range (e.g., less than 8% from top to bottom).
        if box_top > box_bottom * 1.08:
            return {
                "status": "No Box Formed",
                "message": "Stock is too volatile and has not formed a narrow consolidation box recently."
            }

        # --- Step 4: Determine the Status (Breakout, In Box, or Breakdown) ---
        if current_price > box_top:
            # BREAKOUT! Check if it's on high volume.
            volume_check = "on high volume" if current_volume > (avg_volume * 1.5) else "on average volume"
            return {
                "status": "Breakout!",
                "message": f"Stock has broken out above the box top of ${box_top:.2f} {volume_check}.",
                "box_top": box_top,
                "box_bottom": box_bottom,
                "result": "Pass"
            }
        
        elif current_price < box_bottom:
            return {
                "status": "Breakdown",
                "message": f"Stock has broken down below the box bottom of ${box_bottom:.2f}.",
                "box_top": box_top,
                "box_bottom": box_bottom,
                "result": "Fail"
            }
        
        else:
            return {
                "status": "In Box",
                "message": f"Stock is consolidating in a Darvas Box between ${box_bottom:.2f} and ${box_top:.2f}.",
                "box_top": box_top,
                "box_bottom": box_bottom,
                "result": "Neutral"
            }

    except Exception as e:
        print(f"Error calculating Darvas Box: {e}")
        return {"status": "Calculation Error", "message": str(e)}