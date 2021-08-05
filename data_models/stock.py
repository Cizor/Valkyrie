from data_models.tick import Tick


class Stock:
    def __init__(self, ins_token):
        self._instrument_token = ins_token
        self._last_price = 0
        self._change = 0
        self._average_price = 0
        self._last_trade_time = 0

    @property
    def last_price(self):
        return self._last_price

    @last_price.setter
    def last_price(self, value):
        self._last_price = value

    @property
    def average_price(self):
        return self._average_price

    @average_price.setter
    def average_price(self, value):
        self._average_price = value

    @property
    def change(self):
        return self._change

    @change.setter
    def change(self, value):
        self._change = value

    @property
    def instrument_token(self):
        return self._instrument_token

    @instrument_token.setter
    def instrument_token(self, value):
        self._instrument_token = value

    @property
    def last_trade_time(self):
        return self._last_trade_time

    @last_trade_time.setter
    def last_trade_time(self, value):
        self._last_trade_time = value

    def handle_tick(self, tick):
        """
        Check if instrument token is correct and then assign change value only if
        value has been changed
        :param tick:
        :return:
        """
        if isinstance(tick, Tick) and tick.instrument_token == self.instrument_token:
            if self.last_price != tick.last_price:
                self.last_price = tick.last_price
            if self.average_price != tick.average_price:
                self.average_price = tick.average_price
            if self.change != tick.change:
                self.change = tick.change
            self.last_trade_time = tick.last_trade_time
        else:
            raise TypeError("Tick type data not sent or instrument token is wrong")

    def __lt__(self, other):
        return self.last_price < other.last_price

    def __gt__(self, other):
        return self.last_price > other.last_price


