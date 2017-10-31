# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import StockShape
import StockAlgrithm
import numpy as np
from StockFilterWrapper import filtrate_stop_trade


@filtrate_stop_trade
def select(stock_list, kline_type=StockConfig.kline_type_week, x_position=-1, min_vb=6, ratio=0.4, min_item=120):
    """
    振幅/涨幅
    """
    result = []
    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
        except:
            continue
        if kline.shape[0] < min_item:
            continue

        open = kline[:, 1].astype(np.float)
        close = kline[:, 2].astype(np.float)
        high = kline[:, 3].astype(np.float)
        low = kline[:, 4].astype(np.float)
        chg = StockIndicator.chg(kline)
        vb = StockIndicator.vibration(kline)
        entity = StockIndicator.entity(kline)
        sma5, sma10, sma20 = StockIndicator.sma(kline, 5, 10, 20)
        if entity[x_position] / abs(chg[x_position]) > 1.5 and entity[x_position] > 3:
                print(stock)
                result.append(stock)
    return result

if __name__ == '__main__':
    date = '2017-02-03'
    print(select(StockIO.get_stock('sha'), x_position=-4, kline_type=StockConfig.kline_type_day))

    # result = {}
    # for x in range(-5, 0):
    #     print('x = ', x)
    #     stock_list = select(StockIO.get_stock('sha'), x_position=x, kline_type=StockConfig.kline_type_day, min_vb=5, ratio=0.4)
    #     print(stock_list)
    #     for stock in stock_list:
    #         result[stock] = result.get(stock, 0) + 1
    #
    # print(sorted(result.items(), key=lambda d: d[1], reverse=True))
    #print(down_to(StockIO.get_stock('sha'), duration=60))