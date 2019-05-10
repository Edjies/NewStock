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
# 活跃性处于上升状态， 即越来越活跃
# 只有活跃的股票才具有交易价值
# 活跃性降低的股票需要清仓
# 衰减论-活跃性，价格趋势，
# 波峰与波谷
# 排除垃圾票
@StockFilterWrapper.filtrate_stop_trade
def select(stock_list, x_position=-1, zf=4, kline_type=StockConfig.kline_type_week, min_item=80):
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
        high = kline[:, 3].astype(np.float)
        low = kline[:, 4].astype(np.float)
        p_close = np.roll(close, 1)
        sma5, sma10, sma20 = StockIndicator.sma(kline, 5, 10, 20)
        max_zf = StockIndicator.max_zf(kline)
        if max_zf[x_position] > zf and (low[x_position] < sma20[x_position]) and open[x_position] < close[x_position]:

            print(stock)
            result.append(stock)
    print(len(result))
    return result


def get_stock_list(x_position, zf=4, kline_type=StockConfig.kline_type_week):
    stock_list = select(StockIO.get_stock('gzw'), x_position=x_position, zf= zf, kline_type=kline_type)

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
    stock_list = get_stock_list(x_position=-1, zf=4, kline_type=StockConfig.kline_type_day)

    stock_code_list = []


    with open('data/track/today.txt', mode='w', encoding='utf-8') as f:
        for key in stock_list:
            if key.stock_code not in stock_code_list:
                f.write("{}\n".format(key.stock_code))





