import json
import sys
import pandas as pd
from src.data_fetcher.yfinance_fetcher import YFinanceFetcher
from src.data_fetcher.alphavantage_fetcher import AlphaVantageFetcher
from src.data_fetcher.alternative_data_fetcher import AlternativeDataFetcher
from src.indicators.technical import (
    calculate_sma, calculate_rsi, calculate_macd,
    calculate_bollinger_bands, calculate_atr, calculate_vwap, calculate_obv,
    calculate_rvol, identify_hammer, identify_doji, calculate_mfi
)
from src.analysis.scoring_engine import ScoringEngine
from src.utils.db_utils import log_signal
from dotenv import load_dotenv
import os

load_dotenv()

def analyze_stock(ticker, risk_level="Standard", horizon="Short Term"):
    yf_fetcher = YFinanceFetcher()
    av_fetcher = AlphaVantageFetcher()
    alt_fetcher = AlternativeDataFetcher()
    scoring_engine = ScoringEngine(risk_level=risk_level, horizon=horizon)

    print(f"Analyzing {ticker} in {risk_level} mode...")

    # 1. Fetch Data
    try:
        hist_data = yf_fetcher.get_stock_data(ticker, period="1y")
        if hist_data.empty:
            print(f"No historical data for {ticker}")
            return None

        quote = yf_fetcher.get_real_time_quote(ticker)
        fundamentals = yf_fetcher.get_fundamentals(ticker)
        recommendations = yf_fetcher.get_analyst_recommendations(ticker)
        inst_holders = yf_fetcher.get_institutional_holders(ticker)
        
        # Optional news sentiment
        news_sentiment = av_fetcher.get_news_sentiment(ticker)
        
        # Insider & Alternative Data
        insider_purchases = yf_fetcher.get_insider_purchases(ticker)
        politician_trades = alt_fetcher.get_politician_trades(ticker)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

    # 2. Calculate Technicals
    sma20 = calculate_sma(hist_data, 20).iloc[-1]
    sma50 = calculate_sma(hist_data, 50).iloc[-1]
    sma200 = calculate_sma(hist_data, 200).iloc[-1]
    rsi = calculate_rsi(hist_data, 14).iloc[-1]
    macd_line, signal_line = calculate_macd(hist_data)
    macd_val = macd_line.iloc[-1]
    signal_val = signal_line.iloc[-1]
    
    upper_bb, mid_bb, lower_bb = calculate_bollinger_bands(hist_data)
    atr = calculate_atr(hist_data).iloc[-1]
    vwap = calculate_vwap(hist_data).iloc[-1]
    obv = calculate_obv(hist_data).iloc[-1]
    rvol = calculate_rvol(hist_data).iloc[-1]
    is_hammer = bool(identify_hammer(hist_data).iloc[-1])
    is_doji = bool(identify_doji(hist_data).iloc[-1])

    current_price = quote['price']
    
    # Technical Summary for scoring
    tech_summary = {
        'price': current_price,
        'sma20': sma20,
        'sma50': sma50,
        'sma200': sma200,
        'rsi': rsi,
        'rvol': rvol,
        'hammer': is_hammer,
        'doji': is_doji,
        'macd': macd_val,
        'macd_signal': signal_val,
        'lower_bb': lower_bb.iloc[-1] if not lower_bb.empty else None,
        'upper_bb': upper_bb.iloc[-1] if not upper_bb.empty else None,
        'mfi': calculate_mfi(hist_data).iloc[-1],
        'vwap': vwap,
        'atr': atr
    }

    t_score, t_details = scoring_engine.calculate_technical_score(
        current_price, sma50, sma200, rsi, macd_val, signal_val
    )

    # 3. Calculate Fundamentals
    f_score, f_details = scoring_engine.calculate_fundamental_score(
        fundamentals['pe_ratio'],
        fundamentals['peg_ratio'],
        fundamentals['revenue_growth'],
        fundamentals['net_margin'],
        fundamentals['debt_to_equity']
    )

    # 4. Calculate Sentiment
    s_score, s_details = scoring_engine.calculate_sentiment_score(
        recommendations['recommendation_key'],
        news_sentiment
    )
    
    # 4.1 Panic & Vulture Check
    panic_triggered, panic_triggers = scoring_engine.check_panic_signal(hist_data, tech_summary)
    vulture_data = None
    if panic_triggered:
        v_score, v_details = scoring_engine.calculate_vulture_score(fundamentals, tech_summary)
        
        v_verdict = "Vulture Buy" if v_score >= 80 else "Speculative Watch" if v_score >= 50 else "Falling Knife"
        
        vulture_data = {
            "Score": v_score,
            "Details": v_details,
            "Verdict": v_verdict,
            "PanicTriggers": panic_triggers
        }
        
    # 4.2 Insider & Alternative Scan
    alt_score, alt_details = scoring_engine.calculate_alternative_score(insider_purchases, politician_trades)

    # 5. Composite Score & Verdict
    composite_score = scoring_engine.get_composite_score(t_score, f_score, s_score)
    
    # Hierarchy Level 2: The Debate
    debate = generate_debate(fundamentals, t_details, s_details)
    
    # Hierarchy Level 3: Risk Management
    risk_mgmt = perform_risk_assessment(fundamentals, quote, horizon)
    
    # Hierarchy Level 4: Verdict
    final_signal = scoring_engine.get_signal(composite_score)
    if risk_mgmt['no_go_triggered']:
        final_signal = "STRONG SELL (Risk Override)"

    # Vulture Override
    if vulture_data:
        final_signal = f"VULTURE: {vulture_data['Verdict']}"

    # Handle Retailer High-Conviction Mode
    hc_data = None
    if risk_level == "Retailer High-Conviction":
        # Add sma20 to tech_summary for HC mode if not already there
        tech_summary['sma20'] = sma20
        hc_score, hc_details = scoring_engine.calculate_hc_score(fundamentals, tech_summary, recommendations)
        passes_filters, filter_fails = scoring_engine.check_hc_hard_filters(fundamentals, tech_summary, recommendations)
        
        hc_verdict = "AVOID / NOT PICKY ENOUGH"
        if passes_filters:
            is_perfect = bool(current_price > sma20 > sma50 > sma200)
            if hc_score >= 95 and is_perfect: 
                hc_verdict = "SURE-WIN / RETAIL GOLD"
                try:
                    log_signal(ticker, current_price, hc_verdict, hc_score)
                except Exception as e:
                    print(f"Failed to log signal: {e}")
            elif hc_score >= 85: hc_verdict = "HIGH CONVICTION BUY"
            elif hc_score >= 75: hc_verdict = "STANDARD BUY"
        
        hc_data = {
            "Score": hc_score,
            "Details": hc_details,
            "PassesFilters": passes_filters,
            "FilterFails": filter_fails,
            "Verdict": hc_verdict
        }
        final_signal = hc_verdict

    # Data Integrity Check
    missing_params = []
    if fundamentals.get('institutional_ownership') is None: missing_params.append("Institutional Ownership")
    if fundamentals.get('net_margin') is None: missing_params.append("Net Margin")
    if fundamentals.get('debt_to_equity') is None: missing_params.append("Debt to Equity")
    if quote.get('price') is None: missing_params.append("Current Price")
    
    # 6. Prepare Output
    # Format historical data for charts
    chart_data = []
    sma20_hist = calculate_sma(hist_data, 20)
    sma50_hist = calculate_sma(hist_data, 50)
    sma200_hist = calculate_sma(hist_data, 200)
    rsi_hist = calculate_rsi(hist_data, 14)
    macd_line_hist, signal_line_hist = calculate_macd(hist_data)
    upper_bb_hist, _, lower_bb_hist = calculate_bollinger_bands(hist_data)
    mfi_hist = calculate_mfi(hist_data)
    vwap_hist = calculate_vwap(hist_data)
    atr_hist = calculate_atr(hist_data)
    vol_sma20 = hist_data['Volume'].rolling(window=20).mean()

    for i, (date, row) in enumerate(hist_data.iterrows()):
        close_val = row['Close']
        s20 = sma20_hist.iloc[i]
        s50 = sma50_hist.iloc[i]
        s200 = sma200_hist.iloc[i]
        
        is_golden = False
        if not (pd.isna(s20) or pd.isna(s50) or pd.isna(s200)):
            is_golden = bool(close_val > s20 > s50 > s200)
            
        is_uptrend = s50 > s200 if not (pd.isna(s50) or pd.isna(s200)) else False
        touches_20 = row['Low'] <= s20 <= row['High'] if not pd.isna(s20) else False
        touches_50 = row['Low'] <= s50 <= row['High'] if not pd.isna(s50) else False
        buy_dip = bool(is_uptrend and (touches_20 or touches_50))

        # Caution/Reject logic
        caution = bool(close_val < s20) if not pd.isna(s20) else False
        reject = bool(close_val < s50 or close_val < s200) if not (pd.isna(s50) or pd.isna(s200)) else False

        chart_data.append({
            "time": date.strftime('%Y-%m-%d'),
            "open": round(row['Open'], 2),
            "high": round(row['High'], 2),
            "low": round(row['Low'], 2),
            "close": round(row['Close'], 2),
            "volume": int(row['Volume']),
            "vol_sma20": round(vol_sma20.iloc[i], 0) if not pd.isna(vol_sma20.iloc[i]) else None,
            "sma20": round(s20, 2) if not pd.isna(s20) else None,
            "sma50": round(s50, 2) if not pd.isna(s50) else None,
            "sma200": round(s200, 2) if not pd.isna(s200) else None,
            "golden_zone": is_golden,
            "buy_dip": buy_dip,
            "caution": caution,
            "reject": reject,
            "rsi": round(rsi_hist.iloc[i], 2) if not pd.isna(rsi_hist.iloc[i]) else None,
            "macd": round(macd_line_hist.iloc[i], 2) if not pd.isna(macd_line_hist.iloc[i]) else None,
            "macd_signal": round(signal_line_hist.iloc[i], 2) if not pd.isna(signal_line_hist.iloc[i]) else None,
            "bb_upper": round(upper_bb_hist.iloc[i], 2) if not pd.isna(upper_bb_hist.iloc[i]) else None,
            "bb_lower": round(lower_bb_hist.iloc[i], 2) if not pd.isna(lower_bb_hist.iloc[i]) else None,
            "mfi": round(mfi_hist.iloc[i], 2) if not pd.isna(mfi_hist.iloc[i]) else None,
            "vwap": round(vwap_hist.iloc[i], 2) if not pd.isna(vwap_hist.iloc[i]) else None,
            "atr": round(atr_hist.iloc[i], 2) if not pd.isna(atr_hist.iloc[i]) else None
        })

    result = {
        "Ticker": ticker,
        "Company": quote['company_name'],
        "CurrentPrice": round(current_price, 2) if current_price else None,
        "DailyChange": round(quote['change'], 2) if quote['change'] else None,
        "Signal": final_signal,
        "Confidence": round(composite_score / 100, 2),
        "RSI": round(rsi, 2) if rsi else None,
        "MACD": round(macd_val, 2) if macd_val else None,
        "BollingerBands": {
            "Upper": round(upper_bb.iloc[-1], 2) if not upper_bb.empty else None,
            "Lower": round(lower_bb.iloc[-1], 2) if not lower_bb.empty else None
        },
        "ATR": round(atr, 2) if atr else None,
        "VWAP": round(vwap, 2) if vwap else None,
        "OBV": round(obv, 2) if obv else None,
        "PE_Ratio": round(fundamentals['pe_ratio'], 2) if fundamentals['pe_ratio'] else None,
        "RevenueGrowth": f"{round(fundamentals['revenue_growth']*100, 2)}%" if fundamentals['revenue_growth'] else "N/A",
        "NetMargin": f"{round(fundamentals['net_margin']*100, 2)}%" if fundamentals['net_margin'] else "N/A",
        "DebtToEquity": fundamentals['debt_to_equity'],
        "TopHolders": inst_holders['Holder'].head(3).tolist() if inst_holders is not None and not inst_holders.empty else [],
        "Thesis": generate_thesis(ticker, final_signal, t_details, f_details, s_details),
        "Debate": debate,
        "RiskMgmt": risk_mgmt,
        "HighConviction": hc_data,
        "VultureData": vulture_data,
        "ExecutionPlan": generate_execution_plan(current_price, horizon),
        "EliteSignals": {
            "Score": alt_score,
            "Details": alt_details,
            "PoliticianTrades": politician_trades.to_dict('records') if politician_trades is not None else []
        },
        "InsiderActivity": {
            "Score": alt_score,
            "Status": alt_details['insider']
        },
        "DataIntegrity": {
            "Status": "Reliable" if not missing_params else "Incomplete",
            "MissingParams": missing_params,
            "Notice": "Data is delayed by up to 15 minutes."
        },
        "ChartData": chart_data
    }

    return result

