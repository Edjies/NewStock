# -*- coding:utf-8 -*-
import requests
import json
import StockIndicator
import StockIO
import StockConfig
import numpy as np
import StockFilter2
from StockDownloader import write_stock_pool

def day_tendency(x_position=-1):
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
            kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_day)
            open = kline[:, 1].astype(np.float)
            close = kline[:, 2].astype(np.float)
            sma5, sma10, sma20, sma60 = StockIndicator.sma(kline, 5, 10, 20, 60)
        except Exception as e:
            print(e)
            continue
        if kline.shape[0] < 360:
            continue

        if sma5[x_position] >  sma20[x_position] and sma5[x_position] > sma60[x_position] and sma10[x_position] > sma20[x_position] and sma10[x_position] > sma60[x_position]:
            if close[x_position] < sma5[x_position] and open[x_position] > sma5[x_position]:
                stock_result.append(stock)
    return stock_result


if __name__ == '__main__':
    x_position = StockIndicator.position('2018-03-20', stock_code='601398')
    stock_list = day_tendency(x_position=x_position)
    print(len(stock_list))
    write_stock_pool('day_tendency', stock_list)

