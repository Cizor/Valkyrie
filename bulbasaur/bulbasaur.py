from kiteconnect import KiteConnect
from utility.config import *
from utility.utility import pickle_read
import pprint
import pandas as pd
from datetime import datetime, timedelta
from pymongo import MongoClient

"""
Steps of Strategy NR7:
1. Check all large and mid cap stocks 
2. Check if today's candle range is smaller than last 6 candles or not
3. If yes, select it for next day intraday
4. If Next day candle, crosses high of last (7th candle) buy and go long
5. If Next day candle, crosses low of last (7th candle) short sell entire day
"""


class Bulbasaur:
    def __init__(self):
        self.k = KiteConnect(api_key=API_KEY)
        self.k.set_access_token(ACCESS_TOKEN)
        self.all_stocks = pickle_read("../files/large_cap_instrument_tokens")
        self.stock_token = None
        self.stock_interval = INTERVAL_DAY
        self.df = None
        self.test_all_stocks()

    def get_historical_data(self):
        enddate = datetime.now() - timedelta(days=1)
        startdate = enddate - timedelta(days=15)
        df = pd.DataFrame(columns=['date', 'high', 'low'])
        try:
            data = self.k.historical_data(self.stock_token, startdate, enddate, self.stock_interval, oi=1)
            df = pd.DataFrame.from_dict(data, orient='columns', dtype=None)
            if not df.empty:
                df = df[['date', 'high', 'low']]
                df['date'] = df['date'].astype(str).str[:-6]
            else:
                print("Error in getting historical data")
        except Exception as e:
            print("Error in getting historical data", e)
        return df

    def check_seventh_candle(self):
        last_six_candle_ranges = [abs(self.df['high'].iloc[i] - self.df['low'].iloc[i]) for i in range(-7, -1)]
        seventh_range = abs(self.df['high'].iloc[-1] - self.df['low'].iloc[-1])
        return all(x > seventh_range for x in last_six_candle_ranges)

    def test_all_stocks(self):
        nr7_stocks = dict()
        for key, val in self.all_stocks.items():
            self.stock_token = val
            self.df = self.get_historical_data()
            print(f"Testing {key}")
            if self.check_seventh_candle():
                print(f"{key} awesome!")
                nr7_stocks[key] = {"token": self.stock_token,
                                   "high": self.df['high'].iloc[-1],
                                   "low": self.df['low'].iloc[-1]}
        pprint.pprint(nr7_stocks)


if __name__ == '__main__':
    b = Bulbasaur()