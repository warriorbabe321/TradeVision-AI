from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import os
import subprocess
import sys
import json
import time
from functools import wraps

# Add project root to sys.path to import fetcher
# Team Lead: Checked commit ability.
PROJECT_DIR = os.path.dirname(__file__)
sys.path.append(PROJECT_DIR)
from src.data_fetcher.yfinance_fetcher import YFinanceFetcher
from src.utils.db_utils import log_signal, get_signals, update_signal_status, run_query
from src.analysis.scoring_engine import ScoringEngine

app = Flask(__name__)
app.secret_key = "tradevision-ultra-secure-key-2026"

# Paths
REPORTS_DIR = os.path.join(os.path.dirname(__file__), "final_reports")
ACCESS_KEYS_FILE = os.path.join(os.path.dirname(__file__), "access_keys.json")

if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

# Rate limiting tracking
# { key: { "timestamps": [t1, t2...], "blocked_until": timestamp } }
rate_limit_cache = {}

def get_allowed_keys():
    try:
        if os.path.exists(ACCESS_KEYS_FILE):
            with open(ACCESS_KEYS_FILE, 'r') as f:
                data = json.load(f)
                return data.get("keys", [])
    except:
        pass
    return []

def is_rate_limited(key):
    now = time.time()
    if key not in rate_limit_cache:
        rate_limit_cache[key] = {"timestamps": [], "blocked_until": 0}
    
    cache = rate_limit_cache[key]
    
    # Check if currently blocked
    if cache["blocked_until"] > now:
        return True, int((cache["blocked_until"] - now) / 60)
    
    # Clean up old timestamps (older than 5 mins)
    cache["timestamps"] = [t for t in cache["timestamps"] if now - t < 300]
    
    # Check if threshold reached (20 searches in 5 mins)
    if len(cache["timestamps"]) >= 20:
        cache["blocked_until"] = now + 3600 # Block for 1 hour
        return True, 60
        
    return False, 0

def require_access_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_key' not in session:
            return redirect(url_for('login'))
        
        # Immediate lockout if key is deleted
        allowed_keys = get_allowed_keys()
        if session['access_key'] not in allowed_keys:
            session.pop('access_key', None)
            return redirect(url_for('login', error="Key revoked or invalid."))
            
        return f(*args, **kwargs)
    return decorated_function

# Simple in-memory cache for market pulse
pulse_cache = {
    "data": [],
    "timestamp": 0
}

def get_market_pulse():
    now = time.time()
    if pulse_cache["data"] and (now - pulse_cache["timestamp"] < 900): # 15 min cache
        return pulse_cache["data"]

    fetcher = YFinanceFetcher()
    pulse = []
    for ticker in ["SPY", "QQQ", "DIA"]:
        try:
            quote = fetcher.get_real_time_quote(ticker)
            price = quote.get("price")
            change_pct = quote.get("change_percent")
            
            pulse.append({
                "ticker": ticker,
                "price": round(price, 2) if price is not None else "N/A",
                "percent": round(change_pct * 100, 2) if change_pct is not None else 0.0
            })
        except:
            pulse.append({"ticker": ticker, "price": "N/A", "percent": 0.0})
    
    pulse_cache["data"] = pulse
    pulse_cache["timestamp"] = now
    return pulse

def get_system_health():
    # 1. API Status (yfinance)
    # We check if we have any data in pulse_cache that is relatively fresh
    api_status = "Operational"
    now = time.time()
    if not pulse_cache["data"]:
        # Try a quick fetch if cache is empty
        try:
            fetcher = YFinanceFetcher()
            quote = fetcher.get_real_time_quote("SPY")
            if not quote or quote.get("price") is None:
                api_status = "Issues Detected"
        except:
            api_status = "Down"
    elif (now - pulse_cache["timestamp"] > 1800): # More than 30 mins old
        api_status = "Delayed"

    # 2. Data Freshness
    last_updated = "Never"
    if pulse_cache["timestamp"] > 0:
        last_updated = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(pulse_cache["timestamp"]))

    return {
        "status": api_status,
        "last_updated": last_updated,
        "color": "emerald" if api_status == "Operational" else ("rose" if api_status == "Down" else "amber")
    }

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        key = request.form.get("access_key")
        allowed_keys = get_allowed_keys()
        if key in allowed_keys:
            session['access_key'] = key
            return redirect(url_for('index'))
        else:
            return render_template("login.html", error="Invalid Access Key")
    
    error = request.args.get("error")
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop('access_key', None)
    return redirect(url_for('login'))

@app.route("/")
@require_access_key
def index():
    # List existing reports
    reports = []
    if os.path.exists(REPORTS_DIR):
        for f in os.listdir(REPORTS_DIR):
            if f.endswith("_report.html"):
                ticker = f.split("_")[0]
                reports.append({"ticker": ticker, "filename": f})
    
    pulse = get_market_pulse()
    health = get_system_health()
    return render_template("index.html", reports=reports, pulse=pulse, health=health)

