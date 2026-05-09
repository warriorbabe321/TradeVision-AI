from abc import ABC, abstractmethod
import pandas as pd

class DataFetcher(ABC):
    @abstractmethod
    def get_stock_data(self, ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Fetch historical stock data."""
        pass

    @abstractmethod
    def get_real_time_quote(self, ticker: str) -> dict:
        """Fetch real-time stock quote."""
        pass
