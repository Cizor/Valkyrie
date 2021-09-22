import pprint
import time

from data_models.stock import Stock
from utility.config import INSTRUMENT_TOKEN
from utility.utility import load_all_stock_data, pickle_read, load_mis_allowed_stocks
import multiprocessing
import psutil


class HandleStockData():
    def __init__(self):
        self._all_stocks = load_all_stock_data()
        self._stock_list = load_mis_allowed_stocks()
        self._stock_instrument_token_db = dict()
        self._hold_stock_objects_list = list()
        self._pr_list = list()
        self._thread_list = list()
        self.create_stock_objects()
        self.run_threads()

    def create_stock_objects(self):
        for i in self._stock_list:
            self._stock_instrument_token_db[i] = self._all_stocks[i][INSTRUMENT_TOKEN]
        self.create_all_stock_objects()

    def create_all_stock_objects(self):
        tokens = list(self._stock_instrument_token_db.values())
        for token in tokens:
            stock = Stock(token)
            self._hold_stock_objects_list.append(stock)
            pr = multiprocessing.Process(target=stock.run_thread)
            self._thread_list.append(pr)


    def run_threads(self):
        for i in self._thread_list[0:1]:
            i.start()
            self._pr_list.append(i.pid)
        print("Going to sleep")
        time.sleep(5)
        print("Ok complete this")
        for i in self._hold_stock_objects_list:
            print("Called stop")
            i.websocket.stop()
            print("Came out")
        print("Ok  just termionate")
        for i in self._thread_list[0:1]:
            i.terminate()
        print("If process")
        #time.sleep(5)
        #[i.join() for i in self._thread_list[0:10]]





    """
    def _get_large_cap_stock_data(self):
        large_cap_data = pickle_read(LARGE_CAP_FILE)
        large_cap_stock_dict = dict()
        for i in large_cap_data:
            large_cap_stock_dict[self._all_stocks[i][INSTRUMENT_TOKEN]] = Stock(self._all_stocks[i][INSTRUMENT_TOKEN])
        return large_cap_stock_dict

    def _get_mid_cap_stock_data(self):
        mid_cap_data = pickle_read(MID_CAP_FILE)
        mid_cap_stock_dict = dict()
        for i in mid_cap_data:
            try:
                mid_cap_stock_dict[self._all_stocks[i][INSTRUMENT_TOKEN]] = Stock(self._all_stocks[i][INSTRUMENT_TOKEN])
            except KeyError:
                # Some stock symbols have -BE at end by TickerTape data didn't had that so handling
                try:
                    mid_cap_stock_dict[self._all_stocks[f"{i}-BE"][INSTRUMENT_TOKEN]] = Stock(self._all_stocks[f"{i}-BE"][INSTRUMENT_TOKEN])
                except KeyError:
                    pass
        return mid_cap_stock_dict
    

    @property
    def stock_data(self):
        return self._stock_list

    def update(self, subject: Subject):
        self._tick_objects.update(subject.stock_info.get_tick_list_objects())
        self.sync_stock_data()


    def sync_stock_data(self):
        # consistent_data = all(item in self._stock_dict.keys() for item in self._tick_objects.keys())
        # if consistent_data:
        #    for key, val in self._tick_objects.items():
        #        self._stock_dict[key].handle_tick(val)
        # else:
        #    raise ValueError("Stock data may need to be updated. Handle automatically?")
        #
        for key, val in self._tick_objects.items():
            self._stock_dict[key].handle_tick(val)

        self.testing_data = self._stock_dict
        self.notify()
    """


if __name__ == "__main__":
    hs = HandleStockData()
    hs.create_stock_objects()
