# TradeVision AI - Project Summary

## 1. Project Goal
Create a "Superior" US Stock Analysis platform tailored for a **Small Retailer** profile, prioritizing **Sure-Win** trades with institutional-grade data and logic.

## 2. Core Accomplishments
*   **The Command Center**: A live Flask-based web application (running on Port 5000) with a professional "Hedge Fund Terminal" look.
*   **Retailer Gold / Sure-Win Mode**: An extremely picky backend logic that only triggers a "SURE-WIN" verdict for stocks with:
    *   Net Margin > 25% (Financial Moat).
    *   Institutional Ownership > 70% (Big Money backing).
    *   Debt-to-Equity < 0.5 (Fortress Balance Sheet).
    *   Confirmed Technical Uptrend (Above 200 SMA).
*   **4-Level Decision Hierarchy**:
    1.  **Research Desk**: Multi-parameter data gathering.
    2.  **The Debate**: Dynamic Bullish vs. Bearish case arguments.
    3.  **Risk Management**: Automated No-Go filters and Stop-Loss calculations.
    4.  **Fund Manager Verdict**: Final execution plan (Entry, Target, Stop).
*   **Market Pulse**: Real-time ticker header for SPY, QQQ, and DIA.

## 3. Technical Stack (Free-First Strategy)
*   **Backend**: Python, Flask, Pandas.
*   **Data Source**: `yfinance` (Always Free) for prices, fundamentals, and ownership.
*   **Hosting Target**: Free Tiers (Railway, Render, or Vercel).
*   **Caching & Optimization (Free-First)**:
    *   **Market Pulse**: 15-minute in-memory cache to prevent frequent index fetching.
    *   **Reports**: 4-hour on-disk cache for generated reports.
    *   **Safety Scanner**: 1-hour in-memory cache for batch fundamental scans.

*   **Performance Tracker**:
    *   Automated logging of all high-conviction signals.
    *   Manual trade settlement to track Win/Loss ratio.
    *   Real-time Success Rate calculation.

## 4. Key Files & Folders
*   `/home/team/shared/stock_analysis_app/`: Main web application code.
*   `/home/team/shared/stock_analysis_project/`: The "Brain" (Scoring Engine & Report Generator).
*   `/home/team/shared/retailer_high_conviction_logic.md`: The "Sure-Win" math.
*   `/home/team/shared/hedge_fund_hierarchy.md`: The 4-level decision hierarchy logic.

## 5. Instructions for Resuming
To restart the project or add new features:
1.  Navigate to `/home/team/shared/stock_analysis_app/`.
2.  Run `python3 app.py` to start the dashboard on Port 5000.
3.  Check `shared/hedge_fund_hierarchy.md` to understand the current decision flow.
4.  Direct the Software Engineer to add new UI components or the Financial Analyst to update the math.

## 6. Future Roadmap
*   **Insider Edge Cluster**: Tracking clusters of buying between CEOs, CFOs, and Politicians.
*   **Huge Sell-Off Alert (Panic Signal)**: A high-priority alert that triggers only during massive, abnormal sell-offs (detecting spikes in volume + >3% intraday drops).
*   **Simple Password Protection**: For sharing with friends securely.
*   **Portfolio Tracking**: Real-time scoring of your current holdings.
*   **Mobile Optimization**: Adapting the dashboard for better phone use.
