# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import numpy as np
import StockFilterWrapper
import StockFilter2
import datetime
import time

@StockFilterWrapper.filtrate_stop_trade
def select(stock_list, x_position=-1, kline_type=StockConfig.kline_type_day, min_item=120):
    """
    均线选股法
    :param stock_list:
    :param kline_type:
    :param avg:
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

        open = kline[:, 1].astype(np.float)
        close = kline[:, 2].astype(np.float)
        low = kline[:, 4].astype(np.float)
        sma5, sma10, sma20, sma30, sma60= StockIndicator.sma(kline, 5, 10, 20, 30, 60)
        zf = StockIndicator.zf(kline)

        if close[x_position] > sma5[x_position] > sma10[x_position] > open[x_position] and sma10[x_position] > sma20[x_position]:
            if zf[x_position] > 5:
                print(stock)
                result.append(stock)
    return result



if __name__ == '__main__':
    position = -7
    date = '2018-03-20'
    stock_list = select(StockIO.get_stock('sha'), x_position=position, kline_type=StockConfig.kline_type_day) + \
                 select(StockIO.get_stock('sza'), x_position=position, kline_type=StockConfig.kline_type_day)
    print(stock_list)
    stock_code_list = []
    with open('data/track/2_sma_track.txt', mode='a', encoding='utf-8') as f:
        f.write('\n#{}\n'.format(date))
        for key in stock_list:
            if key.stock_code not in stock_code_list:
                f.write('{:>6},{: >5},{:>2},{:>2},{:>5},{:>5}, , ,\n'.format(key.stock_code, key.stock_name, '', '', '00.00', '00.00'))

    with open('data/track/s3_{}.txt'.format(date), mode='w', encoding='utf-8') as f:
        for key in stock_list:
            if key.stock_code not in stock_code_list:
                f.write("{}\n".format(key.stock_code))



