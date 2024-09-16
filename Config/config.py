# Please go to README.md to set up config.py

mt5_credentials = {
    'login' : 25141208,
    'password' : 'l4!z9,JM5>bl',
    'server' : 'Tickmill-Demo'
}


def initialize_mt5():
    import MetaTrader5 as mt5
    mt5.initialize(mt5_credentials)
    mt5.login(mt5_credentials['login'], mt5_credentials['password'], mt5_credentials['server'])