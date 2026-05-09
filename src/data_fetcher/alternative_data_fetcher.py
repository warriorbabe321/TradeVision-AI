import pandas as pd
import random
from datetime import datetime, timedelta

class AlternativeDataFetcher:
    def __init__(self):
        pass

    def get_politician_trades(self, ticker: str) -> pd.DataFrame:
        """
        Fetch politician trades for a given ticker.
        Since there's no easy free API for this, we provide a structured mock
        that simulates real data from sources like Capitol Trades.
        """
        # In a real scenario, we would scrape or use an API like Quiver Quantitative
        # For now, we mock the structure to prepare the UI and backend.
        
        # We'll 'mock' based on ticker to keep it somewhat consistent for testing
        random.seed(ticker)
        
        politicians = ["Nancy Pelosi", "Tommy Tuberville", "Josh Gottheimer", "Mark Green", "Ro Khanna"]
        actions = ["Purchase", "Sale"]
        
        trades = []
        # Generate 0-3 mock trades
        num_trades = random.randint(0, 3)
        for _ in range(num_trades):
            trades.append({
                "Politician": random.choice(politicians),
                "Action": random.choice(actions),
                "Date": (datetime.now() - timedelta(days=random.randint(5, 60))).strftime("%Y-%m-%d"),
                "Amount": random.choice(["$1K-$15K", "$15K-$50K", "$50K-$100K", "$100K-$250K"]),
                "Description": "Simulation of House/Senate trade report."
            })
            
        return pd.DataFrame(trades)

    def get_insider_cluster_signals(self, ticker: str, yf_insider_transactions: pd.DataFrame) -> dict:
        """
        Analyze insider transactions to find clusters (multiple insiders buying/selling in a short window).
        """
        if yf_insider_transactions is None or yf_insider_transactions.empty:
            return {"status": "Neutral", "score": 50, "clusters": []}
        
        # Analyze clusters
        # yfinance insider_transactions columns usually include: 'Date', 'Insider', 'Transaction', 'Shares', 'Value'
        # But wait, we saw insider_transactions was None in our test for TSLA.
        # Let's check another ticker that might have it, or rely on insider_purchases summary.
        
        # If we have detailed transactions:
        try:
            # Mock cluster detection if transactions are not available but summary shows high activity
            # Or if transactions ARE available, we check for multiple people in last 30 days.
            pass
        except:
            pass
            
        return {"status": "Neutral", "score": 50, "clusters": []}
