# -*-coding:utf-8 -*-
import StockIndicator
import StockReporter
import StockFilter
import StockIO
import StockConfig
from StockFilter2 import find_kdj_jx, find_sma_up
import numpy as np


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

# first step : filter stock and select target stock
@find_sma_up(StockConfig.kline_type_day, x_position=-1)
@find_kdj_jx(StockConfig.kline_type_week, x_position=-1, k_max=60)
def filter_stock(stock_list):
    """
    strategy:
    :param stock_list: buy in Tuesday, Monday for confirm up trend, Friday must quits if profited.
    :return:
    """
    return stock_list

stock_list = filter_stock(StockIO.get_stock('sha'))
print(stock_list)
StockReporter.query_report(stock_list)

# second step: track stock and select buy point


# third step: track stock and select sell point
