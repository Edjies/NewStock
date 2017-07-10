# -*- coding:utf-8 -*-
import requests
import json
import StockIO
import StockConfig
import numpy as np
from StockDownloader import write_stock_pool



def fei_lei():
    stock_level_1 = []
    stock_level_2 = []
    stock_level_3 = []
    stock_list_1 = StockIO.get_stock('sha')
    stock_list_2 = StockIO.get_stock('sza')
    stock_list = stock_list_1 + stock_list_2
    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_month)
        except Exception as e:
            print(e)
            continue
        if kline.shape[0] < 41:
            continue

        close = kline[:, 2].astype(np.float)[-40:]
        cur = close[-1]
        # 获取最低价和最高价
        min = np.min(close)
        max = np.max(close)
        # 将将价差分成3等分
        divide = (max - min) / 3
        limit1 = min + divide
        limit2 = min + 2 * divide
        if cur < limit1:
            stock_level_1.append(stock)
        elif cur < limit2:
            stock_level_2.append(stock)
        else:
            stock_level_3.append(stock)

    StockIO.save_stock('level_1', stock_level_1, root=StockConfig.path_stock, message='低价股')
    StockIO.save_stock('level_2', stock_level_2, root=StockConfig.path_stock, message='中价股')
    StockIO.save_stock('level_3', stock_level_3, root=StockConfig.path_stock, message='高价股')


if __name__ == '__main__':
    fei_lei()

