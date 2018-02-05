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
def select(stock_list, x_position=-1, kline_type=StockConfig.kline_type_week, min_item=120):
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

        close = kline[:, 2].astype(np.float)
        sma5, sma10, sma20, sma30, sma60= StockIndicator.sma(kline, 5, 10, 20, 30, 60)
        cjl = StockIndicator.cjl(kline)
        if close[x_position] > sma5[x_position] > sma10[x_position]:
                if close[x_position] > np.max(close[x_position - 8: x_position]):
                    if cjl[x_position] > np.max(cjl[x_position - 8: x_position]):
                        count = 0
                        add = False
                        while count < 4:
                            if StockFilter2.is_jx(sma5, sma10, x_position - count):

                                add = True
                                break
                            count += 1

                        if add:
                            max_exceed = 5
                            while close[x_position] > np.max(close[x_position - max_exceed : x_position]):
                                max_exceed+=1
                                if max_exceed > 200:
                                    break

                            stock.max_exceed=max_exceed
                        if add:
                            print(stock)
                            result.append(stock)

    return result


def get_stock_list(x_position):
    stock_list = []

    stock_list1 = select(StockIO.get_stock('sza'), x_position=x_position, kline_type=StockConfig.kline_type_week)
    stock_list2 = select(StockIO.get_stock('sha'), x_position=x_position, kline_type=StockConfig.kline_type_week)
    for x in stock_list1:
        if x not in stock_list:
            stock_list.append(x)
    for x in stock_list2:
        if x not in stock_list:
            stock_list.append(x)

    return stock_list

def toTDX(date):
    stock_code_list = []
    with open('{}/{}'.format(StockConfig.path_track, '{}.txt'), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if not line.startswith("#") and not '\n' == line:
                data = line.strip('\n').split(',')
                stock_code_list.append(data[0])
    with open('{}/{}.txt'.format(StockConfig.path_track, date), mode='w', encoding='utf-8') as f:
        for stock_code in stock_code_list:
            f.write("{}\n".format(stock_code))



if __name__ == '__main__':
    position = -3
    date = '20180104'
    stock_list_1 = get_stock_list(position)
    stock_list_2 = get_stock_list(position - 1)
    stock_list_3 = get_stock_list(position - 2)
    stock_list_4 = get_stock_list(position - 3)

    stock_list = [x for x in stock_list_1 if x not in (stock_list_2 + stock_list_3 + stock_list_4)]

    print(sorted(stock_list, key=lambda stock: stock.max_exceed, reverse=True))
    print(len(stock_list))



    stock_code_list = []

    with open('data/track/2_sma_track_w.txt', mode='a', encoding='utf-8') as f:
        f.write('\n#{}\n'.format(date))
        for key in stock_list:
            if key.stock_code not in stock_code_list:
                f.write("{},{}, , , , , , ,\n".format(key.stock_code, key.stock_name))

    with open('data/track/w_{}.txt'.format(date), mode='w', encoding='utf-8') as f:
        for key in stock_list:
            if key.stock_code not in stock_code_list:
                f.write("{}\n".format(key.stock_code))




