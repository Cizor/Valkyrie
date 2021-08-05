import logging

from kiteconnect import KiteConnect
from utility.config import *
import pickle

from utility.utility import pickle_write

logging.basicConfig(level=logging.DEBUG)


class KiteSession():
    """This class maintains Kite session"""

    def __init__(self):
        print("I am init")
        logging.debug("Starting Kite session")
        self.k = KiteConnect(api_key=API_KEY)
        # print(self.k.login_url())
        self._set_access_token_k()
        self._prepare_all_files()
        # self.test()

    def _set_access_token_k(self):
        """This function returns sets access token for kite session"""
        logging.debug("To Kite, setting access token")
        self.k.set_access_token(ACCESS_TOKEN)

    def _prepare_all_files(self):
        """This function prepares all db files"""
        logging.debug("Preparing db files")
        self.data = self._get_all_k()
        self._prepare_all_instruments_file()
        self._prepare_all_instrument_tokens_file()
        self._prepare_large_cap_instrument_tokens_file()

    def _get_all_k(self):
        """This function returns all instrument data from kite and stores as JSON with tradingsymbol as key"""
        logging.debug("From Kite, fetching all instruments...")
        data = self.k.instruments()
        data_json = dict()
        for i in data:
            data_json[i[TRADING_SYMBOL]] = i
        return data_json

    def _prepare_all_instruments_file(self):
        """This function stores all stock (instruments) data into DB_FILE"""
        logging.debug("Preparing DB_FILE")
        pickle_write(DB_FILE, self.data)

    def _prepare_all_instrument_tokens_file(self):
        """This functions prepares INSTRUMENT_TOKENS_FILE"""
        logging.debug("Preparing INSTRUMENT_TOKENS_LIST_FILE")
        token_dict = dict()
        for key, val in self.data.items():
            token_dict[key] = val[INSTRUMENT_TOKEN]
        pickle_write(INSTRUMENT_TOKENS_FILE, token_dict)

    def _prepare_large_cap_instrument_tokens_file(self):
        """This function creates file with dictionary of large cap tokens"""
        logging.debug("Preparing LARGE_CAP_INSTRUMENT_TOKENS_LIST_FILE")
        large_cap_token_dict = dict()
        for large_cap_symbol in pickle.load(open(LARGE_CAP_FILE, 'rb')):
            large_cap_token_dict[large_cap_symbol] = self.data[large_cap_symbol][INSTRUMENT_TOKEN]
        pickle_write(LARGE_CAP_INSTRUMENT_TOKENS_FILE, large_cap_token_dict)

    def _prepare_mid_cap_instrument_tokens_file(self):
        """This function creates file with dictionary of mid cap tokens"""
        logging.debug("Preparing MID_CAP_INSTRUMENT_TOKENS_LIST_FILE")
        mid_cap_token_dict = dict()
        for mid_cap_symbol in pickle.load(open(MID_CAP_FILE, 'rb')):
            mid_cap_token_dict[mid_cap_symbol] = self.data[mid_cap_symbol][INSTRUMENT_TOKEN]
        pickle_write(MID_CAP_INSTRUMENT_TOKENS_FILE, mid_cap_token_dict)

    def test(self):
        from utility.utility import pickle_read
        from datetime import datetime
        all_stock = pickle_read(DB_FILE)
        token = all_stock['RELIANCE']['instrument_token']
        data = self.k.historical_data(token, datetime(2021, 8, 5, 10, 15, 0), datetime(2021, 8, 5, 10, 30, 0), "15minute")
        highs = list()
        # 2112.7 with minute
        # 2112.7 with 5minute
        # 2112.7 with 15minute
        for i in data:
            highs.append(i['high'])
        print(highs)
        print(max(highs))

