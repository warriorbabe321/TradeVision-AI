from src.data_fetcher.yfinance_fetcher import YFinanceFetcher
from dotenv import load_dotenv
import os

def main():
    load_dotenv()
    
    # Initialize fetcher
    fetcher = YFinanceFetcher()
    
    # Test ticker
    ticker = "AAPL"
    
    print(f"Fetching data for {ticker}...")
    try:
        # Fetch historical data
        data = fetcher.get_stock_data(ticker, period="5d")
        print("\nHistorical Data (Last 5 days):")
        print(data.tail())
        
        # Fetch real-time quote
        quote = fetcher.get_real_time_quote(ticker)
        print(f"\nReal-time Quote for {ticker}:")
        for key, value in quote.items():
            print(f"{key}: {value}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
