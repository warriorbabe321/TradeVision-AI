# Tech Stack and API Choice

## Selected APIs

### 1. Primary: Yahoo Finance (`yfinance`)
- **Reasoning**: Completely free, no API key required for historical data, provides comprehensive data including dividends, splits, and some fundamentals.
- **Role**: Main source for historical price data and basic fundamental metrics.

### 2. Secondary: Alpha Vantage
- **Reasoning**: Robust official API with excellent technical indicator endpoints.
- **Role**: Used for specific technical indicators (SMA, EMA, RSI, etc.) if `yfinance` is insufficient. Requires an API key (free tier available).

### 3. Tertiary: Polygon.io
- **Reasoning**: High-quality institutional-grade data.
- **Role**: Backup for real-time price updates.

## Language and Libraries
- **Language**: Python 3
- **Data Handling**: `pandas`, `numpy`
- **Visualization**: `matplotlib`, `plotly`
- **Configuration**: `python-dotenv`

## Project Structure
The project is located at `/home/team/shared/stock_analysis_project/` and follows a modular design to allow for easy scaling and addition of new data sources or indicators.
