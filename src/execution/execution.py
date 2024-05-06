import logging

def execute_trades(api, df, symbol, account_id):
    last_row = df.iloc[-1]
    try:
        if last_row['position'] == 1:
            logging.info("Signal to BUY!")
            api.order.market(accountID=account_id, instrument=symbol, units=100)
        elif last_row['position'] == -1:
            logging.info("Signal to SELL!")
            api.order.market(accountID=account_id, instrument=symbol, units=-100)
    except Exception as e:
        logging.error(f"Failed to execute trade: {e}")