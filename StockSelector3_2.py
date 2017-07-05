# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import StockFilter
import numpy as np


def select(stock_list, last_date, kline_type=StockConfig.kline_type_week, x_position=-1, min_chg=-100, max_chg=100, min_vb = 0, max_vb=100, min_item=120):
    """
    根据某个交易段的 成交量 和 振幅 来挖掘
    :param stock_list:
    :param kline_type:
    :param x_position:
    :param min_chg:
    :param max_chg:
    :param min_vb:
    :param max_vb:
    :param min_item:
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

        chg = StockIndicator.chg(kline)
        vb = StockIndicator.vibration(kline)
        open = kline[:, 1].astype(np.float)
        close = kline[:, 2].astype(np.float)
        low = kline[:, 4].astype(np.float)
        sma5, sma10, sma20 = StockIndicator.sma(kline, 5, 10, 20)
        if max_chg > chg[x_position] > min_chg and max_vb > vb[x_position] > min_vb:
            # 未停牌
            if not StockFilter.is_stop_trade(stock, last_date):
                #五日线在十日线下方
                if sma5[x_position] < sma10[x_position]:
                    # 然后存在 最低价小于等于当前的开盘价
                    if np.min(low[x_position+1:] <= min(close[x_position], open[x_position])):
                        print(stock)
                        result.append(stock)
        return result

if __name__ == '__main__':
    date = '2017-02-03'
    position = StockIndicator.position(date, '000001')
    # for x in range(-6, 0):
    #     print('x = ', x)
    #     print(select(StockIO.get_stock('sza'), x_position=x))
    # 按照跌幅来选
    #print(select(StockIO.get_stock('sha'), '2017-07-03', x_position=-3, kline_type=StockConfig.kline_type_week, min_chg=-50, max_chg=0, min_vb=15, max_vb=100))
    # 按照涨幅来选
    print(select(StockIO.get_stock('sha'), '2017-07-03', x_position=-3, kline_type=StockConfig.kline_type_week,
                 min_chg=0, max_chg=30, min_vb=10, max_vb=30))
# =======
#     for x in range(-3, 0):
#         print('x = ', x)
#         print(select(StockIO.get_stock('sha'), x_position=x, kline_type=StockConfig.kline_type_week))

