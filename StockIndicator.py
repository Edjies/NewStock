# -*-coding:utf-8 -*-
try:
    import talib
except ImportError:
    pass
import numpy as np
import pandas as pd
import StockIO
import StockConfig

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
    return [_sma(close, timeperiod=i) for i in timeperiod]


def _sma(nparr, timeperiod):
    # r = [np.round((sum(nparr[index-timeperiod+1:index + 1])/timeperiod if timeperiod <= (index + 1) else 0), 2) for index, i in enumerate(nparr)]
    # return np.array(r)
    return pd.rolling_mean(nparr, timeperiod)


def asma(nparr, *timeperiod):
    """
    :param kline:
    :param timeperiod:
    :return:
    """
    return [_sma(nparr, timeperiod=i) for i in timeperiod]


def ema(kline, *timeperiod):
    """
    :param kline:
    :param timeperiod:
    :return:
    """
    close = kline[:, 2].astype(np.float)
    return [talib.EMA(close, timeperiod=i) for i in timeperiod]

def vibration(kline):
    """
    计算振幅， 第一个数不准确
    :param kline:
    :return:
    """
    open = kline[:, 1].astype(np.float)
    close = kline[:, 2].astype(np.float)
    high = kline[:, 3].astype(np.float)
    low = kline[:, 4].astype(np.float)
    diff = high - low
    p_close = np.roll(close, 1)
    return np.round(diff / p_close * 100, decimals=2)


def entity(kline):
    """
    计算k线实体幅度
    :return:
    """
    open = kline[:, 1].astype(np.float)
    close = kline[:, 2].astype(np.float)
    high = kline[:, 3].astype(np.float)
    low = kline[:, 4].astype(np.float)
    return np.round(abs((open - close) / np.where(open < close, open, close)) * 100, decimals=2)


def chg(kline):
    """
    计算涨跌幅
    :param kline:
    :return:
    """
    open = kline[:, 1].astype(np.float)
    close = kline[:, 2].astype(np.float)
    high = kline[:, 3].astype(np.float)
    low = kline[:, 4].astype(np.float)
    p_close = np.roll(close, 1)
    diff = close - p_close
    return np.round(diff / p_close * 100, decimals=2)


def cjl(kline):
    _cjl = kline[:, 5].astype(np.float)
    for i, v in enumerate(_cjl):
        if _cjl[i] < 10000000:
            _cjl[i] = _cjl[i] * 100
    return _cjl


def hsl(kline, ltgb):
    """
    计算换手率
    :param kline
    :param ltgb 流通股本
    :return:
    """
    if ltgb is None or ltgb <= 0:
        return None
    cjl = kline[:, 5].astype(np.float)
    for i,v in enumerate(cjl):
        if cjl[i] < 10000000:
            cjl[i] = cjl[i] * 100

    return np.round(cjl/(ltgb * 100), decimals=2)


def zf(kline):
    open = kline[:, 1].astype(np.float)
    close = kline[:, 2].astype(np.float)
    return np.round((close - open)/open * 100, decimals=2)



def chg_per(kline, from_position, to_position=-1):
    """
    左开右闭
    :param kline:
    :param from_position:
    :param to_position:
    :return:
    """
    to_position = None if to_position == -1 else to_position
    close_b = kline[:, 2].astype(np.float)[from_position + 1: to_position]
    close_p = kline[:, 2].astype(np.float)[from_position: to_position - 1 if to_position is not None else -1]
    return close_b - close_p, (close_b - close_p) / close_p * 100





def position(date, stock_code, kline_type=StockConfig.kline_type_day):
    kline = StockIO.get_kline(stock_code, kline_type)
    dates = kline[:, 0]
    length = dates.shape[0]
    if date in dates:
        index = np.argwhere(dates == date)[0][0] - length
        return index
    return None





if __name__ == '__main__':
    sma5, sma10 = sma(StockIO.get_kline('000001', kline_type=StockConfig.kline_type_day), 5, 10)
    print(type(sma5))
    print(sma5)
    print(sma10)
    #
    # chg, chg_per = chg_per(get_kline('002040', kline_type_day), from_position=-4, to_position=-1)
    # print(chg)
    # print(chg_per)
    #



