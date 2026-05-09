import sys
import os
import pandas as pd

# Add app path
sys.path.append('/home/team/shared/stock_analysis_app')

from src.analysis.scoring_engine import ScoringEngine

def verify_logic():
    engine = ScoringEngine(risk_level="Retailer High-Conviction")
    
    print("--- Verification of Retailer High-Conviction Logic ---")
    
    # Scenario 1: Perfect Alignment & High Score (Sure-Win)
    fundamentals = {
        'net_margin': 0.35,
        'fcf_growth': 0.25,
        'institutional_ownership': 0.85,
        'debt_to_equity': 10, # 0.1
        'current_ratio': 2.0,
        'revenue_growth': 0.20
    }
    technicals = {
        'price': 150,
        'sma20': 140,
        'sma50': 130,
        'sma200': 110,
        'rsi': 60,
        'macd': 5,
        'macd_signal': 2,
        'mfi': 70
    }
    analyst_consensus = {
        'recommendation_mean': 1.1,
        'target_mean_price': 200
    }
    
    score, details = engine.calculate_hc_score(fundamentals, technicals, analyst_consensus)
    passes, fails = engine.check_hc_hard_filters(fundamentals, technicals, analyst_consensus)
    
    print(f"Scenario 1 (Sure-Win Target): Score={score}, Passes Filters={passes}, Fails={fails}")
    
    # Scenario 2: Fails Perfect Alignment (Price < SMA20)
    technicals_fail_alignment = technicals.copy()
    technicals_fail_alignment['price'] = 135 # price < sma20 (140)
    
    passes_2, fails_2 = engine.check_hc_hard_filters(fundamentals, technicals_fail_alignment, analyst_consensus)
    print(f"Scenario 2 (Alignment Fail): Passes Filters={passes_2}, Fails={fails_2}")
    
    # Scenario 3: Low Institutional Ownership
    fundamentals_low_inst = fundamentals.copy()
    fundamentals_low_inst['institutional_ownership'] = 0.50
    
    passes_3, fails_3 = engine.check_hc_hard_filters(fundamentals_low_inst, technicals, analyst_consensus)
    print(f"Scenario 3 (Inst Fail): Passes Filters={passes_3}, Fails={fails_3}")

    # Scenario 4: High Debt
    fundamentals_high_debt = fundamentals.copy()
    fundamentals_high_debt['debt_to_equity'] = 60 # > 50 (0.5)
    
    passes_4, fails_4 = engine.check_hc_hard_filters(fundamentals_high_debt, technicals, analyst_consensus)
    print(f"Scenario 4 (Debt Fail): Passes Filters={passes_4}, Fails={fails_4}")

if __name__ == "__main__":
    verify_logic()
