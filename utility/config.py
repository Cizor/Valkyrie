# Initial params
ACCESS_TOKEN = "mLAGNu79NKprhU0q1OXlpXquqJ6F5ZfW"
API_KEY = "05q4h560cebbpyjd"

# FILES constants
DB_FILE = "files/all_stocks"
INSTRUMENT_TOKENS_FILE = "files/instrument_tokens"
LARGE_CAP_INSTRUMENT_TOKENS_FILE = "files/large_cap_instrument_tokens"
MID_CAP_INSTRUMENT_TOKENS_FILE = "files/mid_cap_instrument_tokens"

MID_CAP_FILE_NAME_CSV = "files/csv/mid_cap.csv"
LARGE_CAP_FILE_NAME_CSV = "files/csv/large_cap.csv"
MID_CAP_FILE = "files/mid_caps"
LARGE_CAP_FILE = "files/large_caps"

GAINERS_DICT_FILE = "../files/gainers"
LOSERS_DICT_FILE = "../files/losers"
PIKACHU_TARGET_FILE = "files/pikachu_target"

# Stock properties
LAST_PRICE = "last_price"
AVERAGE_PRICE = "average_price"
CHANGE = "change"
LAST_TRADE_TIME = "last_trade_time"
TRADING_SYMBOL = "tradingsymbol"
EXCHANGE = "exchange"
EXCHANGE_TOKEN = "exchange_token"
NAME = "name"
EXPIRY = "expiry"
STRIKE = "strike"
SEGMENT = "segment"
LOT_SIZE = "lot_size"
INSTRUMENT_TYPE = "instrument_type"
INSTRUMENT_TOKEN = "instrument_token"
TICK_SIZE = "tick_size"
SYMBOL = "symbol"
CHANGE_PERCENTAGE = "change_percentage"
NET_PRICE = "netPrice"
HIGH = "high"
LOW = "low"
QUANTITY = "quantity"

# Intervals
INTERVAL_MINUTE = "minute"
INTERVAL_DAY = "day"
INTERVAL_3_MINUTE = "3minute"
INTERVAL_5_MINUTE = "5minute"
INTERVAL_10_MINUTE = "10minute"
INTERVAL_15_MINUTE = "15minute"
INTERVAL_30_MINUTE = "30minute"
INTERVAL_60_MINUTE = "60minute"

# TAGS
PIKACHU_BUY_TAG = "Pikachu BUY"
PIKACHU_SELL_TAG = "Pikachu SELL"

# Run times
PIKACHU_LAUNCH_TIME = "09:44"

NIFTY_50_STOCKS = ['EICHERMOT', "ULTRACEMCO", "BAJFINANCE", "ADANIPORTS", "GRASIM", "BAJAJFINSV", "NESTLEIND",
                   "TATACONSUM", "BAJAJ-AUTO", "BRITANNIA", "SHREECEM", "CIPLA", "HDFCLIFE", "IOC", "TCS", "RELIANCE",
                   "UPL", "HINDUNILVR", "ITC", "TITAN", "DIVISLAB", "M&M", "TECHM", "SUNPHARMA", "HDFCBANK", "DRREDDY",
                   "TATASTEEL", "BPCL", "LT", "ASIANPAINT", "INFY", "HEROMOTOCO", "COALINDIA", "NTPC", "BHARTIARTL",
                   "ONGC", "SBIN", "MARUTI", "AXISBANK", "HCLTECH", "JSWSTEEL", "WIPRO", "HDFC", "INDUSINDBK",
                   "POWERGRID", "TATAMOTORS", "SBILIFE", "ICICIBANK", "HINDALCO", "KOTAKBANK"]

ORDER_STATUS_LIST = ["OPEN","OPEN PENDING","VALIDATION PENDING","PUT ORDER REQ RECEIVED","REJECTED",
                     "COMPLETE", "MODIFIED", "MODIFY PENDING", "MODIFY VALIDATION PENDING", "CANCELLED",
                     "CANCEL PENDING", " TRIGGER PENDING"]

INTERVAL_DAY_RATIO = {
    INTERVAL_MINUTE: 60,
    INTERVAL_3_MINUTE: 100,
    INTERVAL_5_MINUTE: 100,
    INTERVAL_10_MINUTE: 100,
    INTERVAL_15_MINUTE: 200,
    INTERVAL_30_MINUTE: 200,
    INTERVAL_60_MINUTE: 400,
    INTERVAL_DAY: 2000
}