from abstracts.observer_abstract import Observer, Subject
import schedule


class Testing(Observer):
    """
    This strategy explained at https://www.youtube.com/watch?v=IQeeYv9eYlE
    1. At 9:40 start
    2. Check Top Losers and Top Gainers from NSE
    3. At 9:43, check highest absolute value of change from top losers and top gainers list (prefer stocks above 300)
    4. Add the selected stock to watchlist
    5. Open 15 minute chart of stock
    6. Check candle of 9:30 to 9:45, the second candle in 15 minute chart
    7. Set Entry at high of second candle (buffer price of 10 paisa)
    8. Set stop loss as lowest point of second candle
    9. Set target A as:  Entry + (Entry - stop loss)
    10. Once target A achieve, set stop loss as Target A
    11. For stock selection of loser side, use same strategy with selling and not buying
    """
    change_dict = dict()

    def __init__(self, stocks_data):
        self.stocks_data = stocks_data

    def update(self, subject: Subject):
        self.stocks_data = subject.testing_data
        self.create_change_dict()

    def create_change_dict(self):
        for key, val in self.stocks_data.items():
            self.change_dict[key] = val.change
        self.change_dict = {k: v for k, v in sorted(self.change_dict.items(), key=lambda item: item[1])}







