import pickle
from utility.config import *


def pickle_read(file_name):
    return pickle.load(open(file_name, 'rb'))


def pickle_write(file_name, value):
    with open(file_name, "wb") as db:
        pickle.dump(value, db)


def load_all_stock_data():
    """This function loads all stock data. If contents in DB_FILE is changed by ticker or any other module,
    it will load with those new changes."""
    return pickle_read(DB_FILE)
