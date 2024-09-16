import MetaTrader5 as mt5
import pandas as pd


# Function to send a market order
def send_market_order(symbol, volume, order_type, sl=0.0, tp=0.0,
                      deviation=20, comment='', magic=0, type_filling=mt5.ORDER_FILLING_IOC):
    # Retrieve the current tick data for the given symbol
    tick = mt5.symbol_info_tick(symbol)

    # Dictionary to map order type to MetaTrader5 constants
    order_dict = {'buy': 0, 'sell': 1}
    # Dictionary to select price based on order type
    price_dict = {'buy': tick.ask, 'sell': tick.bid}

    # Prepare the order request
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_dict[order_type],
        "price": price_dict[order_type],
        "sl": sl,
        "tp": tp,
        "deviation": deviation,
        "magic": magic,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": type_filling,
    }

    # Send the order request and return the result
    order_result = mt5.order_send(request)
    return order_result


# Function to close a specific position
def close_position(position, deviation=20, magic=0, comment='', type_filling=mt5.ORDER_FILLING_IOC):
    # Dictionary to map position type to MetaTrader5 constants
    order_type_dict = {
        0: mt5.ORDER_TYPE_SELL,
        1: mt5.ORDER_TYPE_BUY
    }

    # Dictionary to select price based on position type
    price_dict = {
        0: mt5.symbol_info_tick(position['symbol']).bid,
        1: mt5.symbol_info_tick(position['symbol']).ask
    }

    # Prepare the close position request
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "position": position['ticket'],  # Position ticket to identify which position to close
        "symbol": position['symbol'],
        "volume": position['volume'],  # Volume of the position to close
        "type": order_type_dict[position['type']],
        "price": price_dict[position['type']],
        "deviation": deviation,  # Allowed deviation from the requested price
        "magic": magic,  # Magic number for order identification
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": type_filling,
    }

    # Send the close position request and return the result
    order_result = mt5.order_send(request)
    return order_result


# Function to close all open positions of a specific type
def close_all_positions(order_type, magic=None, type_filling=mt5.ORDER_FILLING_IOC):
    # Dictionary to map order type to MetaTrader5 constants
    order_type_dict = {
        'buy': 0,
        'sell': 1
    }

    # Check if there are any open positions
    if mt5.positions_total() > 0:
        # Get all open positions
        positions = mt5.positions_get()
        positions_df = pd.DataFrame(positions, columns=positions[0]._asdict().keys())

        # Filter positions by magic number if specified
        if magic:
            positions_df = positions_df[positions_df['magic'] == magic]

        # Filter positions by order type if specified
        if order_type != 'all':
            positions_df = positions_df[positions_df['type'] == order_type_dict[order_type]]

        # Check if there are any positions left after filtering
        if positions_df.empty:
            print('No open positions')
            return []

        # Close each filtered position
        results = []
        for _, position in positions_df.iterrows():
            order_result = close_position(position, type_filling=type_filling)
            print('order_result: ', order_result)
            results.append(order_result)

        return results


# Function to modify Stop Loss (SL) and Take Profit (TP) for a position
def modify_sl_tp(ticket, stop_loss, take_profit):
    # Convert SL and TP to float
    stop_loss = float(stop_loss)
    take_profit = float(take_profit)

    # Prepare the SL/TP modification request
    request = {
        'action': mt5.TRADE_ACTION_SLTP,
        'position': ticket,
        'sl': stop_loss,
        'tp': take_profit
    }

    # Send the modification request and return the result
    res = mt5.order_send(request)
    return res


# Function to get all open positions, optionally filtered by magic number
def get_positions(magic=None):
    # Check if there are any open positions
    if mt5.positions_total():
        # Get all open positions
        positions = mt5.positions_get()
        positions_df = pd.DataFrame(positions, columns=positions[0]._asdict().keys())

        # Filter positions by magic number if specified
        if magic:
            positions_df = positions_df[positions_df['magic'] == magic]

        return positions_df

    # Return an empty DataFrame with the appropriate columns if no positions are found
    return pd.DataFrame(columns=['ticket', 'time', 'time_msc', 'time_update', 'time_update_msc', 'type',
                                 'magic', 'identifier', 'reason', 'volume', 'price_open', 'sl', 'tp',
                                 'price_current', 'swap', 'profit', 'symbol', 'comment', 'external_id'])
