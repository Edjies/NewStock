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
    stock_list = StockFilter.upup(stock_list, kline_type=StockConfig.kline_type_week, count=1, x_position=-4)
    return stock_list


<<<<<<< HEAD
stock_list = select_5()
StockIO.save_stock('s5_20170108', stock_list=stock_list, message='跟踪:持续上涨')
StockReporter.query_report(stock_list)
=======

def select_6():
    """
    jx后的微调
    :return:
    """
    stock_list = StockFilter.find_kdj_jx('sha', kline_type=StockConfig.kline_type_week, x_position=-3, about=False)
    stock_list = StockFilter.updown(stock_list, kline_type=StockConfig.kline_type_week, x_position=-2)
    return stock_list

"""
todo: 观察不同position的后续变化， up down up  or up up
"""
stock_list = select_6()
StockIO.save_stock('s6_20170108', stock_list=stock_list, message='跟踪:up down')
StockReporter.query_report(stock_list)

#StockReporter.query_report(select_1())
>>>>>>> d9b6377bee5556a2029ab920569b435973e358a8
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

