import logging
from kiteconnect import KiteConnect

logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key="05q4h560cebbpyjd")

print(kite.login_url())


req_token = "oX4Ygkd7hKhIyxtsjpvf1BUsrWclrPaQ"

data = kite.generate_session(req_token, api_secret="p1hg1e5gb69r2ut18wvh6uwrjhkuwo55")


acc_token = data['access_token']

print(acc_token)
#kite.set_access_token(acc_token)


#print(kite.instruments(exchange=KiteConnect.EXCHANGE_NSE))


