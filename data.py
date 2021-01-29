import time
import datetime
from configobj import ConfigObj
from poloniex_api import Poloniex


cfg = ConfigObj('config.ini', encoding='utf8')


def poloniex():
    api_key = cfg['API']['key']
    api_secret = cfg['API']['secret']
    p = Poloniex(
        API_KEY=api_key,
        API_SECRET=api_secret
    )
    return p


def ticker():
    coin1 = cfg['PAIR']['coin1']  # первая монета пары (BTC, ETH, USDT)
    coin2 = cfg['CURRENCY']['coin2']  # вторая монета пары

    if coin1 == "BTC":
        TICKER = 'BTC_{currency}'.format(currency=coin2)
    elif coin1 == "USDT":
        TICKER = 'USDT_{currency}'.format(currency=coin2)
    elif coin1 == "USDC":
        TICKER = 'USDC_{currency}'.format(currency=coin2)
    elif coin1 == "ETH":
        TICKER = 'ETH_{currency}'.format(currency=coin2)
    elif coin1 == "XMR":
        TICKER = 'XMR_{currency}'.format(currency=coin2)
    return TICKER
