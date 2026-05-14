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
