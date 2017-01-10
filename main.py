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
    stock_list = StockIO.get_stock('sha')
    stock_list = StockFilter.downdown(stock_list, kline_type=StockConfig.kline_type_week, count=5)
    return stock_list


def select_5():
    stock_list = StockIO.get_stock('sha')
    stock_list = StockFilter.upup(stock_list, kline_type=StockConfig.kline_type_week, count=1, x_position=-1)
    return stock_list


stock_list = select_5()
StockIO.save_stock('s5_20170108', stock_list=stock_list, message='跟踪:持续上涨')
StockReporter.query_report(stock_list)
# stock_list = StockFilter.find_kdj_jx('sha', kline_type=StockConfig.kline_type_day, x_position=-1, about=True)
# stock_result = []
# for stock in stock_list:
#     kline = StockIO.get_kline(stock.stock_code, StockConfig.kline_type_week)
#     close = kline[:, 2].astype(np.float)
#     sma5 = StockIndicator.sma(kline, 5)
#     if close[-1] > sma5[0][-1]:
#         stock_result.append(stock)
#
# print(stock_result)
# StockReporter.query_report(stock_result)

