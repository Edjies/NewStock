# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import StockAlgrithm
from StockFilterWrapper import filtrate_stop_trade, filtrate_high_price
import numpy as np

@filtrate_high_price
@filtrate_stop_trade
def select(stock_list, kline_type=StockConfig.kline_type_day, x_position=-1, min_item=120):
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

        open = kline[:, -1].astype(np.float)
        close = kline[:, -2].astype(np.float)
        high = kline[:, -3].astype(np.float)
        low = kline[:, -4].astype(np.float)
        sma5, sma10, sma20 = StockIndicator.sma(kline, 5, 10, 20)
        vb = StockIndicator.vibration(kline)
        count = 9
        stock.count = 0
        while count >= 0:
            strength = 0
            if high[x_position - count] > sma5[x_position - count] > low[x_position - count]:
                strength += 1
            if high[x_position - count] > sma10[x_position - count] > low[x_position - count]:
                strength += 1
            if high[x_position - count] > sma20[x_position - count] > low[x_position - count]:
                strength += 1
            if strength >= 4 and vb[x_position - count] > 4:
                stock.count += 1
            count -= 1
        if stock.count > 3:
            result.append(stock)
            print(stock)
    return result

def get_stock_list(x_position):
    stock_list = select(StockIO.get_stock('sha'), x_position=x_position, kline_type=StockConfig.kline_type_day)
    stock_list += select(StockIO.get_stock('sza'), x_position=x_position, kline_type=StockConfig.kline_type_day)
    return stock_list

if __name__ == '__main__':
    date = '2017-02-03'
    position = StockIndicator.position(date, '000001')

    stock_list = get_stock_list(-6)
    stock_list = sorted(stock_list, key=lambda stock: stock.count, reverse=True)
    print(stock_list)

