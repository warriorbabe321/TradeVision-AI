# Benchmark Test Scenarios for Stock Scoring Algorithm

This document provides benchmark data and manually calculated "Superior" scores to validate the analysis engine.

---

## Scenario 1: The Rocket (High-Growth Tech)
**Profile:** Bullish alignment, high growth, positive sentiment.
**Target Signal:** Strong Buy (Score > 80)

### 1. Technical Data (T-Score)
*   Trend: Price $150, 50 SMA $140, 200 SMA $120 -> 100 pts
*   Momentum: RSI = 65 -> 25 pts
*   MACD: Bullish Crossover -> 100 pts
*   **T-Score:** (100 * 0.5) + (25 * 0.25) + (100 * 0.25) = **81.25**

### 2. Fundamental Data (F-Score)
*   P/E Ratio: 25 (Industry Avg: 30) -> 100 pts
*   PEG Ratio: 0.8 -> 100 pts
*   Revenue Growth: 25% -> 100 pts
*   Net Margin: 22% -> 100 pts
*   Debt-to-Equity: 0.3 -> 100 pts
*   **F-Score:** (100+100+100+100+100) / 5 = **100**

### 3. Sentiment Data (S-Score)
*   Analyst Rating: Strong Buy -> 100 pts
*   News Sentiment: +0.8 (Very Positive) -> 90 pts
*   **S-Score:** (100 * 0.6) + (90 * 0.4) = **96**

**Composite Score:** (81.25 * 0.4) + (100 * 0.4) + (96 * 0.2) = **91.7 (Strong Buy)**

---

## Scenario 2: The Anchor (Steady Utility)
**Profile:** Stable, low growth, neutral technicals.
**Target Signal:** Hold (Score 40-59)

### 1. Technical Data (T-Score)
*   Trend: Price $55, 50 SMA $52, 200 SMA $50 -> 100 pts
*   Momentum: RSI = 50 -> 50 pts
*   MACD: Bearish Crossover -> 0 pts
*   **T-Score:** (100 * 0.5) + (50 * 0.25) + (0 * 0.25) = **62.5**

### 2. Fundamental Data (F-Score)
*   P/E Ratio: 15 (Industry Avg: 15) -> 100 pts
*   PEG Ratio: 1.6 -> 0 pts
*   Revenue Growth: 4% -> 0 pts
*   Net Margin: 12% -> 50 pts
*   Debt-to-Equity: 0.8 -> 50 pts
*   **F-Score:** (100+0+0+50+50) / 5 = **40**

### 3. Sentiment Data (S-Score)
*   Analyst Rating: Hold -> 50 pts
*   News Sentiment: 0.0 (Neutral) -> 50 pts
*   **S-Score:** (50 * 0.6) + (50 * 0.4) = **50**

**Composite Score:** (62.5 * 0.4) + (40 * 0.4) + (50 * 0.2) = **51 (Hold)**

---

## Scenario 3: The Falling Knife (Distressed Value)
**Profile:** Technical breakdown, negative growth, high debt.
**Target Signal:** Sell (Score 20-39)

### 1. Technical Data (T-Score)
*   Trend: Price $20, 50 SMA $30, 200 SMA $40 -> 0 pts
*   Momentum: RSI = 25 (Oversold) -> 100 pts
*   MACD: Bearish -> 0 pts
*   **T-Score:** (0 * 0.5) + (100 * 0.25) + (0 * 0.25) = **25**

### 2. Fundamental Data (F-Score)
*   P/E Ratio: 5 (Industry Avg: 15) -> 100 pts
*   PEG Ratio: N/A (Negative Earnings) -> Redistribute
*   Revenue Growth: -10% -> 0 pts
*   Net Margin: -5% -> 0 pts
*   Debt-to-Equity: 2.5 -> 0 pts
*   **F-Score:** (100+0+0+0) / 4 = **25**

### 3. Sentiment Data (S-Score)
*   Analyst Rating: Sell -> 25 pts
*   News Sentiment: -0.6 (Negative) -> 20 pts
*   **S-Score:** (25 * 0.6) + (20 * 0.4) = **23**

**Composite Score:** (25 * 0.4) + (25 * 0.4) + (23 * 0.2) = **24.6 (Sell)**

---

## Scenario 4: The Phoenix (Speculative Turnaround)
**Profile:** Improving technicals, weak but stable fundamentals, cautiously optimistic sentiment.
**Target Signal:** Buy/Hold (Score 60-70)

### 1. Technical Data (T-Score)
*   Trend: Price $45, 50 SMA $42, 200 SMA $48 (Price > 50 SMA but < 200 SMA) -> 50 pts
*   Momentum: RSI = 55 -> 50 pts
*   MACD: Bullish Crossover -> 100 pts
*   **T-Score:** (50 * 0.5) + (50 * 0.25) + (100 * 0.25) = **62.5**

### 2. Fundamental Data (F-Score)
*   P/E Ratio: 12 (Industry Avg: 18) -> 100 pts
*   PEG Ratio: 1.2 -> 50 pts
*   Revenue Growth: 6% -> 50 pts
*   Net Margin: 8% -> 0 pts
*   Debt-to-Equity: 0.6 -> 50 pts
*   **F-Score:** (100+50+50+0+50) / 5 = **50**

### 3. Sentiment Data (S-Score)
*   Analyst Rating: Buy -> 75 pts
*   News Sentiment: +0.2 (Slightly Positive) -> 60 pts
*   **S-Score:** (75 * 0.6) + (60 * 0.4) = **69**

**Composite Score:** (62.5 * 0.4) + (50 * 0.4) + (69 * 0.2) = **58.8 (Hold - borderline Buy)**