def generate_thesis(ticker, signal, t_details, f_details, s_details):
    # Simple rule-based thesis generator
    reasons = []
    if t_details['trend'] == 100: reasons.append("Strong bullish price trend")
    if t_details['momentum'] >= 75: reasons.append("Attractive oversold momentum")
    if f_details.get('pe') == 100: reasons.append("Undervalued relative to industry")
    if f_details.get('growth') == 100: reasons.append("Exceptional revenue growth")
    
    summary = f"{signal} signal for {ticker} based on composite analysis. "
    if reasons:
        summary += "Key factors: " + ", ".join(reasons) + "."
    else:
        summary += "Mixed signals observed across indicators."
        
    return summary

def generate_debate(fundamentals, t_details, s_details):
    bull_cases = []
    bear_cases = []
    
    # Growth vs Stability
    rev_growth = fundamentals.get('revenue_growth')
    de = fundamentals.get('debt_to_equity')
    if rev_growth and rev_growth > 0.20:
        bull_cases.append("Aggressive expansion in a growing market (>20% growth).")
        if de and de > 150: # yfinance 150 = 1.5
            bear_cases.append("Overleveraged (D/E > 1.5) and vulnerable to rate hikes.")
            
    # Technicals vs Fundamentals
    if t_details['macd'] == 100 and t_details['trend'] >= 50:
        bull_cases.append("Momentum play; price reflects future earnings dominance.")
        pe = fundamentals.get('pe_ratio')
        if pe and pe > 40:
            bear_cases.append("Potential bubble; P/E is detached from historical reality.")
            
    # Sentiment vs Reality
    if s_details['analyst'] >= 75:
        bull_cases.append("Strong institutional and analyst backing.")
        margin = fundamentals.get('net_margin')
        if margin and margin < 0.05:
            bear_cases.append("Hype cycle hiding thin or declining profit margins.")

    return {
        "BullCase": bull_cases[0] if bull_cases else "Positive momentum and sector tailwinds.",
        "BearCase": bear_cases[0] if bear_cases else "Macroeconomic uncertainty and competitive pressures."
    }

