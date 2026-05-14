# Stock Analysis Report Design Specification

## 1. Overview
The goal is to provide a clean, actionable, and customizable stock analysis report. The report should be available in two formats:
- **Markdown/PDF**: For quick reading and archiving.
- **Web Dashboard**: For interactive exploration.

## 2. Information Architecture

### A. Header & Recommendation (The "Hook")
- **Ticker & Company Name**: Clear identification.
- **Current Price & Daily Change**: Vital stats.
- **AI Recommendation**: Large "BUY", "SELL", or "HOLD" badge.
- **Confidence Score**: 0-100% scale.
- **Timestamp**: When the analysis was generated.

### B. Summary & Thesis
- **Executive Summary**: A 2-3 sentence overview of why this recommendation was made.
- **Key Catalysts**: Bullet points of upcoming events (Earnings, product launches, macro data).

### C. Technical Analysis Dashboard
- **Price Chart**: (Interactive in Web, static in Markdown).
- **Indicators**:
    - RSI (Relative Strength Index)
    - MACD (Moving Average Convergence Divergence)
    - 50-day & 200-day Moving Averages
- **Support & Resistance Levels**: Calculated price floors and ceilings.

### D. Fundamental Health
- **Valuation**: PE Ratio vs. Sector average.
- **Growth**: Revenue and EPS growth trends.
- **Profitability**: Net Margins, ROE.
- **Risk Profile**: Debt-to-Equity, Current Ratio.

### E. Customizable Parameters
Users should be able to toggle "Aggressiveness" or "Strategy Type":
- **Value Investor Mode**: Heavy weighting on fundamentals and PE ratios.
- **Momentum Trader Mode**: Heavy weighting on RSI, MACD, and price trends.
- **Balanced**: A mix of both.

## 3. Visual Language
- **Colors**:
    - Success/Buy: Emerald Green (#10b981)
    - Danger/Sell: Rose Red (#f43f5e)
    - Neutral/Hold: Slate Gray (#64748b)
- **Typography**: Clean sans-serif (Inter or Roboto) for readability.
- **Layout**: Modular cards that can be reordered based on user preference.

## 4. Output Formats

### Web Dashboard Mockup (Draft)
```html
<div class="dashboard">
  <header>
    <h1>AAPL - Apple Inc.</h1>
    <div class="price">$175.40 (+1.2%)</div>
    <div class="signal signal-buy">STRONG BUY (88%)</div>
  </header>
  <section class="grid">
    <div class="card">Technical Signals: Bullish</div>
    <div class="card">Fundamental Health: Strong</div>
    <div class="card">Sentiment: Positive</div>
  </section>
</div>
```

### Markdown Report Template
```markdown
# Stock Analysis: {TICKER}
**Date:** {DATE}
**Signal:** {SIGNAL} ({CONFIDENCE}%)

---

## Executive Summary
{SUMMARY_TEXT}

## Technicals
| Indicator | Value | Status |
|-----------|-------|--------|
| RSI       | 45    | Neutral|
| MACD      | +2.1  | Bullish|

...
```
