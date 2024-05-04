# Trading Bot Project

## Overview
This trading bot is designed to automate forex trading using various strategies including YOLO, SMA, RSI, and more. It connects to the OANDA trading platform and can operate in both demo and live trading modes.

## Features
- Automated trading strategies including YOLO, SMA, and RSI.
- Configurable settings to activate/deactivate specific strategies.
- Support for both demo and live trading modes.
- Comprehensive logging and monitoring of trading activities.

## Installation

### Prerequisites
- Python 3.x
- pip
- Virtual Environment (recommended)

### Setup

1. **Clone the repository**
git clone https://yourrepositoryurl.com/trading_bot.git
cd trading_bot


2. **Create and activate a virtual environment**
- Windows:
  ```
  python -m venv venv
  .\venv\Scripts\activate
  ```
- macOS/Linux:
  ```
  python3 -m venv venv
  source venv/bin/activate
  ```

3. **Install dependencies**
pip install -r requirements.txt



## Configuration
Modify the `config.json` in the `config` folder to set your trading preferences:

```json
{
"use_yolo": 1,
"use_sma": 1,
"use_rsi": 0,
"trading_mode": 1,  // 0 for demo, 1 for live trading
"account_id_live": "your_live_account_id",
"account_id_demo": "your_demo_account_id"
}
use_yolo, use_sma, use_rsi: Set to 1 to activate the strategy, 0 to deactivate.
trading_mode: Set to 0 for demo and 1 for live trading.
account_id_live, account_id_demo: Specify account IDs for live and demo trading.


Running the Bot

Backtesting
python src/backtest.py


Live Trading
python src/main.py

Paper Trading (Demo Mode)
python src/main.py
