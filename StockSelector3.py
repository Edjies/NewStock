# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
from StockFilterWrapper import filtrate_stop_trade, filtrate_high_price
import numpy as np
import StockAlgrithm

@filtrate_high_price
@filtrate_stop_trade
def select(stock_list, kline_type=StockConfig.kline_type_week, x_position=-1, min_item=120):
    """
    根据 振幅区间 和 涨幅区间排序
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
            open = kline[:, 1].astype(np.float)
        except:
            continue
        if kline.shape[0] < min_item:
            continue

        chg = StockIndicator.chg(kline)
        vb = StockIndicator.vibration(kline)
        sma5, sma10, sma20 = StockIndicator.sma(kline, 5, 10, 20)
        if open[x_position] < sma5[x_position] < close[x_position]:
                print(stock)
                result.append(stock)
    return result

if __name__ == '__main__':
    # date = '2017-02-03'
    # position = StockIndicator.position(date, '000001')
    #日线

    stock_list = select(StockIO.get_stock('sha'), x_position=-2, kline_type=StockConfig.kline_type_day)
    print(stock_list)

    # # 周线
    # result = {}
    # for x in range(-5, 0):
    #     print('x = ', x)
    #     stock_list = select(StockIO.get_stock('sza'), x_position=x, kline_type=StockConfig.kline_type_day,
    #                         min_chg=-100, max_chg=100, min_vb=10, max_vb=100)
    #     print(stock_list)
    #
    #     for stock in stock_list:
    #         result[stock] = result.get(stock, 0) + 1
    #
    # print(sorted(result.items(), key=lambda d: d[1], reverse=True))

