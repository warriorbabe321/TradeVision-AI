# Hedge Fund Decision Hierarchy Logic

This document defines the 4-level hierarchy used to arrive at a "Superior" investment decision, simulating a professional hedge fund workflow.

---

## Level 1: Research (The Data Foundation)
Standardizing the five core parameters to ensure a comprehensive data set.

| Parameter | Key Metrics |
| :--- | :--- |
| **Fundamentals** | P/E Ratio, PEG Ratio, Revenue Growth (YoY), Net Margin, Debt-to-Equity. |
| **Technicals** | 50/200 SMA (Trend), RSI (Momentum), MACD (Signal), OBV (Volume), Bollinger Bands (Volatility). |
| **Analyst Ratings** | Mean Consensus (Buy/Hold/Sell), Average Price Target vs. Current Price. |
| **Insider/News** | Net Insider Buying/Selling (last 3 months), News Sentiment Score (NLP). |
| **Market Sentiment** | Fear & Greed Index, VIX (Volatility Index), Social Media Buzz Score. |

---

## Level 2: The Debate (Conflict Resolution)
Defining the "Bullish" and "Bearish" arguments based on conflicting signals.

### Common Conflict Scenarios
1. **Growth vs. Stability**: High Revenue Growth (>20%) but High Debt-to-Equity (>1.5).
    - *Bullish Thesis*: Aggressive expansion in a growing market.
    - *Bearish Thesis*: Overleveraged and vulnerable to interest rate hikes.
2. **Technicals vs. Fundamentals**: Bullish MACD/RSI but Overvalued P/E (top 10% of industry).
    - *Bullish Thesis*: Momentum play; price reflects future earnings dominance.
    - *Bearish Thesis*: A bubble ready to burst; price is detached from reality.
3. **Sentiment vs. Reality**: Strong Positive News/Social Buzz but declining Net Margins.
    - *Bullish Thesis*: Temporary margin squeeze during a brand-building phase.
    - *Bearish Thesis*: Hype cycle hiding structural business decay.

---

## Level 3: Risk Management (The Gatekeeper)
"No-Go" criteria that override any "Buy" signal to protect capital.

### The "No-Go" List (Instant Reject)
- **Debt Crisis**: Debt-to-Equity > 2.0.
- **Margin Collapse**: Negative Net Margin for 2 consecutive quarters.
- **Regulatory Heat**: SEC Investigation, Fraud Allegations, or significant Legal Headwinds.
- **Liquidity Trap**: Average Daily Volume < $1M (Hard to exit positions).

### Stop-Loss Logic
- **Aggressive (Day Trade)**: 3-5% below entry.
- **Standard (Growth)**: 8-10% below entry.
- **Patient (Long-Term)**: 15% below entry (trailing stop-loss recommended).

---

## Level 4: Fund Manager (The Agreeable Verdict)
The final summary and decision template.

### Final Verdict Template
- **Verdict**: [Strong Buy / Buy / Hold / Sell / Strong Sell]
- **The Thesis**: (A concise 2-3 sentence explanation of the "Why").
- **Hedge Fund Debate Summary**:
    - *Bull Case*: (Top 1 argument from Level 2).
    - *Bear Case*: (Top 1 argument from Level 2).
- **Risk Assessment**: (Status of No-Go criteria and recommended Stop-Loss).
- **Execution Plan**:
    - **Entry Target**: $XXX.XX
    - **Price Target**: $XXX.XX
    - **Stop-Loss**: $XXX.XX
