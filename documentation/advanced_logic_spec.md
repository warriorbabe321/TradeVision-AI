# Logic for Risk, Time-Horizon, and Safety Scanner

This document extends the core scoring algorithm to support custom user configurations for Risk Profile and Time-Horizon, as well as a standalone Safety Scanner.

---

## 1. Risk Profile Logic

Users can choose between a **Standard/Growth** (Default) or **Conservative/Safety** profile.

### Conservative/Safety Profile
This profile prioritizes financial stability and profitability over aggressive growth and technical momentum.

**Composite Weight:**
`Final Score = (T-Score * 0.2) + (F-Score * 0.6) + (S-Score * 0.2)`

**F-Score Metric Weights (Redistributed):**
| Metric | Weight | Reason |
| :--- | :--- | :--- |
| Debt-to-Equity | 30% | Prioritize low leverage. |
| Net Margin | 30% | Ensure consistent profitability. |
| P/E Ratio | 20% | Favor reasonable valuation. |
| Revenue Growth | 10% | Growth is secondary to stability. |
| PEG Ratio | 10% | Secondary valuation check. |

---

## 2. Time-Horizon Logic

Users can choose between **Long-Term** (Default) or **Day Trade**.

### Day Trade Profile
This profile prioritizes price action and technical momentum for short-term opportunities.

**Composite Weight:**
`Final Score = (T-Score * 0.7) + (F-Score * 0.1) + (S-Score * 0.2)`

**T-Score Metric Weights (Redistributed):**
| Metric | Weight | Reason |
| :--- | :--- | :--- |
| Momentum (RSI) | 40% | Critical for identifying overbought/oversold. |
| MACD | 40% | Primary signal for entry/exit timing. |
| Trend (SMA) | 20% | General direction check. |

*Note: For Day Trade, Technical indicators should ideally use shorter timeframes (e.g., 5-min, 15-min) if supported by the API, otherwise daily signals are used as the fallback.*

---

## 3. Safety Scanner Criteria

The **Safety Scanner** is a specialized filter designed to find "Safe Haven" stocks. A stock must meet **all** the following "Hard" criteria to pass the scanner, or be ranked by a **Safety Score**.

### Hard Criteria (Pass/Fail)
| Criterion | Threshold | Reason |
| :--- | :--- | :--- |
| Debt-to-Equity | < 0.3 | Extremely low bankruptcy risk. |
| Free Cash Flow | > 0 | Company is self-sustaining. |
| Net Margin | > 10% | Healthy profit cushion. |
| Beta | < 1.0 | Lower volatility than the S&P 500. |
| Current Ratio | > 1.2 | Strong short-term liquidity. |

### Safety Score (0-100)
For the UI "Safety Gauge", calculate a score based on these metrics:
- 25 pts: D/E < 0.3
- 25 pts: Positive FCF
- 20 pts: Net Margin > 15%
- 15 pts: Beta < 0.8
- 15 pts: Current Ratio > 1.5
