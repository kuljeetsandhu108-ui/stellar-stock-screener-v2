import pandas as pd

def calculate_piotroski_f_score(income_statements, balance_sheets, cash_flow_statements):
    """
    Calculates the Piotroski F-Score based on 9 criteria using historical financial data.
    """
    score = 0
    criteria_met = []

    # Ensure we have at least two years of data to compare
    if len(income_statements) < 2 or len(balance_sheets) < 2 or len(cash_flow_statements) < 2:
        return {"score": 0, "criteria": ["Not enough historical data."]}

    # Use pandas DataFrames for easier data manipulation
    try:
        income_df = pd.DataFrame(income_statements).set_index('date').sort_index()
        balance_df = pd.DataFrame(balance_sheets).set_index('date').sort_index()
        cash_flow_df = pd.DataFrame(cash_flow_statements).set_index('date').sort_index()

        # Get current and previous year's data
        cy = income_df.index[-1] # Current Year
        py = income_df.index[-2] # Previous Year

        # --- Piotroski F-Score Criteria (9 points) ---

        # 1. Net Income (Profitability)
        net_income = income_df.loc[cy, 'netIncome']
        if net_income > 0:
            score += 1
            criteria_met.append("Positive Net Income")

        # 2. Operating Cash Flow (Profitability)
        op_cash_flow = cash_flow_df.loc[cy, 'operatingCashFlow']
        if op_cash_flow > 0:
            score += 1
            criteria_met.append("Positive Operating Cash Flow")

        # 3. Return On Assets (ROA) Trend (Profitability)
        total_assets_cy = balance_df.loc[cy, 'totalAssets']
        total_assets_py = balance_df.loc[py, 'totalAssets']
        roa_cy = net_income / total_assets_cy
        roa_py = income_df.loc[py, 'netIncome'] / total_assets_py
        if roa_cy > roa_py:
            score += 1
            criteria_met.append("Increasing Return on Assets (ROA)")

        # 4. Quality of Earnings (Profitability)
        if op_cash_flow > net_income:
            score += 1
            criteria_met.append("Operating Cash Flow > Net Income")

        # 5. Long-Term Debt vs Assets (Leverage)
        debt_cy = balance_df.loc[cy, 'longTermDebt'] / total_assets_cy
        debt_py = balance_df.loc[py, 'longTermDebt'] / total_assets_py
        if debt_cy < debt_py:
            score += 1
            criteria_met.append("Lower Long-term Debt Ratio")

        # 6. Current Ratio Trend (Liquidity)
        current_ratio_cy = balance_df.loc[cy, 'totalCurrentAssets'] / balance_df.loc[cy, 'totalCurrentLiabilities']
        current_ratio_py = balance_df.loc[py, 'totalCurrentAssets'] / balance_df.loc[py, 'totalCurrentLiabilities']
        if current_ratio_cy > current_ratio_py:
            score += 1
            criteria_met.append("Higher Current Ratio")

        # 7. Shares Outstanding (Dilution)
        shares_cy = income_df.loc[cy, 'weightedAverageShsOut']
        shares_py = income_df.loc[py, 'weightedAverageShsOut']
        if shares_cy <= shares_py:
            score += 1
            criteria_met.append("No new shares issued (no dilution)")

        # 8. Gross Margin Trend (Operating Efficiency)
        gross_margin_cy = income_df.loc[cy, 'grossProfit'] / income_df.loc[cy, 'revenue']
        gross_margin_py = income_df.loc[py, 'grossProfit'] / income_df.loc[py, 'revenue']
        if gross_margin_cy > gross_margin_py:
            score += 1
            criteria_met.append("Higher Gross Margin")

        # 9. Asset Turnover Trend (Operating Efficiency)
        asset_turnover_cy = income_df.loc[cy, 'revenue'] / total_assets_py # Avg assets is better, but this is a common proxy
        asset_turnover_py = income_df.loc[py, 'revenue'] / (balance_df.iloc[-3]['totalAssets'] if len(balance_df) > 2 else total_assets_py)
        if asset_turnover_cy > asset_turnover_py:
            score += 1
            criteria_met.append("Higher Asset Turnover Ratio")
            
    except Exception as e:
        print(f"Could not calculate Piotroski score due to missing data or error: {e}")
        return {"score": 0, "criteria": [f"Calculation error: {e}"]}

    return {"score": score, "criteria": criteria_met}