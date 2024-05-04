# src/main.py
import json
import pandas as pd
from strategy.strategy import fetch_forex_data, simple_moving_average_strategy
from strategy.yolo_pattern import detect_patterns, interpret_results, plot_candlestick_chart
from market_data import fetch_forex_data  # Add this import statement

def load_config():
    with open('config/config.json', 'r') as file:
        return json.load(file)


def main():
    config = load_config()
    if config['use_yolo']:
        data = fetch_forex_data(config['access_token'], '2017-01-01T00:00:00Z', '2018-01-01T00:00:00Z', 'D', 'EUR_USD')
        plot_candlestick_chart(data)
        patterns = detect_patterns('latest_chart.png', 'foduucom/stockmarket-future-prediction')
        for result in patterns:
            signals = interpret_results(result)
            print("Detected Patterns:", signals)

# def main():
#     config = load_config()
#     access_token = config['access_token']
#     granularity = 'M15'
#     instrument = 'EUR_USD'
#     prices = fetch_forex_data(access_token, '2012-01-01T00:00:00Z', '2018-02-18T00:00:00Z', granularity, instrument)

#     if config['use_sma']:
#         df = simple_moving_average_strategy(prices)
#         print(df.head())

#     if config['use_yolo']:
#         # Placeholder for YOLO-based market analysis
#         pass

if __name__ == "__main__":
    main()
