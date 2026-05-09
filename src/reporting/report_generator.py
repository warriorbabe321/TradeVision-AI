import json
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def prepare_template_data(raw_data):
    """
    Maps engine output (CamelCase) to template expectations (snake_case)
    and performs additional formatting.
    """
    # Base mapping
    data = {
        "ticker": raw_data.get("Ticker"),
        "company_name": raw_data.get("Company"),
        "current_price": raw_data.get("CurrentPrice"),
        "daily_change": raw_data.get("DailyChange"),
        "signal": raw_data.get("Signal"),
        "confidence": int(raw_data.get("Confidence", 0) * 100),
        "thesis": raw_data.get("Thesis"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Calculate Daily Change Percent
    if data["current_price"] and data["daily_change"]:
        prev_price = data["current_price"] - data["daily_change"]
        if prev_price != 0:
            data["daily_change_percent"] = round((data["daily_change"] / prev_price) * 100, 2)
        else:
            data["daily_change_percent"] = 0
    else:
        data["daily_change_percent"] = 0

    # Map Technicals
    data["technicals"] = {
        "rsi": {
            "value": raw_data.get("RSI"),
            "status": "Bearish (Overbought)" if raw_data.get("RSI", 50) > 70 else ("Bullish (Oversold)" if raw_data.get("RSI", 50) < 30 else "Neutral")
        },
        "macd": {
            "value": raw_data.get("MACD"),
            "status": "Bullish" if raw_data.get("MACD", 0) > 0 else "Bearish"
        },
        "bb_upper": {
            "value": raw_data.get("BollingerBands", {}).get("Upper"),
            "status": "N/A"
        },
        "bb_lower": {
            "value": raw_data.get("BollingerBands", {}).get("Lower"),
            "status": "N/A"
        },
        "atr": {
            "value": raw_data.get("ATR"),
            "status": "N/A"
        },
        "vwap": {
            "value": raw_data.get("VWAP"),
            "status": "N/A"
        },
        "obv": {
            "value": raw_data.get("OBV"),
            "status": "N/A"
        }
    }

    # Map Fundamentals
    data["fundamentals"] = {
        "pe_ratio": f"{raw_data.get('PE_Ratio')}x" if raw_data.get("PE_Ratio") else "N/A",
        "revenue_growth": raw_data.get("RevenueGrowth", "N/A"),
        "net_margin": raw_data.get("NetMargin", "N/A"),
        "top_holders": raw_data.get("TopHolders", [])
    }
    
    # NEW: Hedge Fund Hierarchy & Sure-Win Data
    data["debate"] = raw_data.get("Debate")
    data["risk_mgmt"] = raw_data.get("RiskMgmt")
    data["hc_data"] = raw_data.get("HighConviction")
    data["execution"] = raw_data.get("ExecutionPlan")
    data["integrity"] = raw_data.get("DataIntegrity")
    data["chart_data"] = raw_data.get("ChartData", [])
    data["insider"] = raw_data.get("InsiderActivity", {"Score": 50, "Status": "N/A"})
    data["elite_signals"] = raw_data.get("EliteSignals")

    # Risks (Engine doesn't provide these yet, using generic ones or empty)
    data["risks"] = raw_data.get("RiskMgmt", {}).get("reasons") or raw_data.get("Risks", ["Market Volatility", "Macroeconomic factors"])

    return data

def generate_reports(analysis_data_path, output_dir):
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Load analysis data
    with open(analysis_data_path, 'r') as f:
        raw_data = json.load(f)
    
    # Prepare data for template
    template_data = prepare_template_data(raw_data)

    # Setup Jinja2 environment
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))

    # Generate Markdown Report
    md_template = env.get_template('report_template.md')
    md_output = md_template.render(**template_data)
    md_file_path = os.path.join(output_dir, f"{template_data['ticker']}_report.md")
    with open(md_file_path, 'w') as f:
        f.write(md_output)
    print(f"Markdown report generated: {md_file_path}")

    # Generate HTML Report
    html_template = env.get_template('report_template.html')
    html_output = html_template.render(**template_data)
    html_file_path = os.path.join(output_dir, f"{template_data['ticker']}_report.html")
    with open(html_file_path, 'w') as f:
        f.write(html_output)
    print(f"HTML report generated: {html_file_path}")

if __name__ == "__main__":
    # Path to the mock analysis data (now matching engine format)
    mock_data_path = "os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "mock_analysis.json")"
    
    # Path to save generated reports
    shared_reports_dir = "os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "reports")"
    
    generate_reports(mock_data_path, shared_reports_dir)
