# trading_bot/src/main.py
import json
import pandas as pd
import streamlit as st
from src.strategy import fetch_forex_data, simple_moving_average_strategy
from src.strategy import sma, yolo_pattern

def load_config():
    with open('config/config.json', 'r') as file:
        return json.load(file)

def main():
    config = load_config()
    access_token = config['access_token']
    granularity = 'M15'
    instrument = 'EUR_USD'
    prices = fetch_forex_data(access_token, '2012-01-01T00:00:00Z', '2018-02-18T00:00:00Z', granularity, instrument)

    if config['use_sma']:
        df = simple_moving_average_strategy(prices)
        st.line_chart(df[['close', 'SMA20', 'SMA50']])

    if config['use_yolo']:
        # Placeholder for YOLO-based market analysis
        pass

if __name__ == "__main__":
    main()
