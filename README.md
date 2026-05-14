# TradeVision AI - Portable Source Code v4

This folder contains the complete, verified, and portable source code for the TradeVision AI stock analysis terminal. It is designed to be a complete hand-off package for a new engineering team.

## Folder Structure
- `app.py`: The central Flask web server and routing engine.
- `src/`: Core Python library containing data fetchers, indicators, scoring logic, and database utilities.
- `templates/`: Jinja2 HTML templates for the web interface.
- `documentation/`: Full logical specifications, strategy docs, and design requirements.
- `final_reports/`: Pre-rendered analysis reports for reference and instant viewing.
- `access_keys.json`: Gatekeeper security configuration.
- `requirements.txt`: Python dependency list.
- `PROJECT_SUMMARY.md`: High-level architectural overview.

## Core Intelligence Logic
- **Perfect Alignment**: (Price > 20 SMA > 50 SMA > 200 SMA) is the hard filter for Retailer Gold signals.
- **Safety Scanner**: Weighted scoring (0-100) based on D/E, FCF, Net Margins, Beta, and Current Ratio.
- **Elite Clusters**: Integration of insider and politician transaction data (mocked in the current data model for demonstration).

## Technical Requirements
- Python 3.10+
- Dependencies: `pip install -r requirements.txt`
- Database: The system uses a `team-db` CLI for logging signals. A new team should ensure they have a compatible SQL database interface or modify `src/utils/db_utils.py` to use a local SQLite file.

## How to Start the App
1. Navigate to this directory.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the server: `python3 app.py`.
4. Access via browser on `http://localhost:5000`.
5. Login using keys in `access_keys.json`.

## Notes for Hand-over
- The application has been modified to use relative paths for the `src` module, making it fully portable.
- All technical indicator panes (MACD, RSI, etc.) are synchronized using `LightweightCharts`.
- The UI is built with Tailwind CSS (CDN-based) for instant responsiveness.
