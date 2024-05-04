# src\strategy\yolo_pattern.py
import matplotlib.pyplot as plt
import cv2
from ultralytics import YOLO
import pandas as pd
from ultralyticsplus import YOLO, render_result

def plot_candlestick_chart(data, filename='latest_chart.png'):
    fig, ax = plt.subplots()
    ax.plot(data['close'], label='Close Price')  # Simplified; for real use mplfinance to plot actual candlestick
    plt.legend()
    fig.savefig(filename)
    plt.close(fig)

def detect_patterns(image_path, model_path):
    model = YOLO(model_path)
    image = cv2.imread(image_path)
    results = model(image)
    return results


def interpret_results(results, threshold=0.3):
    signals = []
    for result in results.xyxy[0]:  # Assuming results.xyxy contains detection
        if result[4] >= threshold:  # Confidence threshold
            label = result[5]  # Assuming 5th index is the class label
            signals.append(label.item())
    return signals
