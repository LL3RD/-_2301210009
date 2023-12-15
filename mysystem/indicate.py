import pandas as pd
import numpy as np
import talib as ta


class indicate(object):
    def __init__(self):
        pass

    @classmethod
    def SMA(cls,price,window=20):
        return price.rolling(window=window).mean()
    
    @classmethod
    def EMA(cls,price,window=20):
        return ta.EMA(price,timeperiod=window)

    @classmethod
    def RSI(cls,price):
        return ta.RSI(price, 20) /100

    @classmethod
    def KDJ(cls,price,window=20):
        high = price.rolling(window).max()
        low = price.rolling(window).min()

        k, d = ta.STOCH(high, low, price)
    
        k = k / 100
        d = d / 100
        j = 3 * k - 2*d
    
        return j
    
    @classmethod
    def MACD(cls,price,fastperiod=12, slowperiod=26, signalperiod=9):
        MACD, MACD_signal, MACD_hist =ta.MACD(price, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
        return MACD