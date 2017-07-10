# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import StockFilter
import numpy as np
from StockFilterWrapper import filtrate_high_price, filtrate_stop_trade


@filtrate_stop_trade
def select(stock_list, kline_type=StockConfig.kline_type_week, x_position=-1, period=4, count_limit=3, min_vb=0, max_vb=100, min_item=120):
    """
    通过统计一段时间内振幅较大出现的次数， 然后对支撑价与压力价进行监测
    :param stock_list:
    :param kline_type:
    :param x_position:
    :param min_vb:
    :param max_vb:
    :param min_item:
    :return:
    """
    result = []
    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
            close = kline[:, 2].astype(np.float)
        except Exception as e:
            print(e)
            continue
        if kline.shape[0] < min_item:
            continue

        vb = StockIndicator.vibration(kline)
        count = 0
        for vb_value in vb[x_position - period:x_position]:
            if StockFilter.between(vb_value, min_vb, max_vb):
                count += 1
        if count > count_limit:
            print(stock)
            result.append(stock)
    return result

if __name__ == '__main__':
    date = '2017-02-03'
    position = StockIndicator.position(date, '000001')
    for x in range(-4, 0):
        print('x = ', x)
        # print(select(StockIO.get_stock('sza'), x_position=x))
        # 按照跌幅来选
        #print(select(StockIO.get_stock('sha'), '2017-07-03', x_position=-3, kline_type=StockConfig.kline_type_week, min_chg=-50, max_chg=0, min_vb=15, max_vb=100))
        # 按照涨幅来选
        print(select(StockIO.get_stock('sza'),x_position=-1, kline_type=StockConfig.kline_type_week, period=5, count_limit=3, min_vb=10, max_vb=100))
# =======
#     for x in range(-3, 0):
#         print('x = ', x)
#         print(select(StockIO.get_stock('sha'), x_position=x, kline_type=StockConfig.kline_type_week))

