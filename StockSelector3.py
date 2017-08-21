# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
from StockFilterWrapper import filtrate_stop_trade, filtrate_high_price
import numpy as np
import StockAlgrithm

@filtrate_high_price
@filtrate_stop_trade
def select(stock_list, kline_type=StockConfig.kline_type_week, x_position=-1, min_chg=-100, max_chg=100, min_vb = 10, max_vb=100, min_item=120):
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

        chg = StockIndicator.chg(kline)
        vb = StockIndicator.vibration(kline)
        if max_chg > chg[x_position] > min_chg and max_vb > vb[x_position] > min_vb:
            # 过滤掉单边上涨
            if not StockAlgrithm.sumOfSubArray(chg[-10:])[0] > 10:
                print(stock)
                result.append(stock)
    return result

if __name__ == '__main__':
    # date = '2017-02-03'
    # position = StockIndicator.position(date, '000001')
    result = {}
    for x in range(-5, 0):
        print('x = ', x)
        stock_list = select(StockIO.get_stock('level_1'), x_position=x, kline_type=StockConfig.kline_type_day,
                 min_chg=-100, max_chg=100, min_vb=4, max_vb=100)
        print(stock_list)

        for stock in stock_list:
            result[stock.stock_code] = result.get(stock.stock_code, 0) + 1


    print(sorted(result.items(), key=lambda d: d[1], reverse=True))

