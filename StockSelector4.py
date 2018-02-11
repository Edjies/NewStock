# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import StockShape
import numpy as np
import StockFilter2
import StockAlgrithm
from StockFilterWrapper import filtrate_stop_trade


@filtrate_stop_trade
def select(stock_list, kline_type=StockConfig.kline_type_week, x_position=-1, min_vb=6, ratio=0.4, min_item=120, append_file='recent2.txt'):
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
        vb = StockIndicator.vibration(kline)
        chg = StockIndicator.chg(kline)
        cjl = StockIndicator.cjl(kline)
        sma5, sma10, sma20 = StockIndicator.sma(kline, 5, 10, 20)

        if StockShape.is_lower_shadow(open[x_position], close[x_position], high[x_position], low[x_position], min_vb=min_vb, ratio=ratio, red=True):
            if cjl[x_position] > cjl[x_position - 1]:
                print(stock)
                result.append(stock)
                # print(stock)
                # result.append(stock)
                # append to file
                # path = '{root}/{name}'.format(root=StockConfig.path_track, name=append_file)
                # with open(path, mode='a', encoding='utf-8') as f:
                #     value = low[-1] + (high[-1] - low[-1]) * 0.3
                #     f.write("{},{},{}\n".format(stock.stock_code, value, high[-1]))

    return result


if __name__ == '__main__':
    stock_list = []
    for x in range(-1, 0):
        stock_list += select(StockIO.get_stock('sza'), x_position=x, kline_type=StockConfig.kline_type_day, min_vb=5, ratio=0.5)
        #stock_list += select(StockIO.get_stock('sza'), x_position=x, kline_type=StockConfig.kline_type_day, min_vb=5,ratio=0.6)
    print(stock_list)

    with open('C:/Users/panha/Desktop/xgfx/1002.txt', mode='a', encoding='utf-8') as f:
        for stock in stock_list:
            f.write("{}\n".format(stock.stock_code))