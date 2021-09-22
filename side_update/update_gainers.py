from nsetools import Nse

from utility.config import GAINERS_DICT_FILE, SYMBOL
from utility.utility import pickle_write, pickle_read


class UpdateGainers():
    def __init__(self):
        self.nse = Nse()

    def get_data(self):
        gainers_list = self.nse.get_top_gainers()
        gainers_stock_dict = dict()
        for stock in gainers_list:
            gainers_stock_dict[stock[SYMBOL]] = stock
        print(gainers_stock_dict.keys())
        # pickle_write(GAINERS_DICT_FILE, gainers_stock_dict)
        return gainers_stock_dict

