# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import numpy as np
import StockFilterWrapper
import StockFilter2
import datetime
import time
# 采用跌幅法选股，要符合当前趋势
@StockFilterWrapper.filtrate_stop_trade
def select(stock_list, x_position=-1, df=-4, kline_type=StockConfig.kline_type_week, min_item=80):
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
        sma5, sma10, sma20 = StockIndicator.sma(kline, 5, 10, 20)
        max_df = StockIndicator.max_df(kline)
        if max_df[x_position] < df and (close[x_position] < sma10[x_position]):

            print(stock)
            result.append(stock)
    print(len(result))
    return result


def get_stock_list(x_position, df=-8, kline_type=StockConfig.kline_type_week):
    stock_list = select(StockIO.get_stock('sha'), x_position=x_position, df= df, kline_type=kline_type)
    stock_list += select(StockIO.get_stock('sza'), x_position=x_position, df= df, kline_type=kline_type)
    return stock_list



def toTDX():
    stock_code_list = []
    with open('{}/{}'.format(StockConfig.path_track, '2_sma_track.txt'), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if not line.startswith("#") and not '\n' == line:
                data = line.strip('\n').split(',')
                stock_code_list.append(data[0])
    with open('{}/{}.txt'.format(StockConfig.path_track, 'today_sma'), mode='w', encoding='utf-8') as f:
        for stock_code in stock_code_list:
            f.write("{}\n".format(stock_code))



if __name__ == '__main__':

    date = 'yyyy-mm-dd'
    stock_list = get_stock_list(x_position=-1, df=-6, kline_type=StockConfig.kline_type_week)

    stock_code_list = []


    with open('data/track/today.txt', mode='w', encoding='utf-8') as f:
        for key in stock_list:
            if key.stock_code not in stock_code_list:
                f.write("{}\n".format(key.stock_code))




