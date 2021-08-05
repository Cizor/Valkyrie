from utility.config import *

"""
one_tick = {'tradable': True, 'mode': 'full', 'instrument_token': 2953217, 'last_price': 3272.65, 'last_quantity': 134,
     'average_price': 3283.4, 'volume': 2134713, 'buy_quantity': 115558, 'sell_quantity': 265693,
     'ohlc': {'open': 3300.0, 'high': 3305.2, 'low': 3261.2, 'close': 3284.9}, 'change': -0.3729185058905903,
     'last_trade_time': datetime.datetime(2021, 8, 4, 13, 9, 27), 'oi': 0, 'oi_day_high': 0, 'oi_day_low': 0,
     'timestamp': datetime.datetime(2021, 8, 4, 13, 9, 27), 'depth': {
        'buy': [{'quantity': 74, 'price': 3272.65, 'orders': 1},
                {'quantity': 128, 'price': 3272.6, 'orders': 2},
                {'quantity': 47, 'price': 3272.55, 'orders': 2}, {'quantity': 46, 'price': 3272.5, 'orders': 2},
                {'quantity': 17, 'price': 3272.3, 'orders': 1}],
        'sell': [{'quantity': 40, 'price': 3272.95, 'orders': 3}, {'quantity': 1, 'price': 3273.5, 'orders': 1},
                 {'quantity': 22, 'price': 3273.55, 'orders': 1},
                 {'quantity': 1, 'price': 3273.85, 'orders': 1},
                 {'quantity': 22, 'price': 3273.9, 'orders': 1}]}}
"""


class Tick:
    def __init__(self, tick_value):
        """
        Handles single tick and takes required values
        :param tick_value: Single Tick
        """
        self.value = tick_value
        self.instrument_token = self.value[INSTRUMENT_TOKEN]
        self.last_price = self.value[LAST_PRICE]
        self.average_price = self.value[AVERAGE_PRICE]
        self.change = self.value[CHANGE]
        self.last_trade_time = self.value[LAST_TRADE_TIME]
