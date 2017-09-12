# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
from StockFilterWrapper import filtrate_stop_trade, filtrate_high_price
import numpy as np
import StockAlgrithm
import talib

@filtrate_high_price
@filtrate_stop_trade
def select(stock_list, kline_type=StockConfig.kline_type_week, x_position=-1, min_hsl = 5, max_hsl=100, period=5, min_item=120):
    """
    根据 换手率选择
    :param stock_list:
    :param kline_type:
    :param avg:d
    :return:
    """
    ltgb = StockIO.get_ltgb()
    result = []
    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
            close = kline[:, 2].astype(np.float)
        except:
            continue
        if kline.shape[0] < min_item:
            continue

        hsl = StockIndicator.hsl(kline, ltgb.get(stock.stock_code, 0))
        if hsl is None:
            continue


            #print(stock.stock_code)
        if min_hsl < hsl[x_position] < max_hsl:
            #print(stock)
            # 放量价升
            if hsl[x_position] > np.max(hsl[x_position - period + 1: x_position]) and close[x_position] > np.max(close[x_position - period + 1 : x_position]):
                #print(stock)
                result.append(stock)
    return result



if __name__ == '__main__':
    # date = '2017-02-03'
    # position = StockIndicator.position(date, '000001')
    #日线
    result = {}

    for x in range(2, 10):
        print('x = ', x)
        stock_list = select(stock_list = StockIO.get_stock('sza'), x_position=-1, kline_type=StockConfig.kline_type_day,
                 min_hsl=4, period=x, max_hsl=10)
        print(stock_list)

        for stock in stock_list:
            result[stock] = result.get(stock, 0) + 1


    print(sorted(result.items(), key=lambda d: d[1], reverse=False))
