import logging
from data_models.tick_list import TickList
from kiteconnect import KiteTicker
from abstracts.observer_abstract import Observer, Subject
from framework.handle_stock_data import HandleStockData
from utility.config import API_KEY, ACCESS_TOKEN, LARGE_CAP_INSTRUMENT_TOKENS_FILE, MID_CAP_INSTRUMENT_TOKENS_FILE
from utility.utility import pickle_read

logging.basicConfig(level=logging.DEBUG)


# Initialise
class KTicker(Subject):
    _observers = list()

    def __init__(self):
        self.handle_stocks = HandleStockData()
        self.kws = KiteTicker(API_KEY, ACCESS_TOKEN)
        # Assign the callbacks.
        self.kws.on_ticks = self.on_ticks
        self.kws.on_connect = self.on_connect
        self.kws.on_close = self.on_close
        self._observers.append(self.handle_stocks)

        # Infinite loop on the main thread. Nothing after this will run.
        # You have to use the pre-defined callbacks to manage subscriptions.
        self.kws.connect()

    def on_ticks(self, ws, ticks):
        """
        Callback to receive ticks.
        """
        # logging.debug("Ticks: {}".format(ticks))
        self.stock_info = TickList(ticks)
        self.notify()

    def on_connect(self, ws, response):
        """
        Callback on successful connect.
        """
        # Subscribe to a list of instrument_tokens
        ws.subscribe([*list(self.get_large_cap_instrument_token_list().values()),
                     *list(self.get_mid_cap_instrument_token_list())])
        ws.set_mode(ws.MODE_FULL, [*list(self.get_large_cap_instrument_token_list().values()),
                    *list(self.get_mid_cap_instrument_token_list())])

    def on_close(self, ws, code, reason):
        """
        On connection close stop the main loop
        """
        # Reconnection will not happen after executing `ws.stop()`
        ws.stop()

    def get_large_cap_instrument_token_list(self):
        """
        Gets list of instrument tockens of large caps
        """
        return pickle_read(LARGE_CAP_INSTRUMENT_TOKENS_FILE)

    def get_mid_cap_instrument_token_list(self):
        """
        Gets list of instrument tockens of large caps
        """
        return pickle_read(MID_CAP_INSTRUMENT_TOKENS_FILE)

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
