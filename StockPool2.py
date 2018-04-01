# -*- coding:utf-8 -*-
import requests
import json
import StockIO
import StockConfig
import StockIndicator
import numpy as np
from StockDownloader import write_stock_pool



def week_tendency():
    stock_result = []
    stock_list_1 = StockIO.get_stock('sha')
    stock_list_2 = StockIO.get_stock('sza')
    stock_list = stock_list_1 + stock_list_2
    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_week)
            close = kline[:, 2].astype(np.float)
            sma5, sma10, sma20, sma60 = StockIndicator.sma(kline, 5, 10, 20, 60)
        except Exception as e:
            print(e)
            continue
        if kline.shape[0] < 41:
            continue

        if sma5[-1] > sma20[-1]:
            stock_result.append(stock)

        elif sma20[-1] > sma20[-2]:
            stock_result.append(stock)
    return stock_result

def week_tendency2():
    """
    收盘价 位于 20日线 或者 60日线之上
    :return:
    """
    stock_result = []
    stock_list_1 = StockIO.get_stock('sha')
    stock_list_2 = StockIO.get_stock('sza')
    stock_list = stock_list_1 + stock_list_2
    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_week)
            close = kline[:, 2].astype(np.float)
            sma5, sma10, sma20, sma60 = StockIndicator.sma(kline, 5, 10, 20, 60)
        except Exception as e:
            print(e)
            continue
        if kline.shape[0] < 41:
            continue

        if close[-1] > sma20[-1] or close[-1] > sma60[-1]:
            stock_result.append(stock)

        elif sma5[-1] > sma10[-1]:
            stock_result.append(stock)
    return stock_result

if __name__ == '__main__':
    old_stock_list = StockIO.get_stock('week_tendency')
    stock_list = week_tendency2()

    # new_add_stock = [stock for stock in stock_list if stock not in old_stock_list]
    # new_reduce_stock = [stock for stock in old_stock_list if stock not in stock_list]
    # print('new_add_stock: ', new_add_stock)
    # print('new_reduce_stock: ', new_reduce_stock)
    #old_stock_list = StockIO.get_stock('')
    write_stock_pool('week_tendency', stock_list)

