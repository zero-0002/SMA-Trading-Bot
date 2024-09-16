import MetaTrader5 as mt5

# Import utility functions for trading operations
from mt5_trade_utils import send_market_order, close_position, close_all_positions
from time import sleep

if __name__ == "__main__":
    # Initialize connection to MetaTrader 5
    mt5.initialize()

    # Define login credentials and server information
    login = 25141208
    password = 'l4!z9,JM5>bl'  # Replace with your actual password
    server = 'Tickmill-Demo'    # Replace with your actual server

    # Log in to MetaTrader 5 with provided credentials
    mt5.login(login, password, server)

    # Wait 5 seconds after logging in
    sleep(5)
    symbol = 'EURUSD'
    volume = 1.0
    order_type = 'sell'
    send_market_order(symbol, volume, order_type)
    sleep(5)
    close_all_positions('all')




