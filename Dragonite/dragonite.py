from kiteconnect import KiteConnect
import pandas as pd
from datetime import datetime, timedelta
from utility.config import ACCESS_TOKEN, API_KEY
import schedule


class Dragonite:
    def __init__(self):
        self.order_id = None
        self.k = KiteConnect(api_key=API_KEY)
        self.k.set_access_token(ACCESS_TOKEN)
        schedule.every().minute.do(self.launch)
        while True:
            schedule.run_pending()

    def launch(self):
        d = self.fill_RSI(3)
        e = self.simple_moving_average(d)
        current_rsi = e['RSI'].iloc[-1]
        current_sma = e['SMA_RSI'].iloc[-1]

        if (current_rsi - current_sma) > 0.5 and self.order_id is None:
            print("Dragonite Buy")
            self.order_id = self.k.place_order(self.k.VARIETY_REGULAR, exchange=self.k.EXCHANGE_NSE,
                                               tradingsymbol="IGL",
                                               transaction_type=self.k.TRANSACTION_TYPE_BUY,
                                               quantity=1,
                                               product=self.k.PRODUCT_MIS, order_type=self.k.ORDER_TYPE_MARKET,
                                               validity=self.k.VALIDITY_DAY, tag="Dragonite Buy")
            print(f"Dragonite Buy order id {self.order_id}")
        elif (current_rsi - current_sma) > 0.5 and self.order_id is not None:
            print("Dragonite Already bought")
        elif 0 < (current_rsi - current_sma) < 0.5 or current_rsi == current_sma:
            print("Dragonite Don't do anything")
        elif current_rsi < current_sma and self.order_id is not None:
            print(f"Dragonite Exit with order id {self.order_id}")
            self.k.place_order(self.k.VARIETY_REGULAR, exchange=self.k.EXCHANGE_NSE,
                          tradingsymbol="IGL",
                          transaction_type=self.k.TRANSACTION_TYPE_SELL,
                          quantity=1,
                          product=self.k.PRODUCT_MIS, order_type=self.k.ORDER_TYPE_MARKET,
                          validity=self.k.VALIDITY_DAY, tag="Dragonite Sell")
            self.order_id = None
        elif current_rsi < current_sma and self.order_id is None:
            print("Dragonite Not yet bought")
        else:
            print("Dragonite A case is missing dude!")

    def get_historicaldata(self, token=2883073):
        enddate = datetime.now()
        startdate = enddate - timedelta(days=60)
        df = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        try:
            data = self.k.historical_data(token, startdate, enddate, "minute", oi=1)
            df = pd.DataFrame.from_dict(data, orient='columns', dtype=None)
            if not df.empty:
                df = df[['date', 'open', 'high', 'low', 'close', 'volume', 'oi']]
                df['date'] = df['date'].astype(str).str[:-6]
            else:
                print("Error in getting historical data")
        except Exception as e:
            print("Error in getting historical data", e)
        return df

    def fill_RSI(self, interval):
        df = self.get_historicaldata()
        delta = df['close'].diff()
        up, down = delta.copy(), delta.copy()
        up[up < 0] = 0
        down[down > 0] = 0
        rUp = up.ewm(com=interval - 1, adjust=False).mean()
        rDown = down.ewm(com=interval - 1, adjust=False).mean().abs()

        df['RSI'] = 100 - 100 / (1 + rUp / rDown)
        df['RSI'].fillna(0, inplace=True)
        return df

    def simple_moving_average(self, df):
        df['SMA_RSI'] = df['RSI'].rolling(window=10).mean()
        df['SMA_RSI'].fillna(0, inplace=True)
        return df
