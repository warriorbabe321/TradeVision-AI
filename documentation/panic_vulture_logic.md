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
