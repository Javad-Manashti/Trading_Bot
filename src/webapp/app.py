# trading_bot/src/webapp/app.py
import streamlit as st
import json
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt
import logging
import time
import mplfinance as mpf

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.market_data.market_data import fetch_forex_data
from src.strategy.strategy import simple_moving_average_strategy, rsi_strategy
from src.strategy.yolo_pattern import plot_candlestick_chart, detect_patterns, interpret_results

# Suppress excessive OANDA logging
logging.basicConfig(level=logging.ERROR)
logging.getLogger("oandapyV20").setLevel(logging.ERROR)

# Initialize global variables for caching
cached_data = {}
fig = None
ax_candle = None
ax_volume = None

def load_config():
    """
    Load the configuration from the JSON file.
    """
    with open('config/config.json', 'r') as file:
        return json.load(file)

def fetch_and_update_data(access_token, pair, granularity, from_date, to_date):
    """
    Fetch and update cached data for the given pair.
    """
    if pair not in cached_data:
        cached_data[pair] = fetch_forex_data(access_token, from_date, to_date, granularity, pair)
    else:
        # Fetch only the latest data
        new_data = fetch_forex_data(access_token, to_date, '2024-05-05T00:00:00Z', granularity, pair)
        cached_data[pair] = pd.concat([cached_data[pair], new_data]).drop_duplicates().reset_index(drop=True)
    return cached_data[pair].tail(500)  # Limit to the last 500 candles

def plot_chart(df, title):
    """
    Plot the chart efficiently by reusing the figure and axes.
    """
    global fig, ax_candle, ax_volume
    df.index = pd.to_datetime(df['time'])
    df = df[['open', 'high', 'low', 'close', 'volume']]

    if fig is None or ax_candle is None or ax_volume is None:
        fig, ax_list = mpf.plot(
            df,
            type='candle',
            volume=True,
            style='charles',
            title=title,
            returnfig=True,
            warn_too_much_data=500  # Adjust as needed
        )
        ax_candle = ax_list[0]
        ax_volume = ax_list[1]
    else:
        ax_candle.clear()
        ax_volume.clear()
        mpf.plot(
            df,
            type='candle',
            style='charles',
            ax=ax_candle,
            volume=ax_volume
        )
    st.pyplot(fig)

def analyze_yolo(df, instrument):
    """
    Perform YOLO analysis on the given instrument and display results.
    """
    st.write(f"**Starting YOLO Analysis for {instrument}...**")
    screenshot_path = f'{instrument}_candlestick_chart.png'
    plot_candlestick_chart(df, screenshot_path)

    results = detect_patterns(screenshot_path)
    signals = interpret_results(results)

    st.write(f"**YOLO Analysis Results for {instrument}: {signals if signals else 'No signals found'}**")

def main():
    """
    Main function to initialize the Forex Trading Signals Dashboard.
    """
    st.title("Forex Trading Signals Dashboard")

    config = load_config()
    access_token = config['access_token']
    pairs = config.get('pairs', ['EUR_USD', 'GBP_USD', 'USD_JPY', 'AUD_USD', 'USD_CHF', 'USD_CAD', 'NZD_USD', 'EUR_GBP', 'EUR_JPY', 'GBP_JPY'])

    selected_pair = st.sidebar.selectbox("Select Pair", pairs)
    granularity = st.sidebar.selectbox("Select Timeframe", ['M1', 'M15', 'H1', 'H4', 'D'])
    strategies = st.sidebar.multiselect("Select Strategies", ['SMA', 'RSI', 'YOLO'], ['SMA'])

    st.sidebar.button("Analyze Patterns", key="analyze_patterns")

    def update_screen():
        st.write(f"Fetching data for {selected_pair}...")
        prices = fetch_and_update_data(access_token, selected_pair, granularity, '2024-01-01T00:00:00Z', '2024-05-05T00:00:00Z')

        if 'SMA' in strategies:
            df = simple_moving_average_strategy(prices)
            plot_chart(df, f"Price Chart for {selected_pair}")
        if 'RSI' in strategies:
            df = rsi_strategy(prices)
            st.line_chart(df[['RSI']])

        if 'YOLO' in strategies and st.session_state.get("analyze_patterns"):
            analyze_yolo(prices, selected_pair)

    # Update the screen every 1 minute
    while True:
        update_screen()
        time.sleep(60)

if __name__ == "__main__":
    main()
