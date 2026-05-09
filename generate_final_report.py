import sys
import os
import json
import argparse

# Add the project root and src directory to the path so we can import our modules
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_root)

try:
    from analyze_stock import analyze_stock
    from src.reporting.report_generator import generate_reports
except ImportError as e:
    print(f"Error: Could not import required modules. {e}")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Generate final stock analysis report.')
    parser.add_argument('ticker', help='The stock ticker to analyze (e.g., AAPL)')
    parser.add_argument('--risk', default='Standard', choices=['Standard', 'Conservative', 'Retailer High-Conviction'], help='Risk level')
    parser.add_argument('--horizon', default='Short Term', choices=['Day Trade', 'Short Term', 'Long Term'], help='Time horizon')
    args = parser.parse_args()

    ticker = args.ticker.upper()
    output_dir = os.path.join(os.path.dirname(__file__), "final_reports")
    temp_json_path = f"/tmp/{ticker}_analysis.json"

    try:
        # 1. Run Analysis
        analysis_result = analyze_stock(ticker, risk_level=args.risk, horizon=args.horizon)
        
        if not analysis_result:
            print(f"Error: Analysis failed for ticker {ticker}. Please check if the ticker is valid or if API limits were reached.")
            sys.exit(1)

        # 2. Save JSON temporarily for report_generator
        # report_generator.generate_reports currently expects a file path.
        with open(temp_json_path, 'w') as f:
            json.dump(analysis_result, f, indent=2)

        # 3. Generate Reports
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        generate_reports(temp_json_path, output_dir)

        print(f"\nSUCCESS: Final reports for {ticker} have been generated in: {output_dir}")

        # Cleanup temp file
        if os.path.exists(temp_json_path):
            os.remove(temp_json_path)

    except Exception as e:
        print(f"An unexpected error occurred during the integration process: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
