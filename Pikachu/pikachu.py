from datetime import datetime

import schedule
from kiteconnect import KiteConnect

from utility.config import SYMBOL, CHANGE_PERCENTAGE, API_KEY, ACCESS_TOKEN, INSTRUMENT_TOKEN, \
    INTERVAL_15_MINUTE, HIGH, LOW, PIKACHU_LAUNCH_TIME, PIKACHU_SELL_TAG, PIKACHU_BUY_TAG
from utility.utility import pickle_read

"""
This strategy explained at https://www.youtube.com/watch?v=IQeeYv9eYlE
1. At 9:40 start
2. Check Top Losers and Top Gainers from NSE
3. At 9:43, check highest absolute value of change from top losers and top gainers list (prefer stocks above 300)
4. Add the selected stock to watchlist
5. Open 15 minute chart of stock
6. Check candle of 9:30 to 9:45, the second candle in 15 minute chart
7. Set Entry at high of second candle (buffer price of 10 paisa)
8. Set stop loss as lowest point of second candle
9. Set target A as:  Entry + (Entry - stop loss)
10. Once target A achieve, set stop loss as Target A
11. For stock selection of loser side, use same strategy with selling and not buying
"""


class Pikachu:
    def __init__(self):
        self.k = KiteConnect(api_key=API_KEY)
        self._all_stocks = None
        self._use_stock = None
        schedule.every().day.at(PIKACHU_LAUNCH_TIME).do(self.test)
        while True:
            schedule.run_pending()

    def _identify_stock(self):
        self._get_losers_gainers()
        data = self._segregate_data()
        select_stock_symbol = max(data, key=data.get)
        self._use_stock = self._all_stocks[select_stock_symbol]

    def _segregate_data(self):
        values = list(self._all_stocks.values())
        segregated_data = dict()
        for stock in values:
            segregated_data[stock[SYMBOL]] = abs(float(stock[CHANGE_PERCENTAGE]))
        return segregated_data

    def _get_losers_gainers(self):
        self._all_stocks = {**pickle_read("../files/gainers"), **pickle_read("../files/losers")}

    def test(self):
        self._identify_stock()
        all_stock = pickle_read("../files/all_stocks")
        self.k.set_access_token(ACCESS_TOKEN)
        buy = True if float(self._all_stocks[self._use_stock[SYMBOL]][CHANGE_PERCENTAGE]) > 0 else False
        token = all_stock[self._use_stock[SYMBOL]][INSTRUMENT_TOKEN]
        data = self.k.historical_data(token,
                                      datetime(datetime.now().date().year, datetime.now().date().month,
                                               datetime.now().date().day - 1, 9, 30, 0),
                                      datetime(datetime.now().date().year, datetime.now().date().month,
                                               datetime.now().date().day - 1, 9, 45, 0),
                                      INTERVAL_15_MINUTE)
        if buy:
            print(data)
            entry = data[0][HIGH]
            stop_loss = data[0][LOW]
            target = entry + (entry - stop_loss)
            buy_square_off = entry - stop_loss
            print(f"Buying: {self._use_stock[SYMBOL]} at entry: {entry} with stop_loss {stop_loss}"
                  f"with square_off {buy_square_off} with target kept as {target}")

            self.k.place_order(self.k.VARIETY_BO, exchange=self.k.EXCHANGE_NSE, tradingsymbol=self._use_stock[SYMBOL],
                               transaction_type=self.k.TRANSACTION_TYPE_BUY, quantity=int(2000 / entry),
                               product=self.k.PRODUCT_BO, order_type=self.k.ORDER_TYPE_SL,
                               validity=self.k.VALIDITY_DAY, trigger_price=entry, squareoff=buy_square_off,
                               stoploss=stop_loss, trailing_stoploss=1, tag=PIKACHU_BUY_TAG)

        else:
            entry = data[0][LOW]
            stop_loss = data[0][HIGH]
            target = entry - (stop_loss - entry)
            sell_square_off = stop_loss - entry
            print(f"Selling: {self._use_stock[SYMBOL]} at entry: {entry} with stop_loss {stop_loss}"
                  f"with square_off {sell_square_off}with target kept as {target}")

            self.k.place_order(self.k.VARIETY_BO, exchange=self.k.EXCHANGE_NSE, tradingsymbol=self._use_stock[SYMBOL],
                               transaction_type=self.k.TRANSACTION_TYPE_SELL, quantity=int(2000 / entry),
                               product=self.k.PRODUCT_BO, order_type=self.k.ORDER_TYPE_SL,
                               validity=self.k.VALIDITY_DAY, trigger_price=entry, squareoff=sell_square_off,
                               stoploss=stop_loss, trailing_stoploss=1, tag=PIKACHU_SELL_TAG)


if __name__ == '__main__':
    Pikachu()
