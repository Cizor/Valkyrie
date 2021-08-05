from abstracts.observer_abstract import Observer, Subject
from data_models.stock import Stock
from test_strategy.testing import Testing
from utility.config import LARGE_CAP_FILE, INSTRUMENT_TOKEN, MID_CAP_FILE
from utility.utility import load_all_stock_data, pickle_read


class HandleStockData(Observer, Subject):
    _stock_dict = dict()
    _tick_objects = dict()
    _observers = list()

    def __init__(self):
        self._all_stocks = load_all_stock_data()
        self._stock_dict = {**self._get_large_cap_stock_data(), **self._get_mid_cap_stock_data()}
        self.testing = Testing(self._stock_dict)
        self._observers.append(self.testing)

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
        return self._stock_dict

    def update(self, subject: Subject):
        self._tick_objects.update(subject.stock_info.get_tick_list_objects())
        self.sync_stock_data()

    def sync_stock_data(self):
        """
        Update stock data. Uncomment consistent data check to check if stock_data needs to be updated
        :return:
        """
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

    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        """
        Trigger an update in each subscriber.
        """
        for observer in self._observers:
            observer.update(self)

