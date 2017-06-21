# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import numpy as np

def filter_by_sma(stock_list, kline_type=StockConfig.kline_type_day, sma_period=20, x_position=-1, min_item=360):
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
            origin_kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
        except:
            continue
        if origin_kline.shape[0] < min_item:
            continue

        sma = StockIndicator.sma(origin_kline, sma_period)[0]
        open = origin_kline[:, 1].astype(np.float)
        close = origin_kline[:, 2].astype(np.float)
        high = origin_kline[:, 3].astype(np.float)
        low = origin_kline[:, 4].astype(np.float)
        if low[x_position] < sma[x_position] < high[x_position]:
            if low[x_position - 2] > sma[x_position - 2] and low[x_position - 3] > sma[x_position - 3]:
                # if open[x_position] > close[x_position]:
                #     if sma[x_position - 1] < sma[x_position ]:
                #         result.append(stock)
                if low[x_position + 1]:
                    result.append(stock)

    return result

def a(stock_list, kline_type=StockConfig.kline_type_day, x_position=-1, min_item=360):
    """
    一阳穿三线， 股票有启动迹象，观察后续均线走势
    :param stock_list:
    :param kline_type:
    :param x_position:
    :return:
    """
    result = []
    for stock in stock_list:
        try:
            origin_kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
        except:
            continue

        if origin_kline.shape[0] < min_item:
            continue


        open = origin_kline[:, 1].astype(np.float)
        close = origin_kline[:, 2].astype(np.float)
        high = origin_kline[:, 3].astype(np.float)
        low = origin_kline[:, 4].astype(np.float)
        sma5, sma10, sma20 = StockIndicator.sma(origin_kline, 5, 10, 20)
        if close[x_position] > open[x_position]:
            if open[x_position] < min(sma5[x_position], sma10[x_position], sma20[x_position]) and close[x_position] > max(sma5[x_position], sma10[x_position], sma20[[x_position]]):
                result.append(stock)
    return result

def down_to(stock_list, kline_type=StockConfig.kline_type_day, x_position=-1, duration=10, min_item=360):
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
            origin_kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
        except:
            continue
        if origin_kline.shape[0] < min_item:
            continue


        start = x_position - duration + 1
        end = None if x_position == -1 else (x_position + 1)
        open = origin_kline[:, 1].astype(np.float)[start:end]
        close = origin_kline[:, 2].astype(np.float)[start:end]
        high = origin_kline[:, 3].astype(np.float)[start:end]
        low = origin_kline[:, 4].astype(np.float)[start:end]

        max = np.max(high)
        min = close[x_position]

        if 30 < (max - min) / (max) * 100 < 40:
            print(stock, int((max - min) / (max) * 100))
            result.append(stock)

    return result



def trend_up(stock_list, kline_type=StockConfig.kline_type_day, sma_period=10, x_position=-1, duration=10, min_item=360):
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
            origin_kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
        except:
            continue
        if origin_kline.shape[0] < min_item:
            continue


        start = x_position - duration + 1
        end = None if x_position == -1 else (x_position + 1)
        open = origin_kline[:, 1].astype(np.float)[start:end]
        close = origin_kline[:, 2].astype(np.float)[start:end]
        high = origin_kline[:, 3].astype(np.float)[start:end]
        low = origin_kline[:, 4].astype(np.float)[start:end]
        sma = StockIndicator.sma(origin_kline, sma_period)[0][start:end]

        target = True
        for i in range(duration):
            if sma[i] > close[i]:
                target = False
        if target and low[i] <= sma[i]:
            result.append(stock)

    return result

def trend_up_2(stock_list, x_position=-1, min_item=360):
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
        if kline_day.shape[0] < min_item:
            continue

        open_day = kline_day[:, 1].astype(np.float)
        open_week = kline_week[:, 1].astype(np.float)
        close_day = kline_day[:, 2].astype(np.float)
        close_week = kline_week[:, 2].astype(np.float)

        sma5_d, sma10_d, sma20_d = StockIndicator.sma(kline_day, 5, 10, 20)
        sma5_w, sma10_w, sma20_w = StockIndicator.sma(kline_week, 5, 10, 20)

        # if sma5_d[x_position] > sma5_d[x_position - 1]:
        #     if sma10_d[x_position] > sma10_d[x_position - 1]:
        #         if sma20_d[x_position] > sma20_d[x_position - 1]:
        #             if sma20_d[x_position] > sma5_d[x_position]:
        #                 if close_day[x_position] > sma5_d[x_position]:
        #                     result.append(stock)
        #                     print(stock)

        # if sma5_w[x_position] > sma10_w[x_position] > sma20_w[x_position]:
        #     if close_week[x_position] > sma5_w[x_position]:
        #         result.append(stock)
        #         print(stock)

        # if sma20_w[x_position - 1] > sma5_w[x_position - 1] and sma20_w[x_position] < sma5_w[x_position]:
        #     if sma5_w[x_position] > sma20_w[x_position] > sma10_w[x_position]:
        #         #if close_week[x_position] > sma10_w[x_position] > sma20_w[x_position]:
        #         result.append(stock)
        #         print(stock)

        # # 后置判断
        # if sma10_w[x_position - 1] > sma5_w[x_position - 1] and sma10_w[x_position] < sma5_w[x_position]:
        #     if sma20_w[x_position] > sma5_w[x_position] > sma10_w[x_position]:
        #         if sma10_w[x_position + 1] < open_week[x_position + 1] < close_week[x_position + 1]:
        #             result.append(stock)
        #             print(stock)

        # # 5日线穿过10日线
        if sma10_d[x_position - 1] > sma5_d[x_position - 1] and sma10_d[x_position] < sma5_d[x_position]:
            if sma5_d[x_position] > sma5_d[x_position - 1]:
                    #if sma5_w[x_position - 2] < open_week[x_position - 2] < close_week[x_position - 2]:
                        result.append(stock)
                        print(stock)

        # # 连续三天10日线飘红上升
        # if sma10_w[x_position] < open_week[x_position] < close_week[x_position]:
        #     if sma10_w[x_position - 1] < open_week[x_position] < close_week[x_position - 1]:
        #         if sma10_w[x_position - 2] < open_week[x_position - 2] < close_week[x_position - 2]:
        #             #if sma10_w[x_position - 2] > sma5_w[x_position - 2] and sma10_w[x_position] < sma5_w[x_position]:
        #                 result.append(stock)
        #                 print(stock)

    return result

def xia_ying_xian(kline_item):
    open = float(kline_item[1])
    close = float(kline_item[2])
    high = float(kline_item[3])
    low = float(kline_item[4])

    top = min(close, open)
    bottom = low
    if (top - bottom) / (top) * 100 > 6:
        return True

if __name__ == '__main__':
    # 均线处决胜负， 胜者向上，败者向下
    date = '2017-02-03'
    position = StockIndicator.position(date, '000001')
    print(trend_up_2(StockIO.get_stock('sha'), x_position=-5))
    #print(down_to(StockIO.get_stock('sha'), duration=60))