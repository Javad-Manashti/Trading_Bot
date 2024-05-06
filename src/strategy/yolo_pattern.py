# trading_bot/src/strategy/yolo_pattern.py
import matplotlib.pyplot as plt
import mplfinance as mpf
from ultralyticsplus import YOLO, render_result
import pandas as pd

def plot_candlestick_chart(df, filename='latest_chart.png'):
    df.index = pd.to_datetime(df['time'])
    df = df[['open', 'high', 'low', 'close', 'volume']]
    mpf.plot(df, type='candle', volume=True, style='charles', savefig=filename)

def detect_patterns(image_path, model_path='foduucom/stockmarket-pattern-detection-yolov8'):
    model = YOLO(model_path)
    results = model.predict(source=image_path)
    return results

def interpret_results(results, threshold=0.3):
    signals = []
    for result in results:
        for detection in result.boxes:
            if detection.conf >= threshold:
                label = detection.cls.item()
                signals.append(label)
    return signals
