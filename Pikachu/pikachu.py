from datetime import datetime
from math import floor
import schedule
from kiteconnect import KiteConnect

from utility.config import SYMBOL, API_KEY, ACCESS_TOKEN, INSTRUMENT_TOKEN, \
    INTERVAL_15_MINUTE, HIGH, LOW, PIKACHU_LAUNCH_TIME, PIKACHU_SELL_TAG, PIKACHU_BUY_TAG, NET_PRICE, \
    PIKACHU_TARGET_FILE
from utility.utility import pickle_read, pickle_write
from side_update.update_gainers import UpdateGainers
from side_update.update_losers import UpdateLosers

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
        self.loosers = dict()
        self.gainers = dict()
        self._all_stocks = None
        self._use_stock = None
        schedule.every().day.at(PIKACHU_LAUNCH_TIME).do(self.test)
        while True:
           schedule.run_pending()


    def _identify_stock(self):
        self._get_losers_gainers()
        data = self._segregate_data()
        select_stock_symbol = max(data, key=data.get)
        self._all_stocks = {**self.gainers, **self.loosers}
        self._use_stock = self._all_stocks[select_stock_symbol]

    def _segregate_data(self):
        values = list(self._all_stocks.values())
        segregated_data = dict()
        for stock in values:
            segregated_data[stock[SYMBOL]] = abs(float(stock[NET_PRICE]))
        return segregated_data

    def _get_losers_gainers(self):
        gainers_data = UpdateGainers()
        self.gainers = gainers_data.get_data()
        loosers_data = UpdateLosers()
        self.loosers = loosers_data.get_data()
        print(self.gainers)
        print(self.loosers)
        self._all_stocks = {**self.gainers, **self.loosers}
        # self._all_stocks = {**pickle_read("../files/gainers"), **pickle_read("../files/losers")}

    def mid_test(self):
        print(datetime.now())
        self._get_losers_gainers()
        print(self._all_stocks)

    def test(self):
        self._identify_stock()
        all_stock = pickle_read("files/all_stocks")
        self.k.set_access_token(ACCESS_TOKEN)
        buy = True if float(self._all_stocks[self._use_stock[SYMBOL]][NET_PRICE]) > 0 else False
        token = all_stock[self._use_stock[SYMBOL]][INSTRUMENT_TOKEN]
        data = self.k.historical_data(token,
                                      datetime(datetime.now().date().year, datetime.now().date().month,
                                               datetime.now().date().day, 9, 30, 0),
                                      datetime(datetime.now().date().year, datetime.now().date().month,
                                               datetime.now().date().day, 9, 45, 0),
                                      INTERVAL_15_MINUTE)
        if buy:
            print(data)
            entry = data[0][HIGH]
            stop_loss = data[0][LOW]
            target = entry + (entry - stop_loss)
            buy_square_off = entry - stop_loss

            stock_quantity = self.get_number_stocks_to_buy(self._use_stock[SYMBOL])
            print(f"Buy qunatity: {stock_quantity}")

            print(f"Buying: {self._use_stock[SYMBOL]} at entry: {entry} with stop_loss {stop_loss}"
                  f"with square_off {buy_square_off} with target kept as {target}, Buying {stock_quantity}")
            # pickle_write(PIKACHU_TARGET_FILE, {self._use_stock[SYMBOL]: target})
            """print(self.k.place_order(self.k.VARIETY_CO, exchange=self.k.EXCHANGE_NSE,
                                     tradingsymbol=self._use_stock[SYMBOL],
                                     transaction_type=self.k.TRANSACTION_TYPE_BUY,
                                     quantity=stock_quantity,
                                     product=self.k.PRODUCT_MIS, order_type=self.k.ORDER_TYPE_LIMIT,
                                     validity=self.k.VALIDITY_DAY, price=entry,
                                     tag=PIKACHU_BUY_TAG, trigger_price=stop_loss))"""
            """
            print(self.k.place_order(self.k.VARIETY_CO, exchange=self.k.EXCHANGE_NSE,
                                     tradingsymbol=self._use_stock[SYMBOL],
                                     transaction_type=self.k.TRANSACTION_TYPE_SELL,
                                     quantity=1,
                                     product=self.k.PRODUCT_MIS, order_type=self.k.ORDER_TYPE_LIMIT, trigger_price=stop_loss,
                                     validity=self.k.VALIDITY_DAY, price=target,
                                     tag=PIKACHU_BUY_TAG))
            """



        else:
            entry = data[0][LOW]
            stop_loss = data[0][HIGH]
            target = entry - (stop_loss - entry)
            sell_square_off = stop_loss - entry
            stock_quantity = self.get_number_stocks_to_buy(self._use_stock[SYMBOL])
            print(f"Sell qunatity: {stock_quantity}")
            print(f"Selling: {self._use_stock[SYMBOL]} at entry: {entry} with stop_loss {stop_loss}"
                  f"with square_off {sell_square_off}with target kept as {target}, Selling {stock_quantity}")
            # pickle_write(PIKACHU_TARGET_FILE, {self._use_stock[SYMBOL]: target})
            """print(self.k.place_order(self.k.VARIETY_CO, exchange=self.k.EXCHANGE_NSE,
                                     tradingsymbol=self._use_stock[SYMBOL],
                                     transaction_type=self.k.TRANSACTION_TYPE_SELL,
                                     quantity=stock_quantity,
                                     product=self.k.PRODUCT_MIS, order_type=self.k.ORDER_TYPE_LIMIT,
                                     validity=self.k.VALIDITY_DAY, price=entry,
                                     trigger_price=stop_loss, tag=PIKACHU_SELL_TAG))"""
            # print(self.k.place_order(self.k.VARIETY_CO, exchange=self.k.EXCHANGE_NSE,
            #                         tradingsymbol=self._use_stock[SYMBOL],
            #                         transaction_type=self.k.TRANSACTION_TYPE_BUY,
            #                         quantity=1,
            #                         product=self.k.PRODUCT_MIS, order_type=self.k.ORDER_TYPE_LIMIT, trigger_price=3,
            #                         validity=self.k.VALIDITY_DAY, price=target, tag=PIKACHU_SELL_TAG))

    def current_cash(self):
        data = self.k.margins(self.k.MARGIN_EQUITY)
        return floor(data['net'])

    def get_stock_margin_required(self, symbol):
        order_param_single = [{
            "exchange": "NSE",
            "tradingsymbol": symbol,
            "transaction_type": "BUY",
            "variety": "regular",
            "product": "MIS",
            "order_type": "MARKET",
            "quantity": 1,
            "price": 0,
            "trigger_price": 0
        }]
        data = self.k.order_margins(order_param_single)
        return data[0]['total']

    def get_number_stocks_to_buy(self, symbol):
        try:
            stock_number = floor(self.current_cash() / self.get_stock_margin_required(symbol))
            return stock_number
        except ZeroDivisionError:
            print("Market sent 0 so....")
            return 1

# if __name__ == '__main__':
#    Pikachu()
