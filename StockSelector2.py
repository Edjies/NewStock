# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import numpy as np


def select_w_5(stock_list):
    """
    随机游走模型
    :return:
    """
    min_item = 120
    x_position = -1
    period = 5

    result = []
    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_week)
        except:
            continue
        if kline.shape[0] <= min_item:
            continue

        open = kline[:, 1].astype(np.float)[:None if x_position == -1 else (x_position + 1)]
        close = kline[:, 2].astype(np.float)[:None if x_position == -1 else (x_position + 1)]
        high = kline[:, 3].astype(np.float)[:None if x_position == -1 else (x_position + 1)]
        low = kline[:, 4].astype(np.float)[:None if x_position == -1 else (x_position + 1)]
        vb = StockIndicator.vibration(kline)[:None if x_position == -1 else (x_position + 1)][-period:]
        cg =  (close - open)[-period:]
        count = 0
        for index, z in enumerate(vb):
            if z > 15:
                count = count + 1

        if count >= 3 and not stock.stock_code.startswith('300'):
            result.append(stock)
            print(vb)
            print(stock)

    return result

def select_d_5(stock_list):
    """
    随机游走模型
    :return:
    """
    min_item = 360
    x_position = -1
    period = 6

    result = []
    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_day)
        except:
            continue
        if kline.shape[0] <= min_item:
            continue

        open = kline[:, 1].astype(np.float)[:None if x_position == -1 else (x_position + 1)]
        close = kline[:, 2].astype(np.float)[:None if x_position == -1 else (x_position + 1)]
        high = kline[:, 3].astype(np.float)[:None if x_position == -1 else (x_position + 1)]
        low = kline[:, 4].astype(np.float)[:None if x_position == -1 else (x_position + 1)]
        vb = StockIndicator.vibration(kline)[:None if x_position == -1 else (x_position + 1)][-period:]
        cg =  (close - open)[-period:]
        count_8 = 0
        count_4 = 0
        for index, z in enumerate(vb):
            if z > 8:
                count_8 = count_8 + 1
            if z > 4:
                count_4 = count_4 + 1

        if count_8 <= 2 and count_4 > 4 and not stock.stock_code.startswith('300'):
            result.append(stock)
            print(vb)
            print(stock)

    return result

if __name__ == '__main__':
    # 均线处决胜负， 胜者向上，败者向下
    date = '2017-02-03'
    position = StockIndicator.position(date, '000001')
    # for x in range(-6, 0):
    #     print('x = ', x)
    #     print(select(StockIO.get_stock('sza'), x_position=x))
    print(select_d_5(StockIO.get_stock('sha')))
    #print(down_to(StockIO.get_stock('sha'), duration=60))