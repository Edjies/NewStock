# -*-coding:utf-8 -*-
import StockIndicator
import StockReporter
import StockFilter
import StockIO
import StockConfig
from StockFilter2 import find_kdj_jx, find_sma_up
import numpy as np

def select_1():
    """
    周线即将jx, 收于5日均线之上
    :return:
    """
    stock_list = StockFilter.find_kdj_jx('sha', kline_type=StockConfig.kline_type_week, x_position=-1, k_max=50)
    stock_list += StockFilter.find_kdj_jx('sza', kline_type=StockConfig.kline_type_week, x_position=-1, k_max=50)
    stock_list = StockFilter.sma_close(stock_list, kline_type=StockConfig.kline_type_week)
    stock_list = StockFilter.sma_close(stock_list, kline_type=StockConfig.kline_type_day)
    return stock_list


def select_2():
    stock_list = []
    #stock_list += StockFilter.find_kdj_jx('sha', kline_type=StockConfig.kline_type_day, x_position=-1, k_max=50)
    stock_list += StockFilter.find_kdj_jx('sha', kline_type=StockConfig.kline_type_day, x_position=-2, k_max=50)
    stock_list = StockFilter.sma_close(stock_list, kline_type=StockConfig.kline_type_week)
    return stock_list


def select_3():

    stock_list = []
    stock_list += StockFilter.find_kdj_jx('sha', kline_type=StockConfig.kline_type_week, x_position=-3, about=True)
    stock_list = StockFilter.sma_close(stock_list, kline_type=StockConfig.kline_type_week, x_position=-3)
    stock_list = StockFilter.sma_close(stock_list, kline_type=StockConfig.kline_type_week, x_position=-2, reverse=True)
    return stock_list

def select_4():
    """
    downdown
    :return:
    """
    stock_list = StockIO.get_stock('sha')
    stock_list = StockFilter.downdown(stock_list, kline_type=StockConfig.kline_type_week, count=5)
    return stock_list


def select_5():
    """
    upup
    :return:
    """
    stock_list = StockIO.get_stock('sha')
    stock_list = StockFilter.upup(stock_list, kline_type=StockConfig.kline_type_week, count=1, x_position=-1)
    return stock_list

def select_5_1():
    """
    upup
    :return:
    """
    x_position = -1
    kline_type = StockConfig.kline_type_week
    stock_list = StockIO.get_stock('sza')
    stock_list = StockFilter.upup(stock_list, kline_type=kline_type, count=1, x_position=x_position)
    result = []
    for stock in stock_list:
        k, d = StockIndicator.kd(StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_day), 9)
        if StockFilter.is_jx(k, d, x_position=-3, about=True):
            if StockFilter.between(k[x_position], 0, 100):
                result.append(stock)
    return result


def select_6():
    """
    jx后的微调
    :return:
    """
    stock_list = StockFilter.find_kdj_jx('sha', kline_type=StockConfig.kline_type_week, x_position=-3, about=False)
    stock_list = StockFilter.updown(stock_list, kline_type=StockConfig.kline_type_week, x_position=-2)
    return stock_list


def select_7():
    """
    还有about=False等
    :return:
    """
    x_position = -7
    stock_list = StockFilter.find_kdj_jx('sza', kline_type=StockConfig.kline_type_day, x_position=x_position, about=True)
    result = []
    hit = False
    for stock in stock_list:
        kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_day)
        close = kline[:, 2].astype(np.float)
        sma5 = StockIndicator.sma(kline, 5)[0]
        if sma5.shape[0] < 5 + abs(x_position):
            continue
        if sma5[x_position] < close[x_position]  \
            and sma5[x_position - 2] > close[x_position - 2] \
            and sma5[x_position - 3] > close[x_position - 3] \
                and sma5[x_position - 4] > close[x_position - 4] \
                and sma5[x_position - 5] > close[x_position - 5]:
            result.append(stock)
    return result

"""
todo: 观察不同position的后续变化， up down up  or up up
"""
stock_list = select_7()
StockIO.save_stock('s7_20170110', stock_list=stock_list, message='down to jx')
StockReporter.query_report(stock_list)


