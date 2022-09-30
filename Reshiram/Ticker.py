#!python
import json
import logging
import pickle

import pandas as pd
from kiteconnect import KiteTicker
from pandas import json_normalize
from pandas import concat
from db import mis_stocks
from utility.config import API_KEY, ACCESS_TOKEN, TEST_STOCK

logging.basicConfig(level=logging.DEBUG)

# base_dict = {}
# # Initialise
# kws = KiteTicker(API_KEY, ACCESS_TOKEN)
# f = open("result.json")
# data = json.load(f)
# f.close()
#
# all_tokens_list = list(data.values())
#
# for i in all_tokens_list:
#     base_dict[i] = pd.DataFrame(columns=['instrument_token', 'last_price', 'ohlc.open', 'ohlc.high', 'ohlc.low', 'ohlc.close'])


def on_ticks(ws, ticks):
    # Callback to receive ticks.
    print(ticks)
    # df = json_normalize(ticks)
    # df = df[['instrument_token', 'last_price', 'ohlc.open', 'ohlc.high', 'ohlc.low', 'ohlc.close']]
    # token = str(int(df.iloc[0]['instrument_token']))

    # if token in base_dict.keys():
    #     current_df = base_dict[token]
    #     print("Before append")
    #     print(current_df)
    #     print(df)
    #     current_df.loc[len(current_df.index)] = df
    #     print("Now")
    #     print(current_df)
    #     base_dict[token] = current_df
    # else:
    #     base_dict[token] = df
    # print(base_dict)


def on_connect(ws, response):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe([256265])
    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_FULL, [256265])


def on_close(ws, code, reason):
    # On connection close stop the event loop.
    # Reconnection will not happen after executing `ws.stop()`
    ws.stop()


# Assign the callbacks.
# kws.on_ticks = on_ticks
# kws.on_connect = on_connect
# kws.on_close = on_close
#
# # Infinite loop on the main thread. Nothing after this will run.
# # You have to use the pre-defined callbacks to manage subscriptions.
# kws.connect()
