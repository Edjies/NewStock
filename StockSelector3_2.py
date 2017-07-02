# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import numpy as np


def select(stock_list, kline_type=StockConfig.kline_type_week, x_position=-1, min_chg=-30, max_chg=5, min_vb = 15, max_vb=100, min_item=120):
    """

    :param stock_list:
    :param kline_type:
    :param avg:d
    :return:
    """
    result = []
    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
            close = kline[:, 2].astype(np.float)
        except:
            continue
        if kline.shape[0] < min_item:
            continue

        chg = StockIndicator.chg(kline)
        vb = StockIndicator.vibration(kline)
        if max_chg > chg[x_position] > min_chg and max_vb > vb[x_position] > min_vb:
            print(stock)
            result.append(stock)
    return result

if __name__ == '__main__':
    date = '2017-02-03'
    position = StockIndicator.position(date, '000001')
    # for x in range(-6, 0):
    #     print('x = ', x)
    #     print(select(StockIO.get_stock('sza'), x_position=x))
    print(select(StockIO.get_stock('sha'), x_position=-5, kline_type=StockConfig.kline_type_week))