"""
Use 8 SMA, 50 SMA and 200 SMA

buy when 8 SMA > 50 SMA > 200 SMA

sell when 2 SMA < 50 SMA
"""
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


class Dodrio:
    def __init__(self):
        self.k = KiteConnect(api_key=API_KEY)
        self.k.set_access_token(ACCESS_TOKEN)
        self.stock_interval = INTERVAL_DAY
        assert self.stock_interval in INTERVAL_DAY_RATIO.keys()
        self.stock_historical_days = INTERVAL_DAY_RATIO[self.stock_interval]
        self.stock_token = 0
        self.seg_stocks = list()
        self.large_stocks = pickle_read("../files/large_cap_instrument_tokens")
        self.df = None
        self.rsi_column = 'RSI_close'
        self.sma_8_column = '8_SMA_RSI'
        self.sma_50_column = '50_SMA_RSI'
        self.sma_200_column = '200_SMA_RSI'
        self.today_stock_data = dict()
        self.get_sma()
        print(self.seg_stocks)


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

    def get_sma(self):
        for key, val in self.large_stocks.items():
            self.stock_token = val
            self.df = self.get_historical_data()
            self.fill_8_simple_moving_average()
            self.fill_50_simple_moving_average()
            self.fill_200_simple_moving_average()
            self.today_stock_data[key] = {'close': self.df['close'].iloc[-1],
                                          self.sma_8_column: self.df[self.sma_8_column].iloc[-1],
                                          self.sma_50_column: self.df[self.sma_50_column].iloc[-1],
                                          self.sma_200_column: self.df[self.sma_200_column].iloc[-1]}
            self.segregate_stocks(key,
                                  self.df[self.sma_8_column].iloc[-1],
                                  self.df[self.sma_50_column].iloc[-1],
                                  self.df[self.sma_200_column].iloc[-1])

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


if __name__ == '__main__':
    d = Dodrio()
    #yesterday = ['KOTAKBANK', 'ITC', 'MARUTI', 'JSWSTEEL', 'ADANIGREEN', 'BAJAJ-AUTO', 'ZOMATO', 'M&M', 'DRREDDY', 'MOTHERSUMI', 'CADILAHC', 'UPL', 'INDUSTOWER', 'SAIL', 'HEROMOTOCO', 'AUROPHARMA', 'NMDC', 'GUJGASLTD', 'LUPIN', 'BANDHANBNK', 'BIOCON', 'BOSCHLTD', 'PNB', 'IOB', 'TATACOMM', 'JINDALSTEL', 'ASHOKLEY', 'BHARATFORG', 'AUBANK', 'LAURUSLABS', 'MRF', 'KANSAINER', 'PETRONET', 'RUCHI', 'IDFCFIRSTB', 'YESBANK', 'GICRE', 'IRFC', 'SUNDARMFIN', 'ABCAPITAL', 'GLAXO', 'BANKINDIA', 'WHIRLPOOL', 'TVSMOTOR', 'BAYERCROP', 'RAMCOCEM', 'COROMANDEL', 'UNIONBANK', 'DIXON', 'ENDURANCE', 'SUNTV', 'SUMICHEM', 'L&TFH', 'MINDAIND', 'ALKYLAMINE', 'IDEA', 'BHEL', 'LICHSGFIN']

    #today = ['KOTAKBANK', 'MARUTI', 'JSWSTEEL', 'ADANIGREEN', 'BAJAJ-AUTO', 'ZOMATO', 'M&M', 'DRREDDY', 'MOTHERSUMI', 'GLAND', 'CADILAHC', 'UPL', 'INDUSTOWER', 'SAIL', 'HEROMOTOCO', 'AUROPHARMA', 'NMDC', 'GUJGASLTD', 'LUPIN', 'BANDHANBNK', 'BIOCON', 'IOB', 'TATACOMM', 'JINDALSTEL', 'ASHOKLEY', 'BHARATFORG', 'AUBANK', 'LAURUSLABS', 'MRF', 'KANSAINER', 'PETRONET', 'RUCHI', 'IDFCFIRSTB', 'YESBANK', 'GICRE', 'IRFC', 'SUNDARMFIN', 'ABCAPITAL', 'GLAXO', 'BANKINDIA', 'WHIRLPOOL', 'TVSMOTOR', 'BAYERCROP', 'RAMCOCEM', 'COROMANDEL', 'UNIONBANK', 'DIXON', 'ENDURANCE', 'SUNTV', 'SUMICHEM', 'L&TFH', 'MINDAIND', 'ALKYLAMINE', 'IDEA', 'BHEL', 'LICHSGFIN']
    # today = ['KOTAKBANK', 'MARUTI', 'JSWSTEEL', 'ADANIGREEN', 'BAJAJ-AUTO', 'ZOMATO', 'M&M', 'DRREDDY', 'MOTHERSUMI', 'GLAND', 'CADILAHC', 'UPL', 'INDUSTOWER', 'SAIL', 'HEROMOTOCO', 'AUROPHARMA', 'NMDC', 'GUJGASLTD', 'LUPIN', 'BANDHANBNK', 'BIOCON', 'IOB', 'TATACOMM', 'JINDALSTEL', 'ASHOKLEY', 'BHARATFORG', 'AUBANK', 'LAURUSLABS', 'MRF', 'KANSAINER', 'PETRONET', 'RUCHI', 'IDFCFIRSTB', 'YESBANK', 'GICRE', 'IRFC', 'SUNDARMFIN', 'ABCAPITAL', 'GLAXO', 'BANKINDIA', 'WHIRLPOOL', 'TVSMOTOR', 'BAYERCROP', 'RAMCOCEM', 'COROMANDEL', 'UNIONBANK', 'DIXON', 'ENDURANCE', 'SUNTV', 'SUMICHEM', 'L&TFH', 'MINDAIND', 'ALKYLAMINE', 'IDEA', 'BHEL', 'LICHSGFIN']
    # today = ['KOTAKBANK', 'MARUTI', 'JSWSTEEL', 'ADANIGREEN', 'BAJAJ-AUTO', 'ZOMATO', 'BPCL', 'M&M', 'DRREDDY', 'MOTHERSUMI', 'GLAND', 'MUTHOOTFIN', 'CADILAHC', 'UPL', 'INDUSTOWER', 'SAIL', 'HEROMOTOCO', 'AUROPHARMA', 'NMDC', 'GUJGASLTD', 'LUPIN', 'BANDHANBNK', 'BIOCON', 'IOB', 'TATACOMM', 'JINDALSTEL', 'ASHOKLEY', 'BHARATFORG', 'AUBANK', 'LAURUSLABS', 'MRF', 'EMBASSY', 'KANSAINER', 'PETRONET', 'RUCHI', 'IDFCFIRSTB', 'YESBANK', 'GICRE', 'IRFC', 'SUNDARMFIN', 'ABCAPITAL', 'GLAXO', 'BANKINDIA', 'WHIRLPOOL', 'TVSMOTOR', 'BAYERCROP', 'RAMCOCEM', 'COROMANDEL', 'UNIONBANK', 'DIXON', 'ENDURANCE', 'SUNTV', 'SUMICHEM', 'L&TFH', 'MINDAIND', 'ALKYLAMINE', 'IDEA', 'BHEL', 'LICHSGFIN', 'ABFRL', 'VINATIORGA']


    #print(list(set(yesterday) - set(today)))
