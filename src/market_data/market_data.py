# trading_bot/src/market_data/market_data.py
import pandas as pd
from oandapyV20 import API
from oandapyV20.contrib.factories import InstrumentsCandlesFactory
import logging

# Suppress oandapyV20 logging
logging.getLogger("oandapyV20").setLevel(logging.ERROR)

def fetch_forex_data(access_token, from_date, to_date, granularity, instrument):
    client = API(access_token=access_token, environment="practice")
    params = {
        "granularity": granularity,
        "from": from_date,
        "to": to_date
    }
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
