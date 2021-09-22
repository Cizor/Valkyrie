from kiteconnect import KiteConnect
from utility.config import *
from utility.utility import pickle_read
import pprint
import pandas as pd
from datetime import datetime, timedelta
from pymongo import MongoClient


class Charmander:
    def __init__(self):
        self.k = KiteConnect(api_key=API_KEY)
        self.k.set_access_token(ACCESS_TOKEN)
        self.mongo_client = MongoClient()
        self.rsi_interval = 25
        self.rsi_ma_window = 10
        self.stock_interval = INTERVAL_DAY
        assert self.stock_interval in INTERVAL_DAY_RATIO.keys()
        self.stock_historical_days = INTERVAL_DAY_RATIO[self.stock_interval]
        self.large_stocks = pickle_read("../files/large_cap_instrument_tokens")
        self.stock_token = 0
        self.df = None
        self.rsi_column = 'RSI_' + str(self.rsi_interval)
        self.sma_column = 'SMA_RSI'
        self.today_stock_data = dict()
        self.below_40_rsi_sma_stocks = list()
        self.get_rsi_and_sma()
        print(self.below_40_rsi_sma_stocks)
        self.today_stock_data['segregated_stocks'] = {"segregated_stocks_list": self.below_40_rsi_sma_stocks}
        # self.send_to_mongo()
        # self.get_crossed_stocks_for_buy()

    def get_rsi_and_sma(self):
        for key, val in self.large_stocks.items():
            self.stock_token = val
            self.df = self.get_historical_data()
            self.fill_RSI()
            self.fill_simple_moving_average()
            print(key, self.df[self.rsi_column].iloc[-1], self.df[self.sma_column].iloc[-1])
            self.today_stock_data[key] = {self.rsi_column: self.df[self.rsi_column].iloc[-1],
                                          self.sma_column: self.df[self.sma_column].iloc[-1]}
            self.segregate_stocks(key, self.df[self.rsi_column].iloc[-1], self.df[self.sma_column].iloc[-1])

    def segregate_stocks(self, key, rsi, sma):
        if rsi < 40 and 40 > sma > rsi:
            self.below_40_rsi_sma_stocks.append(key)

    def send_to_mongo(self):
        db = self.mongo_client["RSI_SMA_DAILY"]
        rs_sma_coll = db[f"{str(datetime.today().date())}"]
        post = rs_sma_coll.insert_one(self.today_stock_data)

    def get_crossed_stocks_for_buy(self):
        db = self.mongo_client["RSI_SMA_DAILY"]
        yesterday_stocks = db[f"{str(datetime.today().date() - timedelta(days=1))}"].find_one()['segregated_stocks']['segregated_stocks_list']
        today_stocks = db[f"{str(datetime.today().date())}"].find_one()['segregated_stocks']['segregated_stocks_list']
        crossed_stocks = list(set(yesterday_stocks) - set(today_stocks))
        print(f"Yesterday's stocks were: {yesterday_stocks}")
        print(f"Today's stocks are: {today_stocks}")
        print(f"Crossed Stocks to buy tomorrow: f{crossed_stocks}")

    def get_historical_data(self):
        enddate = datetime.now() - timedelta(days=3)
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

    def fill_RSI(self):
        delta = self.df['close'].diff()
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        rUp = up.ewm(com=self.rsi_interval - 1, adjust=False).mean()
        rDown = down.ewm(com=self.rsi_interval - 1, adjust=False).mean().abs()

        self.df[self.rsi_column] = 100 - 100 / (1 + rUp / rDown)
        self.df[self.rsi_column].fillna(len(self.df), inplace=True)

    def fill_simple_moving_average(self):
        self.df[self.sma_column] = self.df[self.rsi_column].rolling(window=self.rsi_ma_window).mean()
        self.df[self.sma_column].fillna(len(self.df), inplace=True)


if __name__ == '__main__':
    c = Charmander()
