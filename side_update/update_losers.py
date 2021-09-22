from nsetools import Nse

from utility.config import LOSERS_DICT_FILE, SYMBOL
from utility.utility import pickle_write, pickle_read


class UpdateLosers():
    def __init__(self):
        self.nse = Nse()

    def get_data(self):
        losers_list = self.nse.get_top_losers()
        losers_stock_dict = dict()
        for stock in losers_list:
            losers_stock_dict[stock[SYMBOL]] = stock
        print(losers_stock_dict.keys())
        # pickle_write(LOSERS_DICT_FILE, losers_stock_dict)
        return losers_stock_dict
