# -*- coding:utf-8 -*-
import requests
import json
import StockIndicator
import StockIO
import StockConfig
import numpy as np
import StockFilter2
from StockDownloader import write_stock_pool



def fei_lei():
    stock_result = []
    stock_list = StockIO.get_stock('sha')
    stock_list += StockIO.get_stock('sza')

    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_day)
        except Exception as e:
            print(e)
            continue
        if kline.shape[0] < 41:
            continue

        close = kline[:, 2].astype(np.float)
        sma5, sma10, sma20, sma30 = StockIndicator.sma(kline, 5, 10, 20, 30)

        if close[-1] > sma5[-1] > sma10[-1] > sma20[-1] > sma30[-1]:
            print(stock)
            stock_result.append(stock)

    StockIO.save_stock('day_up', stock_result, root=StockConfig.path_stock, message='日线向上股')


if __name__ == '__main__':
    fei_lei()

