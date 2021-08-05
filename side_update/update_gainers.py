from nsetools import Nse

from utility.config import GAINERS_DICT_FILE, SYMBOL
from utility.utility import pickle_write, pickle_read


class UpdateGainers(Nse):
    def __init__(self):
        Nse.__init__(self)
        while True:
            pickle_write(GAINERS_DICT_FILE, self.get_data())

    def get_data(self):
        gainers_list = self.get_top_gainers()
        gainers_stock_dict = dict()
        for stock in gainers_list:
            gainers_stock_dict[stock[SYMBOL]] = stock
        return gainers_stock_dict
