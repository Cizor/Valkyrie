import multiprocessing
from multiprocessing import Process, Manager

from Arceus.arceus import Arceus
from Pikachu.pikachu import Pikachu
from framework.kite_session import KiteSession
from framework.ticker import KTicker

from Dragonite.dragonite import Dragonite
from Dragonite.dragonair import Dragonair

from handle_data.handle_stock_data import HandleStockData
from side_update.update_gainers import UpdateGainers
from side_update.update_losers import UpdateLosers


def handle():
    KTicker()


def update_gainers():
    UpdateGainers()


def update_losers():
    UpdateLosers()

def pikachu():
    Pikachu()

def dragonite():
    Dragonite()


def arceus():
    Arceus()


if __name__ == '__main__':
    framework1 = Process(target=pikachu)
    # framework2 = Process(target=Dragonite)
    framework1.start()
    # framework2.start()
    framework1.join()
    # framework2.join()
    """
    framework3 = Process(target=arceus)
    framework3.start()
    framework3.join()
    """

    # framework4 = Process(target=Dragonair)

    # framework4.start()

    # framework4.join()
