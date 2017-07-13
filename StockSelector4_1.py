# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import StockShape
import numpy as np
from StockFilterWrapper import filtrate_stop_trade


@filtrate_stop_trade
def select(stock_list, kline_type=StockConfig.kline_type_week, x_position=-1, min_vb=6, ratio=0.4, min_item=120):
    """
    下影线选股法
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
        sma5, sma10, sma20 = StockIndicator.sma(kline, 5, 10, 20)

        if StockShape.is_shadow(open[x_position], close[x_position], high[x_position], low[x_position], min_vb=min_vb, ratio=ratio, red=False):
                print(stock)
                result.append(stock)
    return result

if __name__ == '__main__':
    date = '2017-02-03'
    position = StockIndicator.position(date, '000001')
    result = {}
    for x in range(-5, 0):
        print('x = ', x)
        stock_list = select(StockIO.get_stock('level_1'), x_position=x, kline_type=StockConfig.kline_type_day, min_vb=3.5, ratio=0.2)
        print(stock_list)
        for stock in stock_list:
            result[stock] = result.get(stock, 0) + 1

    print(sorted(result.items(), key=lambda d: d[1], reverse=True))

    #print(down_to(StockIO.get_stock('sha'), duration=60))