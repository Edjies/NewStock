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
def select(stock_list, x_position=-1, min_item=120):
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
            kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_week)
            kline_day = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_day)
        except Exception as e:
            print(e)
            continue
        if kline.shape[0] < min_item:
            continue

        open = kline[:, 1].astype(np.float)
        close = kline[:, 2].astype(np.float)
        low = kline[:, 4].astype(np.float)
        sma5, sma10, sma20, sma60= StockIndicator.sma(kline, 5, 10, 20, 60)
        sma5_day, sma10_day, sma20_day = StockIndicator.sma(kline_day, 5, 10, 20)
        if stock.stock_code == '300146':
            print(stock.stock_code)

        if sma5[x_position] > sma20[x_position] or sma5[x_position] > sma60[x_position]:
                #or (sma5[x_position] > sma10[x_position] and close[x_position] > sma20[x_position]):
            #if sma5_day[x_position] > sma10_day[x_position]:
                print(stock)
                result.append(stock)
    return result



if __name__ == '__main__':
    position = -1
    date = '2018-07-17'
    stock_list = select(StockIO.get_stock('sha'), x_position=position) + \
                 select(StockIO.get_stock('sza'), x_position=position)
    #stock_list = select(StockIO.get_stock('sha'), x_position=position)

    print(stock_list)

    origin_stock_code_list = []
    # with open('data/track/today.txt', mode='r', encoding='utf-8') as f:
    #     lines = f.readlines()
    #     for line in lines:
    #         if not line.startswith("#") and not '\n' == line:
    #             data = line.strip('\n').split(',')
    #             origin_stock_code_list.append(data[0])




    with open('data/track/today.txt', mode='w', encoding='utf-8') as f:

        f.write('###' + date + '\n')
        for key in stock_list:
            code = key.stock_code
            if code not in origin_stock_code_list:
                f.write("{}\n".format(key.stock_code))



