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
