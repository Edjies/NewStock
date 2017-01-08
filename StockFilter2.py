# -*-coding:utf-8 -*-
import StockIndicator
import StockIO
import numpy as np
import StockFilter
"""
通过修饰器提供过滤
"""


def find_kdj_jx(kline_type, x_position=-1, k_min=0, k_max=100, about=False):
    def f_decorator(func):
        def f_wrapper(stock_list):
            print('find_kdj_jx:', stock_list)
            stock_list = func(stock_list)
            result = []
            for stock in stock_list:
                k, d = StockIndicator.kd(StockIO.get_kline(stock.stock_code, kline_type), 9)
                if is_jx(k, d, x_position, about):
                    if between(k[x_position], k_min, k_max):
                            result.append(stock)
            return result
        return f_wrapper
    return f_decorator


def find_sma_up(kline_type, x_position=-1, timepeirod=5):
    def f_decorator(func):
        def f_wrapper(stock_list):
            stock_list = func(stock_list)
            print('find_sma_up:', stock_list)
            result = []
            for stock in stock_list:
                kline = StockIO.get_kline(stock.stock_code, kline_type)
                close = kline[:, 2].astype(np.float)
                sma, = StockIndicator.sma(kline, timepeirod)
                if sma.shape[0] > timepeirod + 3:
                    if close[x_position] > sma[x_position] > sma[x_position - 1] > sma[x_position - 2] > close[x_position - 2]:
                        result.append(stock)
            return result
        return f_wrapper
    return f_decorator


def f_kdj(kline_type, position=-1, k_min=0, k_max=20):
    def f_decorator(func):
        def f_wrapper(stock_list):
            stock_list = func(stock_list)
            return [stock for stock in stock_list if StockFilter.kdj_is_in(stock, kline_type, position=position, k_min=k_min, k_max=k_max)]
        return f_wrapper
    return f_decorator


def f_sma(kline_type, position=-1):
    def f_decorator(func):
        def f_wrapper(stock_list):
            return True
        return f_wrapper
    return f_decorator

def find_macd_jx(stock_pool, kline_type, x_position=-1):
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







