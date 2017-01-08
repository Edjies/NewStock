# -*-coding:utf-8 -*-
import talib
import numpy as np
from StockIO import *

"""
StockIndicator used for confirm price movement
"""


def kd(kline, n_rsv=9):
    """
    :param kline:
    :param n_rsv:
    :param n_k:
    :param n_d:
    :return:k (nparray)
             d (nparray)

    """
    rsv = [0] * kline.shape[0]
    k = [0] * len(rsv)
    d = [0] * len(rsv)
    open = kline[:, 1].astype(np.float)
    close = kline[:, 2].astype(np.float)
    high = kline[:, 3].astype(np.float)
    low = kline[:, 4].astype(np.float)

    if len(rsv) < n_rsv:
        return np.array(k), np.array(d)

    for i in range(0, close.shape[0]):
        if i < n_rsv - 1:
            rsv[i] = 0
        else:
            start = i - n_rsv + 1
            end = i + 1
            rsv[i] = (close[i] - np.min(low[start:end])) / (np.max(high[start:end]) - np.min(low[start:end])) * 100

    for index, i in enumerate(rsv):
        if index != 0:
            k[index] = 1/3.0*rsv[index] + 2/3.0*k[index-1]    # 计算平滑移动平均线

    for index, i in enumerate(k):
        if index != 0:
            d[index] = 1/3.0*k[index] + 2/3.0*d[index-1]      # 计算平滑移动平均线

    return np.array(k), np.array(d)


def macd(kline, fastperiod=12, slowperiod=26, signalperiod=9):
    """
    :param kline:
    :return:macd   (nparray)
            macdsignal   (nparray)
            macdhist    (nparray)
    """
    close = kline[:, 2].astype(np.float)
    return talib.MACD(close, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)


def sma(kline, *timeperiod):
    """
    :param kline:
    :param timeperiod:
    :return:
    """
    close = kline[:, 2].astype(np.float)
    return [talib.SMA(close, timeperiod=i) for i in timeperiod]


def ema(kline, *timeperiod):
    """
    :param kline:
    :param timeperiod:
    :return:
    """
    close = kline[:, 2].astype(np.float)
    return [talib.EMA(close, timeperiod=i) for i in timeperiod]


if __name__ == '__main__':
    sma5, sma10 = sma(get_kline('601611', kline_type=kline_type_day), 5, 10)
    print(sma5)
    print(sma10)


