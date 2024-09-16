import MetaTrader5 as mt5
from mt5_trade_utils import send_market_order, close_all_positions, get_positions
import pandas as pd
from time import sleep
from datetime import datetime


if __name__ == '__main__':
    # Initialize connection to MetaTrader 5
    mt5.initialize()

    # Define login credentials and server information
    login = 25141208
    password = 'l4!z9,JM5>bl'  # Replace with your actual password
    server = 'Tickmill-Demo'    # Replace with your actual server

    # Log in to MetaTrader 5 with provided credentials
    mt5.login(login, password, server)

    # strategy parameters
    symbol = 'EURUSD'
    time_frame = mt5.TIMEFRAME_M1
    period = 20
    # The 'magic' number identifies orders from different trading bots in MetaTrader 5 running at the same time.
    magic = 1


    volume = 1.0

    # sleep to switch to MT5 platform manually to check execution
    sleep(5)

    # trade logic
    trading_allowed = True
    while trading_allowed:

        # calculate sma
        # Take The Last 20 Candles - start from last closed candle
        # Convert candles to pandas data frame
        # Take close prices and we calculate the average = The SMA
        rates = mt5.copy_rates_from_pos(symbol, time_frame, 1, 20)
        rates_df = pd.DataFrame(rates)
        print(rates)

        sma = rates_df['close'].mean()

        # calculate last_close
        last_close = rates_df.iloc[-1]['close']

        print('time', datetime.now(), '|', 'sma', sma, '|', 'last_close', last_close)

        # retrieving positions by magic
        positions = get_positions(magic=magic)

        # separating positions into buy and sell orders
        num_buy_positions = positions[positions['type'] == mt5.ORDER_TYPE_BUY].shape[0]
        num_sell_positions = positions[positions['type'] == mt5.ORDER_TYPE_SELL].shape[0]

        if last_close > sma:
            # close sell positions
            if num_sell_positions > 0:
                close_all_positions('sell', magic=magic)

            # open buy positions
            if num_buy_positions == 0:
                send_market_order(symbol, volume, 'buy', magic=magic)

        elif last_close < sma:
            # close buy positions
            if num_buy_positions > 0:
                close_all_positions('buy', magic=magic)

            # open sell positions
            if num_sell_positions == 0:
                send_market_order(symbol, volume, 'sell', magic=magic)

        sleep(1)


