from utility.config import NIFTY_50_STOCKS, DB_FILE, API_KEY, INTERVAL_MINUTE, \
    ACCESS_TOKEN, MID_CAP_FILE, LARGE_CAP_FILE, EXCHANGE, INSTRUMENT_TOKEN, CHANGE_PERCENTAGE, CHANGE
from utility.utility import pickle_read
from kiteconnect import KiteConnect, KiteTicker
import pprint
from datetime import datetime
import pprint

"""
    Look for stocks that has moved up >3% by 11: 15 AM from Day open.
    Go long at 11:15 AM candle close
    Stop loss Day open price, if stock goes below day open price, we exit.
    If stop loss is not hit, we close the position by 3.20 PM
    No shorts, only long.
"""


class Arceus:
    def __init__(self):
        self.k = KiteConnect(api_key=API_KEY)
        self.k.set_access_token(ACCESS_TOKEN)
        self.mid_caps = pickle_read(MID_CAP_FILE)
        self.large_caps = pickle_read(LARGE_CAP_FILE)
        self.all_stocks = pickle_read(DB_FILE)
        self.subscribe_list = list()
        self.get_stocks()
        self.kws = KiteTicker(API_KEY, ACCESS_TOKEN)
        self.kws.on_ticks = self.on_ticks
        self.kws.on_connect = self.on_connect
        self.kws.on_close = self.on_close
        self.stock_data = list()
        self.start_ticker()
        self.get_high_change_stocks()

    def get_stocks(self):
        for i in self.mid_caps:
            try:
                self.subscribe_list.append(self.all_stocks[i][INSTRUMENT_TOKEN])
            except KeyError:
                pass

    def on_ticks(self, ws, ticks):
        # Callback to receive ticks.
        self.stock_data.extend(ticks)
        self.kws.close()

    def on_connect(self, ws, response):
        # Callback on successful connect.
        # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
        ws.subscribe(self.subscribe_list)

        # Set RELIANCE to tick in `full` mode.
        ws.set_mode(ws.MODE_FULL, self.subscribe_list)

    def on_close(self, ws, code, reason):
        # On connection close stop the event loop.
        # Reconnection will not happen after executing `ws.stop()`
        ws.stop()

    def start_ticker(self):
        self.kws.connect()

    def get_high_change_stocks(self):
        high_percentage_stocks_tokens = list()
        high_percentage_stocks_symbols = list()
        for i in self.stock_data:
            if i[CHANGE] >= 3:
                high_percentage_stocks_tokens.append(i[INSTRUMENT_TOKEN])

        # pprint.pprint(self.k.quote(high_percentage_stocks_tokens))
        # pprint.pp(self.all_stocks)
        for key, val in self.all_stocks.items():
            if val[INSTRUMENT_TOKEN] in high_percentage_stocks_tokens:
                print(key)

