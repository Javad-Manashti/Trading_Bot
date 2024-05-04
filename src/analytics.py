def calculate_metrics(trades):
    wins = 0
    total_pip_profit = 0
    total_pip_loss = 0
    
    for buy_price, sell_price in trades:
        pip_profit = (sell_price - buy_price) * 10000  # assuming EUR/USD pip size
        if pip_profit > 0:
            wins += 1
            total_pip_profit += pip_profit
        else:
            total_pip_loss += abs(pip_profit)
    
    win_rate = (wins / len(trades)) * 100 if trades else 0
    return win_rate, total_pip_profit, total_pip_loss