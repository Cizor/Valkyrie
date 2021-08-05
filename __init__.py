from multiprocessing import Process

from framework.kite_session import KiteSession
from framework.kite_ticker import KTicker
from side_update.update_gainers import UpdateGainers
from side_update.update_losers import UpdateLosers


def init():
    KiteSession()
    # KTicker()


def update_gainers():
    UpdateGainers()


def update_losers():
    UpdateLosers()


if __name__ == '__main__':
    # framework = Process(target=init)
    # framework.start()
    # framework.join()

    update_gainers_process = Process(target=update_gainers)
    update_gainers_process.start()

    update_losers_process = Process(target=update_losers)
    update_losers_process.start()

    update_gainers_process.join()
    update_losers_process.join()

