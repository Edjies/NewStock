# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import StockAlgrithm
from StockFilterWrapper import filtrate_stop_trade, filtrate_high_price
import numpy as np

@filtrate_high_price
@filtrate_stop_trade
def select(stock_list, kline_type=StockConfig.kline_type_week, x_position=-1, period=5, max_sum_chg=12, min_sum_chg = -12, min_sum_vb=40, min_item=120):
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
        except:
            continue
        if kline.shape[0] < min_item:
            continue

        from_position = x_position - period + 1
        to_position = None if x_position == -1 else (x_position + 1)
        close = kline[:, -2].astype(np.float)[from_position:to_position]
        chg = StockIndicator.chg(kline)[from_position:to_position]
        vb = StockIndicator.vibration(kline)[from_position:to_position]
        sma20 = StockIndicator.sma(kline, 20)[0][from_position:to_position]
        real_max_sum_chg, real_min_sum_chg = StockAlgrithm.sumOfSubArray(chg)
        real_min_sum_vb = np.sum(vb)
        if real_max_sum_chg < max_sum_chg and real_min_sum_chg > min_sum_chg and real_min_sum_vb > min_sum_vb:
            if close[-1] < sma20[-1]:
                print(stock)
                print(vb)
                result.append(stock)
    return result

if __name__ == '__main__':
    date = '2017-02-03'
    position = StockIndicator.position(date, '000001')

    result = {}
    for x in range(-10, 0):
        print('x = ', x)
        stock_list = select(StockIO.get_stock('level_1'), kline_type=StockConfig.kline_type_day, x_position=x, period=5, max_sum_chg= 10, min_sum_chg= -12, min_sum_vb= 30)
        print(stock_list)

        for stock in stock_list:
            result[stock.stock_code] = result.get(stock.stock_code, 0) + 1


    print(sorted(result.items(), key=lambda d: d[1], reverse=True))