def perform_risk_assessment(fundamentals, quote, horizon):
    no_go_triggered = False
    reasons = []
    
    # Debt Crisis
    de = fundamentals.get('debt_to_equity')
    if de and de > 200: # yfinance 200 = 2.0
        no_go_triggered = True
        reasons.append("Debt Crisis: D/E > 2.0")
        
    # Margin Collapse
    margin = fundamentals.get('net_margin')
    if margin and margin < 0:
        no_go_triggered = True
        reasons.append("Margin Collapse: Negative Net Margin")
        
    # Liquidity Trap
    volume = quote.get('volume')
    price = quote.get('price')
    if volume and price and (volume * price < 1000000):
        no_go_triggered = True
        reasons.append("Liquidity Trap: Daily Volume < $1M")
        
    # Stop Loss Logic
    stop_loss_pct = 0.10
    if horizon == "Day Trade": stop_loss_pct = 0.04
    elif horizon == "Long Term": stop_loss_pct = 0.15
    
    current_price = quote.get('price')
    stop_loss = current_price * (1 - stop_loss_pct) if current_price else None
    
    return {
        "no_go_triggered": no_go_triggered,
        "reasons": reasons,
        "stop_loss": round(stop_loss, 2) if stop_loss else None
    }

def generate_execution_plan(price, horizon):
    if not price: return {}
    
    target_pct = 0.15
    if horizon == "Day Trade": target_pct = 0.05
    elif horizon == "Long Term": target_pct = 0.30
    
    return {
        "Entry": round(price, 2),
        "Target": round(price * (1 + target_pct), 2),
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Analyze a stock ticker.')
    parser.add_argument('ticker', help='The stock ticker to analyze (e.g., AAPL)')
    parser.add_argument('--risk', default='Standard', choices=['Standard', 'Conservative', 'Retailer High-Conviction'], help='Risk level')
    parser.add_argument('--horizon', default='Short Term', choices=['Day Trade', 'Short Term', 'Long Term'], help='Time horizon')
    args = parser.parse_args()
    
    ticker = args.ticker.upper()
    analysis = analyze_stock(ticker, risk_level=args.risk, horizon=args.horizon)
    if analysis:
        print(json.dumps(analysis, indent=2))
