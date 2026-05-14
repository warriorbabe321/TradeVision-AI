# US Stock Analysis Strategy and Metrics

## 1. Core Philosophy
The goal is to provide a holistic view of a stock by combining multiple dimensions of analysis. A "superior" decision is one backed by convergence across Technicals, Fundamentals, and Sentiment.

## 2. Technical Indicators (Short-to-Medium Term)
These indicators help identify entry and exit points.

| Category | Indicator | Purpose |
| :--- | :--- | :--- |
| **Trend** | SMA (50, 200) | Identify long-term trend and "Golden/Death Crosses". |
| **Trend** | MACD | Trend direction and momentum shifts. |
| **Momentum** | RSI (14) | Identify overbought (>70) or oversold (<30) conditions. |
| **Volatility** | Bollinger Bands | Identify price volatility and potential breakouts. |
| **Volume** | OBV | Confirm price trends with volume flow. |
| **Support/Res** | Fibonacci Retracement | Potential price reversal levels. |

## 3. Fundamental Metrics (Long-Term Health)
These metrics evaluate the underlying business quality and valuation.

| Category | Metric | "Superior" Benchmark |
| :--- | :--- | :--- |
| **Valuation** | P/E Ratio (Trailing/Forward) | Compare vs Industry average and historical mean. |
| **Valuation** | PEG Ratio | Value relative to growth (Ideally < 1.0). |
| **Growth** | Revenue Growth (YoY) | Consistent double-digit growth for growth stocks. |
| **Growth** | EPS Growth | Net income growth consistency. |
| **Profitability**| Net Margin | High margins indicate a competitive moat. |
| **Health** | Debt-to-Equity | Low leverage (< 0.5 preferred). |
| **Health** | Free Cash Flow | Positive and growing FCF. |

## 4. Sentiment Analysis
Real-time pulse of the market's perception.

- **Analyst Consensus:** Average rating (Buy, Hold, Sell) and Price Target vs. Current Price.
- **News Sentiment Score:** Natural Language Processing (NLP) score from recent headlines.
- **Social Media Sentiment:** (Optional/Advanced) Trending status on platforms like X/Twitter or Reddit.
- **Insider Activity:** Net buying/selling by company insiders.

## 5. Decision Logic (The "Superior" Engine)
The tool should calculate a **Composite Score (0-100)**:

- **40% Fundamentals:** Business quality and valuation.
- **40% Technicals:** Timing and trend.
- **20% Sentiment:** Market psychology.

### Recommendation Tiers:
- **Strong Buy (80-100):** Bullish alignment across all three dimensions.
- **Buy (60-79):** Generally positive with some minor weaknesses.
- **Hold (40-59):** Mixed signals or neutral outlook.
- **Sell (20-39):** Bearish alignment or overvaluation/weakening trend.
- **Strong Sell (0-19):** High risk, negative fundamentals and bearish technicals.

## 6. Customizable Filters (User-Defined)
Users can prioritize what matters to them:
- **Dividend Seekers:** Filter for high Yield and low Payout Ratio.
- **Growth Investors:** Focus on Revenue/EPS growth metrics.
- **Value Investors:** Focus on low P/E, P/B, and high FCF.
- **Day Traders:** Focus on high volatility (ATR) and short-term technicals (RSI, VWAP).

## 7. Data Source Mapping (Internal Reference)
*To assist Development Team:*

| Metric Group | Recommended Source | Key API Endpoint/Function |
| :--- | :--- | :--- |
| **Technical Indicators** | Alpha Vantage | `RSI`, `MACD`, `SMA`, `TIME_SERIES_DAILY` |
| **Fundamental Overview** | Alpha Vantage / yfinance | `OVERVIEW` / `ticker.info` |
| **Growth Metrics** | yfinance | `ticker.financials` (Revenue, EPS) |
| **Analyst Ratings** | yfinance | `ticker.recommendations` |
| **News Sentiment** | Alpha Vantage | `NEWS_SENTIMENT` |
| **Insider Activity** | yfinance / SEC Edgar | `ticker.insider_transactions` |
# Scoring Algorithm for US Stock Analysis

This document defines the mathematical logic for the composite "Superior" score.

## 1. Technical Score (T-Score) - 40% Weight
Calculate individual scores (0-100) and average them.

- **Trend Score (50% of T):**
  - Score 100 if Price > 50 SMA > 200 SMA (Bullish alignment).
  - Score 50 if Price > 50 SMA but < 200 SMA.
  - Score 0 if Price < 50 SMA and < 200 SMA.
- **Momentum Score (25% of T):**
  - RSI between 40 and 60: 50 points.
  - RSI between 30 and 40: 75 points (Oversold but recovery potential).
  - RSI < 30: 100 points (Strong Oversold).
  - RSI between 60 and 70: 25 points.
  - RSI > 70: 0 points (Overbought).
