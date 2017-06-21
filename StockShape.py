# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import numpy as np

def bottom(stock_list, kline_type = StockConfig.kline_type_day, x_position=-1,  period=20, round=2):
    """
    当股价到达均线附近时， 要么调整， 要么突破
    :param stock_list:
    :param kline_type:
    :param avg:
    :return:
    """
    result = []
    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
        except:
            continue
        if kline.shape[0] <= period:
            continue

        open = kline[:, 1].astype(np.float)[:None if x_position == -1 else (x_position + 1)]
        close = kline[:, 2].astype(np.float)[:None if x_position == -1 else (x_position + 1)]
        high = kline[:, 3].astype(np.float)[:None if x_position == -1 else (x_position + 1)]
        low = kline[:, 4].astype(np.float)[:None if x_position == -1 else (x_position + 1)]

        if np.min(close) >= np.min(low[-round:]):
            result.append(stock)
    return result

if __name__ == '__main__':
    # 均线处决胜负， 胜者向上，败者向下
    date = '2017-02-03'
    position = StockIndicator.position(date, '000001')
    for x in range(-6, 0):
        print('x = ', x)
        print(bottom(StockIO.get_stock('sza'), x_position=-3))
    #print(select(StockIO.get_stock('sza'), x_position=-10))
    #print(down_to(StockIO.get_stock('sha'), duration=60))