@app.route("/analyze", methods=["POST"])
@require_access_key
def analyze():
    key = session.get('access_key')
    limited, minutes = is_rate_limited(key)
    if limited:
        return f"Rate limit exceeded. Access Key '{key}' is blocked for {minutes} more minutes due to high search volume.", 429
    
    # Record this search for rate limiting
    if key in rate_limit_cache:
        rate_limit_cache[key]["timestamps"].append(time.time())

    ticker = request.form.get("ticker", "").upper().strip()
    risk = request.form.get("risk", "Standard")
    # Map 'Sure-Win' from UI to 'Retailer High-Conviction' for backend
    if risk == "Sure-Win":
        risk = "Retailer High-Conviction"
    horizon = request.form.get("horizon", "Short Term")
    
    if not ticker:
        return redirect(url_for("index"))

    report_filename = f"{ticker}_report.html"
    report_path = os.path.join(REPORTS_DIR, report_filename)

    # Basic Caching: If report exists and is < 4 hours old, reuse it
    if os.path.exists(report_path):
        mtime = os.path.getmtime(report_path)
        if (time.time() - mtime) < 14400: # 4 hours
            return redirect(f"/reports/{report_filename}")
    
    # Trigger the existing script
    cmd = [sys.executable, "generate_final_report.py", ticker, "--risk", risk, "--horizon", horizon]
    
    try:
        # Run the analysis script
        process = subprocess.run(cmd, cwd=PROJECT_DIR, capture_output=True, text=True)
        
        if process.returncode == 0:
            # The script saves the report to /home/team/shared/final_reports/{ticker}_report.html
            report_filename = f"{ticker}_report.html"
            return redirect(f"/reports/{report_filename}")
        else:
            return f"Error analyzing ticker {ticker}: {process.stderr}", 500
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}", 500

# Simple in-memory cache for safety scanner
scanner_cache = {
    "data": [],
    "timestamp": 0
}

@app.route("/safety_scanner")
@require_access_key
def safety_scanner():
    now = time.time()
    if scanner_cache["data"] and (now - scanner_cache["timestamp"] < 3600): # 1 hour cache
        return render_template("scanner.html", stocks=scanner_cache["data"])

    fetcher = YFinanceFetcher()
    # A small subset of stocks to scan
    candidates = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "BRK-B", "V", "MA", "JNJ", "PG", "KO", "PEP", "XOM", "CVX", "WMT", "COST", "HD"]
    safe_stocks = []
    
    for ticker in candidates:
        try:
            funds = fetcher.get_fundamentals(ticker)
            
            # Hard Criteria (Pass/Fail) as per risk_time_logic.md
            de = funds.get("debt_to_equity") # e.g. 140.96 for 1.40
            fcf = funds.get("free_cash_flow")
            margin = funds.get("net_margin") # e.g. 0.25 for 25%
            beta = funds.get("beta")
            cr = funds.get("current_ratio")
            
            # Use thresholds from logic doc (interpreting 0.3 as 30 for D/E if yfinance uses percent)
            # Actually, let's be careful. If de is 140, and threshold is 0.3, it fails.
            # If de is 20, and threshold is 0.3 (meaning 30%), it passes.
            
            is_safe = True
            if de is None or de > 30: is_safe = False
            if fcf is None or fcf <= 0: is_safe = False
            if margin is None or margin < 0.10: is_safe = False
            if beta is None or beta >= 1.0: is_safe = False
            if cr is None or cr < 1.2: is_safe = False
            
            # Safety Score (0-100)
            score = 0
            if de is not None and de < 30: score += 25
            if fcf is not None and fcf > 0: score += 25
            if margin is not None and margin > 0.15: score += 20
            if beta is not None and beta < 0.8: score += 15
            if cr is not None and cr > 1.5: score += 15
            
            if is_safe or score >= 70: # Show stocks that are either "Hard Safe" or have high score
                quote = fetcher.get_real_time_quote(ticker)
                price = quote.get("price", 0)
                safe_stocks.append({
                    "ticker": ticker,
                    "price": price,
                    "score": score,
                    "de": round(de, 2) if de else "N/A",
                    "margin": round(margin * 100, 2) if margin else "N/A",
                    "beta": round(beta, 2) if beta else "N/A",
                    "status": "Retail Gold" if score >= 85 else "Safe Haven"
                })
        except:
            continue
    
    # Sort by score descending and take top 10
    safe_stocks = sorted(safe_stocks, key=lambda x: x["score"], reverse=True)[:10]
    
    # Log Retail Gold signals found in scanner
    for s in safe_stocks:
        if s['status'] == 'Retail Gold' and s['score'] >= 90:
             try:
                 log_signal(s['ticker'], s.get('price', 0), "RETAIL GOLD (Scanner)", s['score'])
             except:
                 pass

    scanner_cache["data"] = safe_stocks
    scanner_cache["timestamp"] = now
    
    health = get_system_health()
    return render_template("scanner.html", stocks=safe_stocks, health=health)

@app.route("/trade_history")
@require_access_key
def trade_history():
    signals = get_signals()
    
    # Calculate success rate
    closed_signals = [s for s in signals if s['status'] == 'Closed']
    wins = 0
    for s in closed_signals:
        if s['exit_price'] and s['exit_price'] > s['price']:
            wins += 1
    
    success_rate = (wins / len(closed_signals) * 100) if closed_signals else 0
    health = get_system_health()
    return render_template("performance.html", signals=signals, success_rate=round(success_rate, 2), health=health)

@app.route("/performance")
def performance_alias():
    return redirect(url_for("trade_history"))

@app.route("/update_signal", methods=["POST"])
def update_signal():
    signal_id = request.form.get("id")
    exit_price = request.form.get("exit_price")
    if signal_id and exit_price:
        update_signal_status(signal_id, "Closed", float(exit_price))
    return redirect(url_for("performance"))

@app.route("/reports/<path:filename>")
@require_access_key
def serve_report(filename):
    return send_from_directory(REPORTS_DIR, filename)

if __name__ == "__main__":
    # Bind to 0.0.0.0 to expose the service
    app.run(host="0.0.0.0", port=5000, debug=True)
