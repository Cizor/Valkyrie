from kiteconnect import KiteConnect
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


class Squirtle:
    def __init__(self):
        self.k = KiteConnect(api_key=API_KEY)
        self.k.set_access_token(ACCESS_TOKEN)
        self.stock_interval = INTERVAL_DAY
        assert self.stock_interval in INTERVAL_DAY_RATIO.keys()
        self.stock_historical_days = INTERVAL_DAY_RATIO[self.stock_interval]
        self.stock_token = 0
        self.large_stocks = pickle_read("../files/large_cap_instrument_tokens")
        self.df = None
        self.rsi_interval = 2
        self.rsi_column = 'RSI_close'
        self.sma_10_column = '10_SMA_RSI'
        self.sma_200_column = '200_SMA_RSI'
        self.rsi_10_ma_window = 10
        self.rsi_200_ma_window = 200
        self.today_stock_data = dict()
        self.get_rsi_and_sma()


    def get_historical_data(self):
        enddate = datetime.now()
        startdate = enddate - timedelta(days=self.stock_historical_days)
        df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        try:
            data = self.k.historical_data(self.stock_token, startdate, enddate, self.stock_interval, oi=1)
            df = pd.DataFrame.from_dict(data, orient='columns', dtype=None)
            if not df.empty:
                df = df[['date', 'open', 'high', 'low', 'close', 'volume', 'oi']]
                df['date'] = df['date'].astype(str).str[:-6]
            else:
                print("Error in getting historical data")
        except Exception as e:
            print("Error in getting historical data", e)
        return df

    def get_rsi_and_sma(self):
        for key, val in self.large_stocks.items():
            self.stock_token = val
            self.df = self.get_historical_data()
            self.fill_RSI()
            self.fill_10_simple_moving_average()
            self.fill_200_simple_moving_average()
            self.today_stock_data[key] = {'close': self.df['close'].iloc[-1],
                                          self.rsi_column: self.df[self.rsi_column].iloc[-1],
                                          self.sma_10_column: self.df[self.sma_10_column].iloc[-1],
                                          self.sma_200_column: self.df[self.sma_200_column].iloc[-1]}
            self.segregate_stocks(key, self.df['close'].iloc[-1],
                                  self.df['high'].iloc[-1],
                                  self.df[self.rsi_column].iloc[-1],
                                  self.df[self.sma_10_column].iloc[-1],
                                  self.df[self.sma_200_column].iloc[-1])

    def segregate_stocks(self, key, close_price, high, rsi, sma_10, sma_200):
        if high > sma_10 > close_price > sma_200 and rsi < 10:
            print(key, sma_10, sma_200, rsi, close_price, high)

    def fill_RSI(self):
        delta = self.df['close'].diff()
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        rUp = up.ewm(com=self.rsi_interval - 1, adjust=False).mean()
        rDown = down.ewm(com=self.rsi_interval - 1, adjust=False).mean().abs()

        self.df[self.rsi_column] = 100 - 100 / (1 + rUp / rDown)
        self.df[self.rsi_column].fillna(len(self.df), inplace=True)

    def fill_10_simple_moving_average(self):
        self.df[self.sma_10_column] = self.df['close'].rolling(window=self.rsi_10_ma_window).mean()
        self.df[self.sma_10_column].fillna(len(self.df), inplace=True)

    def fill_200_simple_moving_average(self):
        self.df[self.sma_200_column] = self.df['close'].rolling(window=self.rsi_200_ma_window).mean()
        self.df[self.sma_200_column].fillna(len(self.df), inplace=True)


if __name__ == '__main__':
    s = Squirtle()
    """
    RAMCOCEM 1046.935
    DIXON 4289.55
    """