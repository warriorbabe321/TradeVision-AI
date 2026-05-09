import pandas as pd
import numpy as np

def calculate_sma(df: pd.DataFrame, window: int) -> pd.Series:
    return df['Close'].rolling(window=window).mean()

def calculate_rsi(df: pd.DataFrame, window: int = 14) -> pd.Series:
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(df: pd.DataFrame, slow: int = 26, fast: int = 12, signal: int = 9):
    exp1 = df['Close'].ewm(span=fast, adjust=False).mean()
    exp2 = df['Close'].ewm(span=slow, adjust=False).mean()
    macd_line = exp1 - exp2
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    return macd_line, signal_line

def calculate_bollinger_bands(df: pd.DataFrame, window: int = 20, num_std: int = 2):
    sma = df['Close'].rolling(window=window).mean()
    std = df['Close'].rolling(window=window).std()
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    return upper_band, sma, lower_band

def calculate_atr(df: pd.DataFrame, window: int = 14):
    high_low = df['High'] - df['Low']
    high_close = np.abs(df['High'] - df['Close'].shift())
    low_close = np.abs(df['Low'] - df['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(window=window).mean()
    return atr

def calculate_vwap(df: pd.DataFrame):
    v = df['Volume'].values
    tp = (df['Low'] + df['High'] + df['Close']).values / 3
    return pd.Series((tp * v).cumsum() / v.cumsum(), index=df.index)

def calculate_mfi(df: pd.DataFrame, window: int = 14) -> pd.Series:
    """Calculate Money Flow Index (MFI)."""
    typical_price = (df['High'] + df['Low'] + df['Close']) / 3
    money_flow = typical_price * df['Volume']
    
    positive_flow = pd.Series(0.0, index=df.index)
    negative_flow = pd.Series(0.0, index=df.index)
    
    price_diff = typical_price.diff()
    
    positive_flow[price_diff > 0] = money_flow[price_diff > 0]
    negative_flow[price_diff < 0] = money_flow[price_diff < 0]
    
    pos_mf_sum = positive_flow.rolling(window=window).sum()
    neg_mf_sum = negative_flow.rolling(window=window).sum()
    
    mfr = pos_mf_sum / neg_mf_sum
    mfi = 100 - (100 / (1 + mfr))
    return mfi

def calculate_obv(df: pd.DataFrame):
    obv = (np.sign(df['Close'].diff()) * df['Volume']).fillna(0).cumsum()
    return obv

def calculate_rvol(df: pd.DataFrame, window: int = 20):
    """Calculate Relative Volume (RVOL)."""
    avg_volume = df['Volume'].rolling(window=window).mean()
    return df['Volume'] / avg_volume

def identify_hammer(df: pd.DataFrame):
    """Identify Hammer candlestick pattern."""
    # Body is small (less than 1/3 of the candle range)
    # Lower shadow is at least 2x the body
    # Upper shadow is very small or non-existent
    body = np.abs(df['Close'] - df['Open'])
    candle_range = df['High'] - df['Low']
    lower_shadow = np.minimum(df['Close'], df['Open']) - df['Low']
    upper_shadow = df['High'] - np.maximum(df['Close'], df['Open'])
    
    is_hammer = (body <= candle_range / 3) & \
                (lower_shadow >= 2 * body) & \
                (upper_shadow <= body * 0.5)
    return is_hammer

def identify_doji(df: pd.DataFrame):
    """Identify Doji candlestick pattern."""
    # Body is very small (less than 10% of the candle range)
    body = np.abs(df['Close'] - df['Open'])
    candle_range = df['High'] - df['Low']
    is_doji = body <= (candle_range * 0.1)
    return is_doji
