# -*-coding:utf-8 -*-
import StockIndicator
import StockIO
import numpy as np

def find_trend_up(stock_pool, kline_type):
    result = []
    stock_list = StockIO.get_stock(stock_pool)
    for stock in stock_list:
        k, d = StockIndicator.kd(StockIO.get_kline(stock.stock_code, kline_type))
        if k.shape[0] > 2:
            if k[-2] > d[-2] and k[-1] < k[-2] and d[-1] > d[-2] and k[-1] > d[-1] and k[-1] > 50 and k[-1] < 80:
                result.append(stock)
    return result


def sma_close(stock_list, kline_type, x_position = -1, timeperiod=5, reverse=False):
    result = []
    for stock in stock_list:
        kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
        close = kline[:, 2].astype(np.float)
        open = kline[:, 1].astype(np.float)
        sma = StockIndicator.sma(kline, timeperiod)[0]

        if close.shape[0] < abs(x_position):
            return result

        if close[x_position] > sma[x_position] and not reverse:
            result.append(stock)
        elif close[x_position] < sma[x_position] and reverse:
            result.append(stock)
    return result


def downdown(stock_list, kline_type, x_position = -1, count=4, timeperiod=5):
    result = []
    for stock in stock_list:
        kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
        open = kline[:, 1].astype(np.float)
        close = kline[:, 2].astype(np.float)
        sma = StockIndicator.sma(kline, timeperiod)[0]
        if close.shape[0] < abs(x_position) + count:
            return result

        hit = True
        for i in range(count):
            if  close[x_position - i] > sma[x_position - i]  or open[x_position - i] < close[x_position - i]:
                hit = False
                break
        if hit:
            result.append(stock)

    return result

def upup(stock_list, kline_type, x_position = -1, count=4, timeperiod=5, strict=True):
    result = []
    for stock in stock_list:
        kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
        open = kline[:, 1].astype(np.float)
        close = kline[:, 2].astype(np.float)
        sma = StockIndicator.sma(kline, timeperiod)[0]
        if close.shape[0] < abs(x_position) + count:
            return result

        hit = True
        for i in range(count):
            if  close[x_position - i] < sma[x_position - i]  or open[x_position - i] > close[x_position - i]:
                hit = False
                break
        if strict:
            position = x_position - count
            if close[position] > open[position] and close[position] > sma[position]:
                hit = False

        if hit:
            result.append(stock)

    return result



def find_kdj_jx(stock_pool, kline_type, n_rsv=9, x_position=-1, k_min=0, k_max=100, period=-1, times=1, about=False):
    """
    :param stock_pool: name
    :param kline_type:
    :param n_rsv:
    :param x_position: 发生位置 -1代表当日， -2代表前一天
    :param k_min:  limit min k in x_position
    :param k_max:  limit max k in x_position
    :param period: to count the times of jx between period
    :param times:
    :param about:
    :return:  stock_list
    """
    result = []
    stock_list = StockIO.get_stock(stock_pool)
    for stock in stock_list:
        k, d = StockIndicator.kd(StockIO.get_kline(stock.stock_code, kline_type), n_rsv)
        if is_jx(k, d, x_position, about):
            if between(k[x_position], k_min, k_max):
                if period < -1 and times > 1:
                    count = 1
                    for i in range(period, x_position):
                        count = count + 1 if is_jx(k, d, i) else count
                    if count >= times:
                        result.append(stock)
                else:
                    result.append(stock)
    return result


def find_kdj_sx(stock_pool, kline_type, n_rsv=9, x_position=-1, k_min=0, k_max=100):
    """
    kdj死叉
    :param stock_pool: name
    :param kline_type:
    :param n_rsv:
    :param x_position:
    :param k_min:  limit min k in x_position
    :param k_max:  limit max k in x_position
    :return:  stock_list
    """
    result = []
    stock_list = StockIO.get_stock(stock_pool)
    for stock in stock_list:
        k, d = StockIndicator.kd(StockIO.get_kline(stock.stock_code, kline_type), n_rsv)
        if is_sx(k, d, x_position) and between(k[x_position], k_min, k_max):
            result.append(stock)
    return result


def find_macd_jx(stock_pool, kline_type, x_position = -1):
    """
    :param stock_pool:
    :param kline_type:
    :param x_position:
    :return: stock_list
    """
    result = []
    stock_list = StockIO.get_stock(stock_pool)
    for stock in stock_list:
        macd, macdsignal, macdhist = StockIndicator.macd(StockIO.get_kline(stock.stock_code, kline_type))
        if is_jx(macd, macdsignal, x_position):
            result.append(stock)
    return result


def find_macd_sx(stock_pool, kline_type, x_position = -1):
    """
    macd死叉
    :param stock_pool:
    :param kline_type:
    :param x_position:  死叉发生点
    :return: stock_list
    """
    result = []
    stock_list = StockIO.get_stock(stock_pool)
    for stock in stock_list:
        macd, macdsignal, macdhist = StockIndicator.macd(StockIO.get_kline(stock.stock_code, kline_type))
        if is_sx(macd, macdsignal, x_position):
            result.append(stock)
    return result


def is_jx(fast, slow, x_position, about=False):
    if fast.shape[0] - 1 > abs(x_position):
        if slow[x_position - 1] > fast[x_position - 1] and (fast[x_position] < slow[x_position] if about else fast[x_position] > slow[x_position])\
                and fast[x_position] > fast[x_position - 1] and (slow[x_position] > slow[x_position - 1] or about):
            return True
    return False


def is_sx(fast, slow, x_position, about=False):
    if fast.shape[0] - 1 > abs(x_position):
        if slow[x_position - 1] < fast[x_position - 1] and (fast[x_position] > slow[x_position] if about else fast[x_position] < slow[x_position])\
                and fast[x_position] < fast[x_position - 1] and (slow[x_position] < slow[x_position - 1] or about):
            return True
    return False


def kdj_is_in(stock, kline_type, position = 0, k_min=0, k_max=30):
    kline = StockIO.get_kline(stock.stock_code, kline_type)
    k, d = StockIndicator.kd(StockIO.get_kline(stock.stock_code, kline_type), 9)
    if k.shape[0] > abs(position) + 1:
        if k_max > k[position] > k[position - 1] > k_min:
            return True
    return False


def intersection(l1, l2):
    """
    取两个列表的交集
    :param l1:
    :param l2:
    :return:
    """
    return [x for x in l1 if x in l2]


def between(x, min=0, max=20):
    return min <= x <= max







