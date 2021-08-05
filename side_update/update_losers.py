from nsetools import Nse

from utility.config import LOSERS_DICT_FILE, SYMBOL
from utility.utility import pickle_write, pickle_read


class UpdateLosers(Nse):
    def __init__(self):
        super().__init__()
        while True:
            pickle_write(LOSERS_DICT_FILE, self.get_data())


    def get_data(self):
        losers_list = self.get_top_losers()
        losers_stock_dict = dict()
        for stock in losers_list:
            losers_stock_dict[stock[SYMBOL]] = stock
        return losers_stock_dict
