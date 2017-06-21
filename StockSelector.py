# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import numpy as np

def select(stock_list, x_position=-1, min_item=120):
    """
    当股价到达均线附近时， 要么调整， 要么突破
    :param stock_list:
    :param kline_type:
    :param avg:
    :return:
    """
    result = []
    for stock in stock_list:
        try:
            kline_day = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_day)
            kline_week = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_week)
        except:
            continue
        if kline_week.shape[0] < min_item:
            continue

        open_day = kline_day[:, 1].astype(np.float)
        open_week = kline_week[:, 1].astype(np.float)
        close_day = kline_day[:, 2].astype(np.float)
        close_week = kline_week[:, 2].astype(np.float)

        sma5_d, sma10_d, sma20_d = StockIndicator.sma(kline_day, 5, 10, 20)
        sma5_w, sma10_w, sma20_w = StockIndicator.sma(kline_week, 5, 10, 20)

        # 三线向下， 5 < 10 < 20 and  closeX > openX (x = x_position)
        if sma5_w[x_position] < sma10_w[x_position] < sma20_w[x_position]:
            if sma5_w[x_position - 1] < sma10_w[x_position - 1] < sma20_w[x_position - 1]:
                #if sma10_w[x_position] > close_week[x_position] > sma5_w[x_position] > open_week[x_position]:
                if close_week[x_position] > sma5_w[x_position] and close_week[x_position] > open_week[x_position]:
                    if close_week[x_position - 1] > sma5_w[x_position - 1] and close_week[x_position - 1] > open_week[x_position - 1]:
                        if np.min(close_week[-min_item: x_position]) == np.min(close_week[x_position - 5: x_position]):
                            print(stock)
                            result.append(stock)
                    if x_position == -1 and np.min(close_week[-min_item:] == np.min(close_week[-5:])):
                        print(stock)
                        result.append(stock)



    return result

if __name__ == '__main__':
    # 均线处决胜负， 胜者向上，败者向下
    date = '2017-02-03'
    position = StockIndicator.position(date, '000001')
    for x in range(-6, 0):
        print('x = ', x)
        print(select(StockIO.get_stock('sza'), x_position=x))
    #print(select(StockIO.get_stock('sza'), x_position=-10))
    #print(down_to(StockIO.get_stock('sha'), duration=60))