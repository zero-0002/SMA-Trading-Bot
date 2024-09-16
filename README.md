# Simple Moving Average (SMA) Trading Bot

## Overview

This project features a trading bot that uses the Simple Moving Average (SMA) strategy to trade the EUR/USD forex pair. The bot operates on MetaTrader 5 (MT5), utilizing historical data to make trading decisions based on SMA calculations. The bot demonstrates how to automate trading strategies with Python, integrating with MT5 to perform buy and sell operations based on technical indicators.

## Technologies Used

- **MetaTrader 5 (MT5)**: Trading platform used for executing trades and retrieving market data.
- **Python**: Programming language used for scripting the trading bot.
- **Pandas**: Library for data manipulation and analysis.
- **MetaTrader5 Python API**: For interacting with the MT5 platform.
- **Time and DateTime Modules**: For managing execution intervals and timestamps.

## Installation

1. **MetaTrader 5**: Ensure MetaTrader 5 is installed and set up on your machine.
2. **Python Libraries**: Install required libraries using pip:

   ```bash
   pip install MetaTrader5 pandas
   ```

3. **Configuration**: Update the credentials and server details directly in the script or use a configuration file.

## Setup

1. **Initialization**:
   The script initializes a connection to MetaTrader 5 using your credentials and server information.
   
   ```python
   import MetaTrader5 as mt5
   from mt5_trade_utils import send_market_order, close_all_positions, get_positions
   import pandas as pd
   from time import sleep
   from datetime import datetime

   mt5.initialize()
   mt5.login(login, password, server)
   ```

2. **Strategy Parameters**:
   - **Symbol**: Trading pair, set to 'EURUSD'.
   - **Time Frame**: 1-minute candles (`mt5.TIMEFRAME_M1`).
   - **SMA Period**: 20 candles.
   - **Magic Number**: 1 (identifies orders from this bot).

   ```python
   symbol = 'EURUSD'
   time_frame = mt5.TIMEFRAME_M1
   period = 20
   magic = 1
   volume = 2
   ```

## Trading Logic

1. **SMA Calculation**:
   The bot fetches the latest 20-minute candlestick data, computes the Simple Moving Average (SMA), and compares it with the most recent closing price.

   ```python
   rates = mt5.copy_rates_from_pos(symbol, time_frame, 1, 20)
   rates_df = pd.DataFrame(rates)
   sma = rates_df['close'].mean()
   last_close = rates_df.iloc[-1]['close']
   ```

2. **Order Management**:
   - **Buy Conditions**: If the last close price is greater than the SMA and no existing buy positions are open, the bot sends a buy order.
   - **Sell Conditions**: If the last close price is less than the SMA and no existing sell positions are open, the bot sends a sell order.
   - **Position Closure**: Closes opposing positions if a new trade signal is generated.

   ```python
   positions = get_positions(magic=magic)
   num_buy_positions = positions[positions['type'] == mt5.ORDER_TYPE_BUY].shape[0]
   num_sell_positions = positions[positions['type'] == mt5.ORDER_TYPE_SELL].shape[0]

   if last_close > sma:
       if num_sell_positions > 0:
           close_all_positions('sell', magic=magic)
       if num_buy_positions == 0:
           send_market_order(symbol, volume, 'buy', magic=magic)
   elif last_close < sma:
       if num_buy_positions > 0:
           close_all_positions('buy', magic=magic)
       if num_sell_positions == 0:
           send_market_order(symbol, volume, 'sell', magic=magic)
   ```

3. **Execution Loop**:
   The bot continuously runs and checks trading conditions every second.

   ```python
   while trading_allowed:
       # Trading logic
       sleep(1)
   ```

## Strategy Explanation

The bot employs the Simple Moving Average (SMA) strategy, a common method in technical analysis:

- **Simple Moving Average (SMA)**: A trend-following indicator that smooths out price data by averaging prices over a specified period (20 minutes in this case). It helps in identifying the direction of the trend.

- **Trading Signal**: 
  - **Buy Signal**: Triggered when the current price is above the SMA, suggesting an uptrend.
  - **Sell Signal**: Triggered when the current price is below the SMA, indicating a downtrend.

## Skills Demonstrated

- **Technical Analysis**: Implementing SMA to guide trading decisions.
- **Automation**: Creating an automated trading bot that interacts with MT5.
- **Data Handling**: Using Pandas for data manipulation and analysis.
- **API Integration**: Connecting to MT5 for trading operations.

## Future Enhancements

- **Risk Management**: Incorporate stop-loss and take-profit mechanisms.
- **Advanced Strategies**: Explore and integrate additional trading strategies and indicators.
- **User Interface**: Develop a UI for easier configuration and monitoring of the bot.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Feel free to customize the README further based on additional requirements or features you might add to the project!
