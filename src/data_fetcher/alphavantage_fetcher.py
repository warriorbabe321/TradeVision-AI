import requests
import pandas as pd
from .base import DataFetcher
import os

class AlphaVantageFetcher(DataFetcher):
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("ALPHAVANTAGE_API_KEY")
        self.base_url = "https://www.alphavantage.co/query"

    def get_stock_data(self, ticker: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        # Implementation for Alpha Vantage
        # Note: Alpha Vantage has different endpoints for daily, weekly, etc.
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": ticker,
            "apikey": self.api_key,
            "outputsize": "full"
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()
        # Logic to convert JSON to DataFrame and filter by date
        return pd.DataFrame(data)

    def get_real_time_quote(self, ticker: str) -> dict:
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        data = response.json().get("Global Quote", {})
        return {
            "symbol": data.get("01. symbol"),
            "price": data.get("05. price"),
            "change": data.get("09. change"),
            "change_percent": data.get("10. change percent"),
            "volume": data.get("06. volume"),
        }

    def get_news_sentiment(self, ticker: str) -> float:
        """Fetch news sentiment score using Alpha Vantage."""
        params = {
            "function": "NEWS_SENTIMENT",
            "tickers": ticker,
            "apikey": self.api_key
        }
        try:
            response = requests.get(self.base_url, params=params)
            data = response.json()
            feed = data.get("feed", [])
            if not feed:
                return None
            
            # Average sentiment score for the specific ticker in the news feed
            scores = []
            for item in feed:
                for t_sentiment in item.get("ticker_sentiment", []):
                    if t_sentiment.get("ticker") == ticker:
                        scores.append(float(t_sentiment.get("ticker_sentiment_score", 0)))
            
            return sum(scores) / len(scores) if scores else None
        except Exception:
            return None
