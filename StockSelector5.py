# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
from StockFilterWrapper import filtrate_stop_trade, filtrate_high_price
import numpy as np
import StockAlgrithm

@filtrate_stop_trade
def select(stock_list, kline_type=StockConfig.kline_type_week, x_position=-1, period=10, min_down = -5, max_down = -15, min_item=100):
    """
    根据跌幅来选择
    :param stock_list:
    :param kline_type:
    :param avg:d
    :return:
    """
    result = []
    from_position = x_position - period + 1
    to_position = None if x_position == -1 else (x_position + 1)
    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
            chg = StockIndicator.chg(kline)[from_position:to_position]
        except:
            continue
        if kline.shape[0] < min_item:
            continue

        up, down = StockAlgrithm.sumOfSubArray(chg)
        if max_down <down < min_down:
            result.append(stock)

    return result

if __name__ == '__main__':
    # date = '2017-02-03'
    # position = StockIndicator.position(date, '000001')
    #日线
    stock_list = select(StockIO.get_stock('level_2'), x_position=-1, period=10, max_down=-20, min_down=-15,
                        kline_type=StockConfig.kline_type_day)
    print(stock_list)
    # result = {}
    # for x in range(-10, 0):
    #     print('x = ', x)
    #     stock_list = select(StockIO.get_stock('level_2'), x_position=x, period=3, max_down=-20, min_down= -5, kline_type=StockConfig.kline_type_day)
    #     print(stock_list)
        # for stock in stock_list:
        #     result[stock] = result.get(stock, 0) + 1


    #print(sorted(result.items(), key=lambda d: d[1], reverse=True))

