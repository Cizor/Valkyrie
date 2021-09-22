from mongoengine import connect, Document, StringField, ListField, DictField, IntField, FloatField
from pymongo import MongoClient
from utility.utility import pickle_read
from pprint import pprint


# data = pickle_read("../files/all_stocks")
# pprint(data["ITC"])
"""
{'exchange': 'NSE',
 'exchange_token': '1660',
 'expiry': '',
 'instrument_token': 424961,
 'instrument_type': 'EQ',
 'last_price': 0.0,
 'lot_size': 1,
 'name': 'ITC',
 'segment': 'NSE',
 'strike': 0.0,
 'tick_size': 0.05,
 'tradingsymbol': 'ITC'}
"""


class Stock(Document):
    exchange = StringField(required=True)
    exchange_token = StringField(required=True)
    expiry = StringField(required=True)
    instrument_token = IntField(required=True)
    instrument_type = StringField(required=True)
    last_price = FloatField(required=True)
    lot_size = IntField(required=True)
    name = StringField(required=True)
    segment = StringField(required=True)
    strike = FloatField(required=True)
    tick_size = FloatField(required=True)
    tradingsymbol = StringField(required=True)

    def __repr__(self):
        return self.name


if __name__ == '__main__':
    dc = connect(db="market", host="localhost", port=27017)

    '''
    data = {'exchange': 'NSE', 'exchange_token': '1660', 'expiry': '', 'instrument_token': 424961,
            'instrument_type': 'EQ', 'last_price': 0.0, 'lot_size': 1, 'name': 'ITC', 'segment': 'NSE',
            'strike': 0.0, 'tick_size': 0.05, 'tradingsymbol': 'ITC'}
    stock = Stock(**data)
    stock.save()
    '''
    print(dc)

