#!python
import json
import logging
from kiteconnect import KiteConnect
import pickle

from utility.config import API_KEY, ACCESS_TOKEN, API_SECRET
from utility.mis_allowed import mis_allowed
from utility.utility import pickle_read

logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)
# print(kite.login_url())
inst = kite.instruments()

for i in inst:
    if 'NIFTY22O0617000PE' in i['tradingsymbol']:
        print(i)
# data = kite.generate_session("X69YWBeXXfA3qAAFfLJ4ntp6gnKjmoa8", api_secret=API_SECRET)
# print(data)
#
# data = kite.place_order(kite.VARIETY_REGULAR, exchange=kite.EXCHANGE_NSE,
#                    tradingsymbol="JPPOWER",
#                    transaction_type=kite.TRANSACTION_TYPE_BUY,
#                    quantity=1,
#                    product=kite.PRODUCT_MIS, order_type=kite.ORDER_TYPE_MARKET,
#                    validity=kite.VALIDITY_DAY,
#                    tag="Dodrio")
#
# print(data)
# data = kite.exit_order(variety=kite.VARIETY_REGULAR, order_id=220930400489259)
# print(data)
data = kite.place_order(kite.VARIETY_REGULAR, exchange=kite.EXCHANGE_NFO,
                        tradingsymbol="NIFTY22O0617000PE",
                        transaction_type=kite.TRANSACTION_TYPE_BUY,
                        quantity=50,
                        product=kite.PRODUCT_MIS, order_type=kite.ORDER_TYPE_MARKET,
                        validity=kite.VALIDITY_DAY,
                        tag="Dodrio")

print(data)

data = kite.place_order(kite.VARIETY_REGULAR, exchange=kite.EXCHANGE_NFO,
                        tradingsymbol="NIFTY22O0617000PE",
                        transaction_type=kite.TRANSACTION_TYPE_SELL,
                        quantity=50,
                        product=kite.PRODUCT_MIS, order_type=kite.ORDER_TYPE_MARKET,
                        validity=kite.VALIDITY_DAY,
                        tag="Dodrio")

print(data)

# Redirect the user to the login url obtained
# from kite.login_url(), and receive the request_token
# from the registered redirect url after the login flow.
# Once you have the request_token, obtain the access_token
# as follows.

"""
data = kite.generate_session(ACCESS_TOKEN, api_secret=API_SECRET)
kite.set_access_token(ACCESS_TOKEN)
"""

# data = kite.historical_data(878593, "2022-09-27", "2022-09-28", '5minute')
# print(data)
"""
full_data = kite.instruments()
allowed_data = dict()
for i in mis_allowed:
    for j in full_data:
        if j['tradingsymbol'] == i:
            allowed_data[i] = j['instrument_token']
print(allowed_data)

with open('result_old.json', 'w') as fp:
    json.dump(allowed_data, fp)
"""
"""
stocks_list = dict()
ce_list = dict()
pe_list = dict()
fut_list = dict()

for i in full_data:
    if i['instrument_type'] == 'CE':
        ce_list[i['tradingsymbol']] = i['instrument_token']
    elif i['instrument_type'] == 'PE':
        pe_list[i['tradingsymbol']] = i['instrument_token']
    elif i['instrument_type'] == 'EQ':
        stocks_list[i['tradingsymbol']] = i['instrument_token']
    elif i['instrument_type'] == 'FUT':
        fut_list[i['tradingsymbol']] = i['instrument_token']"""

# data = dict()
# for i in full_data:
#     data[i['tradingsymbol']] = i['instrument_token']
# print(data)

# json_object = json.dumps(data, indent=4)

# Writing to sample.json
"""
with open("../dodrio/stockTokens.pkl", "wb") as outfile:
    pickle.dump(stocks_list, outfile)
with open("pe.pkl", "wb") as outfile:
    pickle.dump(pe_list, outfile)
with open("ce.pkl", "wb") as outfile:
    pickle.dump(ce_list, outfile)
with open("fut.pkl", "wb") as outfile:
    pickle.dump(fut_list, outfile)
    

print(pickle_read("../dodrio/stockTokens.pkl"))"""

# with open('../dodrio/stockTokens', 'wb') as f:
#    pickle.dump(stocks_list, f)
'''
data = dict()
with open('data.pkl', 'rb') as f:
    data = pickle.load(f)
print(data)
'''
'''

for i in data:
    print(i['close'])
test = []
for i in data[-5:]:
    test.append(i['close'])

print(test)
last_close = test[-1]
sma = sum(test)/5
print(sma)
smoothing_constant = 2 / (5 + 1)

print(smoothing_constant)
ema = (last_close - sma) * smoothing_constant + sma
print(ema)
'''
'''
# Place an order
try:
    order_id = kite.place_order(variety=kite.VARIETY_REGULAR,
                                tradingsymbol="INFY",
                                exchange=kite.EXCHANGE_NSE,
                                transaction_type=kite.TRANSACTION_TYPE_BUY,
                                quantity=1,
                                order_type=kite.ORDER_TYPE_MARKET,
                                product=kite.PRODUCT_CNC,
                                validity=kite.VALIDITY_DAY)

    logging.info("Order placed. ID is: {}".format(order_id))
except Exception as e:
    logging.info("Order placement failed: {}".format(e.message))

# Fetch all orders
kite.orders()

# Get instruments


# Place an mutual fund order

kite.place_mf_order(
    tradingsymbol="INF090I01239",
    transaction_type=kite.TRANSACTION_TYPE_BUY,
    amount=5000,
    tag="mytag"
)


# Cancel a mutual fund order
kite.cancel_mf_order(order_id="order_id")


# Get mutual fund instruments
kite.mf_instruments()

'''
