# -*- coding:utf-8 -*-
import requests
import json
import StockIndicator
import StockIO
import StockConfig
import numpy as np
from StockDownloader import write_stock_pool



def fei_lei():
    stock_level_1_up = []
    stock_list = StockIO.get_stock('level_1')


    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_week)
        except Exception as e:
            print(e)
            continue
        if kline.shape[0] < 41:
            continue

        close = kline[:, 2].astype(np.float)[-40:]
        sma5, sma10, sma20 = StockIndicator.sma(kline, 5, 10, 20)

        if close[-1] > sma5[-1] > sma10[-1] > sma20[-1]:
            stock_level_1_up.append(stock)

    StockIO.save_stock('level_1_up', stock_level_1_up, root=StockConfig.path_stock, message='低价股')


if __name__ == '__main__':
    fei_lei()

