"""
Use 8 SMA, 50 SMA and 200 SMA

buy when 8 SMA > 50 SMA > 200 SMA

sell when 2 SMA < 50 SMA
"""
import json

from kiteconnect import KiteConnect, KiteTicker

from utility.utility import *
from datetime import datetime, timedelta
import pandas as pd

"""
Interval is of 1 day
RSI of 2
Moving average of 10 and 200

Buy Condition next day if: 
1. Price above 200 SMA
2. Price below 10 SMA
3. RSI below 10
4. Register 10 SMA value

If met, buy stock next day

Sell when:
1. Price touches 10 SMA value
"""


class Dodrio:
    def __init__(self):
        self._current_price = None
        self.k = KiteConnect(api_key=API_KEY)
        self.kws = KiteTicker(API_KEY, ACCESS_TOKEN)
        self.kws.on_ticks = self.on_ticks
        self.kws.on_connect = self.on_connect
        self.kws.on_close = self.on_close
        self.k.set_access_token(ACCESS_TOKEN)
        self.stock_interval = INTERVAL_5_MINUTE
        assert self.stock_interval in INTERVAL_DAY_RATIO.keys()
        self.stock_historical_days = INTERVAL_DAY_RATIO[self.stock_interval]
        self.stock_token = 0
        self.seg_stocks = list()
        f = open("result.json")
        self.large_stocks = json.load(f)
        f.close()
        self.df = None
        self.rsi_column = 'RSI_close'
        self.sma_8_column = '8_SMA_RSI'
        self.sma_50_column = '50_SMA_RSI'
        self.sma_200_column = '200_SMA_RSI'
        self.ema_5 = '5_EMA'
        self.current_tick_price = 0
        self.today_stock_data = dict()
        self.get_sma()
        print(self.df)
        self.open_price = None
        self.close_price = None
        self.low_price = None
        self.high_price = None
        self.ema_5_price = None
        self.position_taken = False
        self.handle_5_ema()
        # print(self.seg_stocks)

    def get_historical_data(self):
        enddate = datetime.today().date()  # - timedelta(days=1)
        # startdate = enddate - timedelta(days=self.stock_historical_days)
        df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        try:
            data = self.k.historical_data(self.stock_token, enddate, enddate, self.stock_interval, oi=1)
            print(data)
            df = pd.DataFrame.from_dict(data, orient='columns', dtype=None)
            if not df.empty:
                df = df[['date', 'open', 'high', 'low', 'close', 'volume', 'oi']]
                df['date'] = df['date'].astype(str).str[:-6]
            else:
                print("Error in getting historical data")
        except Exception as e:
            print("Error in getting historical data", e)
        return df

    def get_sma(self):
        for key, val in self.large_stocks.items():
            print(key, val)
            self.stock_token = val
            self.df = self.get_historical_data()
            self.fill_8_simple_moving_average()
            self.fill_50_simple_moving_average()
            self.fill_200_simple_moving_average()
            self.fill_5_ema()
            self.today_stock_data[key] = {'close': self.df['close'].iloc[-1],
                                          self.sma_8_column: self.df[self.sma_8_column].iloc[-1],
                                          self.sma_50_column: self.df[self.sma_50_column].iloc[-1],
                                          self.sma_200_column: self.df[self.sma_200_column].iloc[-1],
                                          self.ema_5: self.df[self.ema_5].iloc[-1]}

            # self.segregate_stocks(key,
            #                      self.df[self.sma_8_column].iloc[-1],
            #                      self.df[self.sma_50_column].iloc[-1],
            #                      self.df[self.sma_200_column].iloc[-1])

    def segregate_stocks(self, key, sma_8, sma_50, sma_200):
        if not sma_8 > sma_50 > sma_200:
            print(key, sma_8, sma_50, sma_200)
            self.seg_stocks.append(key)

    def fill_8_simple_moving_average(self):
        self.df[self.sma_8_column] = self.df['close'].rolling(window=8).mean()
        self.df[self.sma_8_column].fillna(len(self.df), inplace=True)

    def fill_50_simple_moving_average(self):
        self.df[self.sma_50_column] = self.df['close'].rolling(window=50).mean()
        self.df[self.sma_50_column].fillna(len(self.df), inplace=True)

    def fill_200_simple_moving_average(self):
        self.df[self.sma_200_column] = self.df['close'].rolling(window=200).mean()
        self.df[self.sma_200_column].fillna(len(self.df), inplace=True)

    def fill_5_ema(self):
        self.df[self.ema_5] = self.df['close'].ewm(span=5, min_periods=0, adjust=False, ignore_na=False).mean()
        self.df[self.ema_5].fillna(len(self.df), inplace=True)

    def handle_5_ema(self):
        print('Last value')
        print(list(self.df))
        self.open_price = self.df.iloc[-1]['open']
        self.close_price = self.df.iloc[-1]['close']
        self.low_price = self.df.iloc[-1]['low']
        self.high_price = self.df.iloc[-1]['high']
        self.ema_5_price = self.df.iloc[-1]['5_EMA']

        self.handle_alert_candle()
        # if low_price > ema_5_price:
        #     print("This is alert candle")
        #     self.handle_alert_candle(high_price, low_price)

    # Start ticker and buy PE if price goes below low_price
    # Exit if price is crosses above high_price or
    # Exit if price = low_price - (2 *(high_price - low_price))
    def handle_alert_candle(self):
        self.kws.connect()

    def on_ticks(self, ws, ticks):
        # Callback to receive ticks.
        print(ticks)
        self.current_price = ticks[0]['last_price']

    def on_connect(self, ws, response):
        # Callback on successful connect.
        # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
        ws.subscribe([256265])
        # Set RELIANCE to tick in `full` mode.
        ws.set_mode(ws.MODE_FULL, [256265])

    def on_close(self, ws, code, reason):
        # On connection close stop the event loop.
        # Reconnection will not happen after executing `ws.stop()`
        ws.stop()

    def check_current_price(self):
        print(self.current_price, self.ema_5_price, self.low_price, self.high_price)
        print("Current price: ", self.current_price)
        print("5 EMA price: ", self.ema_5_price)
        print("Low price: ", self.low_price)
        print("High price: ", self.high_price)
        print("Decide for buying or exiting")
        if self.current_price < self.low_price and self.position_taken is False:
            print("Buying now")
            self.position_taken = True
            self.k.place_order(self.k.VARIETY_REGULAR, exchange=self.k.EXCHANGE_NSE,
                               tradingsymbol="NIFTY22O0617000PE",
                               transaction_type=self.k.TRANSACTION_TYPE_BUY,
                               quantity=1,
                               product=self.k.PRODUCT_MIS, order_type=self.k.ORDER_TYPE_MARKET,
                               validity=self.k.VALIDITY_DAY,
                               tag="Dodrio")

        if (self.current_price > self.high_price or self.current_price <= self.low_price - (
                2 * (self.high_price - self.low_price))) and self.position_taken is True:
            print("Exit position if exists")
            self.position_taken = False
            self.k.place_order(self.k.VARIETY_REGULAR, exchange=self.k.EXCHANGE_NSE,
                               tradingsymbol="NIFTY22O0617000PE",
                               transaction_type=self.k.TRANSACTION_TYPE_SELL,
                               quantity=1,
                               product=self.k.PRODUCT_MIS, order_type=self.k.ORDER_TYPE_MARKET,
                               validity=self.k.VALIDITY_DAY,
                               tag="Dodrio")

    @property
    def current_price(self):
        return self._current_price

    @current_price.setter
    def current_price(self, value):
        self._current_price = value
        self.check_current_price()

    # # NIFTY22O0617000PE
    # def place_order(self):
    #     self.k.place_order(self.k.VARIETY_REGULAR, exchange=self.k.EXCHANGE_NSE,
    #                        tradingsymbol="NIFTY22O0617000PE",
    #                        transaction_type=self.k.TRANSACTION_TYPE_BUY,
    #                        quantity=25,
    #                        product=self.k.PRODUCT_MIS, order_type=self.k.ORDER_TYPE_MARKET,
    #                        validity=self.k.VALIDITY_DAY,
    #                        tag="Dodrio")


if __name__ == '__main__':
    d = Dodrio()
