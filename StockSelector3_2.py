# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import StockFilter
from StockFilterWrapper import filtrate_stop_trade, filtrate_high_price
import numpy as np


@filtrate_stop_trade
def select(stock_list, kline_type=StockConfig.kline_type_week, x_position=-1, min_chg=-100, max_chg=100, min_vb = 0, max_vb=100, min_item=120):
    """
    根据某个交易段的 成交量 和 振幅 来挖掘
    :param stock_list:
    :param kline_type:
    :param x_position:
    :param min_chg:
    :param max_chg:
    :param min_vb:
    :param max_vb:
    :param min_item:
    :return:
    """
    result = []
    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
        except Exception as e:
            print(e)
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
    for x in range(-6, 0):
        print('x = ', x)
    #     print(select(StockIO.get_stock('sza'), x_position=x))
    # 按照跌幅来选
    #print(select(StockIO.get_stock('sha'), '2017-07-03', x_position=-3, kline_type=StockConfig.kline_type_week, min_chg=-50, max_chg=0, min_vb=15, max_vb=100))
    # 按照涨幅来选
        print(select(StockIO.get_stock('level_2'), x_position=-2, kline_type=StockConfig.kline_type_week,
                 min_chg=-100, max_chg=0, min_vb=10, max_vb=100))
# =======
#     for x in range(-3, 0):
#         print('x = ', x)
#         print(select(StockIO.get_stock('sha'), x_position=x, kline_type=StockConfig.kline_type_week))

