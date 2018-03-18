# -*-coding:utf-8 -*-
import StockIO
import StockConfig
import StockFilter
import StockIndicator
import numpy as np
from StockDownloader import save_stock

# 每日分析

# 1. 分析每日仍然保持了趋势的个股（两点： 一是新高底部， 二是最近新高靠近日线， 三是均线金叉）
stock_list = StockIO.get_stock('week_tendency')


def avg_up_trend(stock):
    kline = StockIO.get_kline(stock.stock_code, StockConfig.kline_type_day)
    sma5, sma10, sma20, sma60 = StockIndicator.sma(kline, 5, 10, 20, 60)
    if sma5[-1] > sma10[-1] > sma20[-1] and sma5[-1] > sma60[-1]:
        return True
    return False


StockIO.save_stock('today_trend.txt', [stock for stock in stock_list if avg_up_trend(stock)])






