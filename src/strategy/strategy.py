# src\strategy\strategy.py
import pandas as pd
import numpy as np
from oandapyV20 import API
from oandapyV20.contrib.factories import InstrumentsCandlesFactory

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
    df['SMA20'] = df['close'].rolling(window=20).mean()
    df['SMA50'] = df['close'].rolling(window=50).mean()
    df['signal'] = 0
    df.loc[50:, 'signal'] = np.where(df['SMA20'][50:] > df['SMA50'][50:], 1, 0)
    df['position'] = df['signal'].diff()
    return df