- **MACD Score (25% of T):**
  - 100 if MACD Line > Signal Line (Bullish crossover).
  - 0 if MACD Line < Signal Line.

## 2. Fundamental Score (F-Score) - 40% Weight
Each metric contributes 20% to the F-Score.

- **P/E Ratio:** 
  - Score 100 if P/E < Industry Average.
  - Score 50 if P/E within 20% of Industry Average.
  - Score 0 if P/E > 20% above Industry Average.
- **PEG Ratio:**
  - Score 100 if PEG < 1.0.
  - Score 50 if PEG 1.0 - 1.5.
  - Score 0 if PEG > 1.5.
- **Revenue Growth (YoY):**
  - Score 100 if Growth > 15%.
  - Score 50 if Growth 5-15%.
  - Score 0 if Growth < 5%.
- **Net Margin:**
  - Score 100 if Margin > 20%.
  - Score 50 if Margin 10-20%.
  - Score 0 if Margin < 10%.
- **Debt-to-Equity:**
  - Score 100 if D/E < 0.5.
  - Score 50 if D/E 0.5 - 1.0.
  - Score 0 if D/E > 1.0.

## 3. Sentiment Score (S-Score) - 20% Weight
- **Analyst Score (60% of S):**
  - 100 for "Strong Buy" consensus.
  - 75 for "Buy".
  - 50 for "Hold".
  - 25 for "Sell".
  - 0 for "Strong Sell".
- **News Sentiment (40% of S):**
  - Scaled score from NLP analysis (-1.0 to 1.0 mapped to 0 to 100).

## 4. Final Composite Score
`Final Score = (T-Score * 0.4) + (F-Score * 0.4) + (S-Score * 0.2)`

## 5. Logic Adjustments
- If a data point is missing, redistribute its weight within its category.
- If an entire category is missing (e.g., no Sentiment data), redistribute weight to Technicals and Fundamentals (50/50).
# Panic Signal and Vulture Entry Logic

This document defines the logic for identifying extreme market panic and the subsequent "Deep Value" entry points, referred to as the "Vulture Entry."

---

## 1. The Panic Signal (High Alert)
The Panic Signal triggers when a stock experiences irrational or extreme selling pressure. This serves as a "Warning" to standard investors but a "Beacon" for Vulture investors.

### Trigger Criteria (Must meet 3 out of 4)
| Metric | Threshold | Reason |
| :--- | :--- | :--- |
| **Price Velocity** | > 15% drop in 5 trading days | Indicates a break in trend and mass exit. |
| **Institutional Dump**| Relative Volume (RVOL) > 2.5 | Confirms that large blocks are being sold (High conviction selling). |
| **Technical Break** | Price < 200 SMA AND Price < 50 SMA | Major technical support levels have failed. |
| **Sentiment Crash** | News Sentiment moves from >0 to < -0.5 in 72hrs | Significant negative catalyst (Earnings miss, scandal, sector crash). |

---

## 2. The Vulture Entry (Contrarian Opportunity)
The Vulture Entry is only evaluated **after** a Panic Signal has been triggered. It identifies the point of "maximum pessimism" where the risk/reward ratio becomes asymmetric.

### Entry Requirements (Must meet ALL)
| Category | Requirement | "Vulture" Threshold |
| :--- | :--- | :--- |
| **Momentum** | RSI (14) | **< 20** (Extreme Oversold) |
| **Valuation** | Historical P/E Range | **Bottom 5%** of 10-year historical P/E ratio. |
| **Liquidity** | Current Ratio | **> 1.2** (Ensures company can survive the panic). |
| **Solvency** | Altman Z-Score | **> 1.8** (Safe zone, not approaching bankruptcy). |
| **Cash Flow** | FCF Yield | **> 5%** (The company is still a "cash machine"). |
| **Price Action** | Volume Exhaustion | High-volume "Hammer" or "Doji" candle (Indicates bottoming process). |

---

## 3. Vulture Verdict Logic
The "Superior" score is replaced by a **Vulture Confidence Score (0-100)** during this state:

- **60% Financial Floor**: (Z-Score, FCF Yield, Current Ratio).
- **40% Capitulation Intensity**: (RSI, RVOL, Distance from 50 SMA).

### Recommendation Tiers:
- **Vulture Buy (Score 80-100)**: Irrational panic has met a "Fortress" balance sheet. Heavy Contrarian Buy.
- **Speculative Watch (Score 50-79)**: Panic is present, but financial floor is not yet confirmed.
- **Falling Knife (Score < 50)**: Panic is justified by deteriorating financials. **DO NOT ENTER.**

---

## 4. Risk Management (Vulture Exit)
Vulture trades are high-volatility.
- **Stop-Loss**: 10% below Vulture Entry price.
- **Take-Profit**: Reversion to the 50-day SMA or +25% (whichever is higher).
