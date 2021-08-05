from observer_abstract import Observer, Subject
from data_models.stock import Stock
from utility import *
from data_models.tick import Tick


class HandleStockData(Observer):
    _stock_dict = dict()

    def __init__(self):
        self._all_stocks = load_all_stock_data()
        self._stock_dict = {**self._get_large_cap_stock_data(), **self._get_mid_cap_stock_data()}

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
                mid_cap_stock_dict[self._all_stocks[f"{i}-BE"][INSTRUMENT_TOKEN]] = Stock(self._all_stocks[f"{i}-BE"][INSTRUMENT_TOKEN])
        return mid_cap_stock_dict

    @property
    def stock_data(self):
        return self._stock_dict

    def update(self, subject: Subject):
        t = Tick(subject.stock_info)
        self._stock_dict[t.instrument_token].handle_tick(t)
