import builtins
import logging
from kiteconnect import KiteTicker

from utility.config import API_KEY, ACCESS_TOKEN, DB_FILE, INSTRUMENT_TOKEN, NAME
from utility.mis_allowed import mis_allowed
from utility.utility import pickle_read
import pandas as pd
import time

logging.basicConfig(level=logging.DEBUG)


class KTicker():
    def __init__(self):
        self.kws = KiteTicker(API_KEY, ACCESS_TOKEN)
        self.stock_objects_dict = dict()
        self.prepare_stock_object_dict()
        self.counter = 0
        self.call = None
        self.df = pd.DataFrame(columns=['last_price'])
        self.kws.on_ticks = self.on_ticks
        self.kws.on_connect = self.on_connect
        self.kws.on_close = self.on_close
        self.kws.connect()

    def on_ticks(self, ws, ticks):
        # Callback to receive ticks.
        # logging.debug("Ticks: {}".format(ticks))

        if len(self.df) == 0 or ticks[0]['last_price'] != self.df['last_price'].iloc[-1]:
            self.counter += 1
            temp = {'last_price': ticks[0]['last_price']}
            temp_df = pd.DataFrame(temp, index=[len(self.df)])
            self.df = pd.concat([self.df, temp_df])
            self.df = self.fill_RSI_second(self.df, 200)
            self.df = self.simple_moving_average_second(self.df)
            self.print_last(self.df)
        else:
            pass


    def on_connect(self, ws, response):
        # Callback on successful connect.
        # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
        ws.subscribe([2883073])

        # Set RELIANCE to tick in `full` mode.
        ws.set_mode(ws.MODE_LTP, [2883073])

    def on_close(self, ws, code, reason):
        # On connection close stop the main loop
        # Reconnection will not happen after executing `ws.stop()`
        ws.stop()

    def prepare_stock_object_dict(self):
        pass
        """
        all_stocks = pickle_read(DB_FILE)
        for i in mis_allowed:
            self.stock_objects_dict[all_stocks[i][INSTRUMENT_TOKEN]] = f"I am{all_stocks[i][NAME]}"
        print(self.stock_objects_dict)
        """

    def fill_RSI_second(self, df, interval):
        delta = df['last_price'].diff()
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        rUp = up.ewm(com=interval - 1, adjust=False).mean()
        rDown = down.ewm(com=interval - 1, adjust=False).mean().abs()
        df['RSI'] = 100 - 100 / (1 + rUp / rDown)
        df['RSI'].fillna(len(df), inplace=True)
        return df

    def simple_moving_average_second(self, df):
        df['SMA_RSI'] = df['RSI'].rolling(window=50).mean()
        df['SMA_RSI'].fillna(len(df), inplace=True)
        return df

    def print_last(self, df):
        print(self.counter, df['last_price'].iloc[-1], df['RSI'].iloc[-1], df['SMA_RSI'].iloc[-1])

    def set_buy_or_sell(self, df):
        if self.counter < 200:
            pass
        elif self.counter > 200:
            if self.call is None:
                self.call = "START_CALL"
            elif self.call == "START_CALL":
                if df['RSI'].iloc[-1] > df['SMA_RSI'].iloc[-1]:
                    self.call = "LATE_BUY_CALL"
                else:
                    self.call = "LATE_SELL_CALL"
            elif self.call == "LATE_BUY_CALL":
                if df['RSI'].iloc[-1] > df['SMA_RSI'].iloc[-1]:
                    print("STILL ABOVE IN START!")
                if df['RSI'].iloc[-1] < df['SMA_RSI'].iloc[-1]:
                    self.call = "CHECK_TO_BUY_CALL"
            elif self.call == "LATE_SELL_CALL":
                if df['RSI'].iloc[-1] < df['SMA_RSI'].iloc[-1]:
                    print("STILL BELOW IN START!")
                if df['RSI'].iloc[-1] > df['SMA_RSI'].iloc[-1]:
                    self.call = "CHECK_TO_SELL_CALL"
            elif self.call == "CHECK_TO_BUY_CALL":
                if df['RSI'].iloc[-1] > df['SMA_RSI'].iloc[-1]:
                    self.do_buy()
                    self.call = "CHECK_TO_SELL_CALL"
                else:
                    print("Don't buy yet")
            elif self.call == "CHECK_TO_SELL_CALL":
                if df['RSI'].iloc[-1] < df['SMA_RSI'].iloc[-1]:
                    self.do_sell()
                    self.call = "CHECK_TO_BUY_CALL"
                else:
                    print("Don't sell yet")

    def do_sell(self):
        print(f"First complete existing buy and SELLING at {self.df['last_price'].iloc[-1]} and short sell")

    def do_buy(self):
        print(f"First complete existing short sell and then BUYING at {self.df['last_price'].iloc[-1]}")



if __name__ == '__main__':
    k = KTicker()

