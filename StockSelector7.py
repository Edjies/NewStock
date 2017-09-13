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
def select(stock_list, kline_type=StockConfig.kline_type_week, x_position=-1, min_item=120):
    """
    根据 换手率选择
    :param stock_list:
    :param kline_type:
    :param avg:d
    :return:
    """
    ltgb = StockIO.get_ltgb()
    print(ltgb)
    result = []
    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
            close = kline[:, 2].astype(np.float)
        except:
            continue
        if kline.shape[0] < min_item:
            continue

        sma30 = StockIndicator.sma(kline, 30)[0]


        if close[x_position] > sma30[x_position]:
                #print(stock)
                result.append(stock)
    return result


if __name__ == '__main__':
    # date = '2017-02-03'
    # position = StockIndicator.position(date, '000001')
    #日线
    result = {}
    for x in range(-3, -1):
        print('x = ', x)
        stock_list = select(StockIO.get_stock('sza'), x_position=x, kline_type=StockConfig.kline_type_week,)
        print(stock_list)

        for stock in stock_list:
            result[stock] = result.get(stock, 0) + 1


    print(sorted(result.items(), key=lambda d: d[1], reverse=True))
