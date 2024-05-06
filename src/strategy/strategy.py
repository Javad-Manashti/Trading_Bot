# trading_bot/src/strategy/strategy.py
import pandas as pd
import numpy as np
import logging
from oandapyV20 import API
from oandapyV20.contrib.factories import InstrumentsCandlesFactory

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_forex_data(access_token, from_date, to_date, granularity, instrument):
    client = API(access_token=access_token, environment="practice")
    params = {"granularity": granularity, "from": from_date, "to": to_date}
    data = []
    for request in InstrumentsCandlesFactory(instrument=instrument, params=params):
        response = client.request(request)
        for candle in response.get('candles'):
            rec = {
                'time': candle.get('time')[0:19],
                'complete': candle['complete'],
                'open': float(candle['mid']['o']),
                'high': float(candle['mid']['h']),
                'low': float(candle['mid']['l']),
                'close': float(candle['mid']['c']),
                'volume': candle['volume'],
            }
            data.append(rec)
    return pd.DataFrame(data)

def simple_moving_average_strategy(df):
    """
    Apply the SMA strategy to the DataFrame.
    """
    df = df.copy()
    df.loc[:, 'SMA20'] = df['close'].rolling(window=20).mean().fillna(0)
    df.loc[:, 'SMA50'] = df['close'].rolling(window=50).mean().fillna(0)

    # Log SMA column lengths
    logging.debug(f"Length of SMA20 column: {len(df['SMA20'])}")
    logging.debug(f"Length of SMA50 column: {len(df['SMA50'])}")

    df.loc[:, 'signal'] = 0

    # Log the lengths of signals before assignment
    sma_condition = df['SMA20'][50:] > df['SMA50'][50:]
    logging.debug(f"Length of SMA condition: {len(sma_condition)}")

    signal_values = np.where(sma_condition, 1, 0)
    logging.debug(f"Length of signal values: {len(signal_values)}")

    try:
        df.loc[df.index[50:], 'signal'] = signal_values
    except ValueError as e:
        logging.error(f"Error assigning signal values: {e}")
        logging.debug(f"df index length: {len(df.index)}")
        logging.debug(f"Signal index length: {len(df.loc[50:].index)}")
        raise

    df.loc[:, 'position'] = df['signal'].diff().fillna(0)

    return df

def rsi_strategy(df, window=14):
    """
    Apply the RSI strategy to the DataFrame.
    """
    df = df.copy()
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean().fillna(0)
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean().fillna(0)
    rs = gain / loss
    df.loc[:, 'RSI'] = 100 - (100 / (1 + rs)).fillna(0)
    return df
