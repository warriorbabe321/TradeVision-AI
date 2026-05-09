import subprocess
import json
import datetime

def run_query(sql):
    result = subprocess.run(["team-db", sql], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"DB Error: {result.stderr}")
        return []
    try:
        return json.loads(result.stdout)
    except:
        return []

def log_signal(ticker, price, verdict, hc_score):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Escape single quotes for SQL
    verdict_escaped = verdict.replace("'", "''")
    sql = f"INSERT INTO signals (ticker, timestamp, price, verdict, hc_score, status) VALUES ('{ticker}', '{timestamp}', {price}, '{verdict_escaped}', {hc_score}, 'Open')"
    run_query(sql)

def get_signals():
    return run_query("SELECT * FROM signals ORDER BY timestamp DESC")

def update_signal_status(signal_id, status, exit_price):
    sql = f"UPDATE signals SET status = '{status}', exit_price = {exit_price} WHERE id = {signal_id}"
    run_query(sql)
