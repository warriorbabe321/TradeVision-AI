# Validation Test Scenarios for Stock Scoring Algorithm

This document outlines three test scenarios representing different stock profiles to validate the "Superior" scoring algorithm.

---

## Scenario 1: The Rocket (High-Growth Tech)
**Profile:** A leading tech company with strong momentum, high growth, and bullish market sentiment.
**Target Signal:** Strong Buy (Score > 80)

### 1. Technical Data (T-Score)
*   **Trend:** Price $150, 50 SMA $140, 200 SMA $120 (Price > 50 SMA > 200 SMA) -> **100 pts**
*   **Momentum:** RSI = 65 -> **25 pts**
*   **MACD:** MACD Line > Signal Line -> **100 pts**
*   **T-Score Calculation:** `(100 * 0.5) + (25 * 0.25) + (100 * 0.25)` = **81.25**

### 2. Fundamental Data (F-Score)
*   **P/E Ratio:** 25 (Industry Avg: 30) -> **100 pts**
*   **PEG Ratio:** 0.8 -> **100 pts**
*   **Revenue Growth (YoY):** 25% -> **100 pts**
*   **Net Margin:** 22% -> **100 pts**
*   **Debt-to-Equity:** 0.3 -> **100 pts**
*   **F-Score Calculation:** `(100+100+100+100+100) / 5` = **100**

### 3. Sentiment Data (S-Score)
*   **Analyst Rating:** Strong Buy -> **100 pts**
*   **News Sentiment:** +0.8 (Very Positive) -> **90 pts** (Scaled: `(0.8+1)*50`)
*   **S-Score Calculation:** `(100 * 0.6) + (90 * 0.4)` = **96**

### **Expected Final Score:** 
`(81.25 * 0.4) + (100 * 0.4) + (96 * 0.2)` = **91.7 (Strong Buy)**

---

## Scenario 2: The Anchor (Steady Utility)
**Profile:** A stable utility company with moderate growth, solid dividends, and neutral technicals.
**Target Signal:** Hold (Score 40-59)

### 1. Technical Data (T-Score)
*   **Trend:** Price $55, 50 SMA $52, 200 SMA $50 (Price > 50 SMA > 200 SMA) -> **100 pts**
*   **Momentum:** RSI = 50 -> **50 pts**
*   **MACD:** MACD Line < Signal Line -> **0 pts**
*   **T-Score Calculation:** `(100 * 0.5) + (50 * 0.25) + (0 * 0.25)` = **62.5**

### 2. Fundamental Data (F-Score)
*   **P/E Ratio:** 15 (Industry Avg: 15) -> **100 pts** (Actually exactly industry, let's say 100 for being fair/cheap)
*   **PEG Ratio:** 1.6 -> **0 pts**
*   **Revenue Growth (YoY):** 4% -> **0 pts**
*   **Net Margin:** 12% -> **50 pts**
*   **Debt-to-Equity:** 0.8 -> **50 pts**
*   **F-Score Calculation:** `(100+0+0+50+50) / 5` = **40**

### 3. Sentiment Data (S-Score)
*   **Analyst Rating:** Hold -> **50 pts**
*   **News Sentiment:** 0.0 (Neutral) -> **50 pts**
*   **S-Score Calculation:** `(50 * 0.6) + (50 * 0.4)` = **50**

### **Expected Final Score:** 
`(62.5 * 0.4) + (40 * 0.4) + (50 * 0.2)` = **51 (Hold)**

---

## Scenario 3: The Falling Knife (Distressed Value)
**Profile:** A former giant facing structural decline, high debt, and negative market sentiment.
**Target Signal:** Sell (Score 20-39)

### 1. Technical Data (T-Score)
*   **Trend:** Price $20, 50 SMA $30, 200 SMA $40 (Price < 50 SMA < 200 SMA) -> **0 pts**
*   **Momentum:** RSI = 25 (Oversold) -> **100 pts**
*   **MACD:** MACD Line < Signal Line -> **0 pts**
*   **T-Score Calculation:** `(0 * 0.5) + (100 * 0.25) + (0 * 0.25)` = **25**

### 2. Fundamental Data (F-Score)
*   **P/E Ratio:** 5 (Industry Avg: 15) -> **100 pts** (Deep value)
*   **PEG Ratio:** N/A (Negative Earnings) -> **Weight Redistributed**
*   **Revenue Growth (YoY):** -10% -> **0 pts**
*   **Net Margin:** -5% -> **0 pts**
*   **Debt-to-Equity:** 2.5 -> **0 pts**
*   **F-Score Calculation:** `(100+0+0+0) / 4` = **25**

### 3. Sentiment Data (S-Score)
*   **Analyst Rating:** Sell -> **25 pts**
*   **News Sentiment:** -0.6 (Negative) -> **20 pts** (Scaled: `(-0.6+1)*50`)
*   **S-Score Calculation:** `(25 * 0.6) + (20 * 0.4)` = **23**

### **Expected Final Score:** 
`(25 * 0.4) + (25 * 0.4) + (23 * 0.2)` = **24.6 (Sell)**
