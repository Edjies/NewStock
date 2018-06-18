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
def select(stock_list, x_position=-1, w_x_position= -1, kline_type=StockConfig.kline_type_week, min_item=480):
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
        sma5, sma10, sma20, sma30, sma60= StockIndicator.sma(kline, 5, 10, 20, 30, 60)
        cjl = StockIndicator.cjl(kline)
        vb = StockIndicator.vibration(kline)
        add = False

        #破势
        if close[x_position] > sma10[x_position] > sma5[x_position] > open[x_position] and sma20[x_position] > sma5[x_position]:
            if 5<vb[x_position] < 15:
                min_low_5 = min(np.min(low[x_position - 2: x_position]), low[x_position])
                if (close[x_position] - min_low_5) / min_low_5 * 100 < vb[x_position] * 1.2:

                    add = True
                    stock.vb=vb[x_position]
        if add:
            print(stock)
            result.append(stock)

    return result


def get_stock_list(x_position):
    stock_list = select(StockIO.get_stock('sha'), x_position=x_position, kline_type=StockConfig.kline_type_day)
    stock_list += select(StockIO.get_stock('sza'), x_position=x_position, kline_type=StockConfig.kline_type_day)
    stock_list = sorted(stock_list, key=lambda stock: stock.vb, reverse=True)
    return stock_list[:40]




if __name__ == '__main__':
    position = -1
    date = '2018-04-02'
    stock_list = get_stock_list(position)
    print(stock_list)

    stock_code_list = []

    with open('data/track/2_dow_track.txt', mode='a', encoding='utf-8') as f:
        f.write('\n#{}\n'.format(date))
        for key in stock_list:
            if key.stock_code not in stock_code_list:
                f.write('{:>6},{: >5},{:>2},{:>2},{:>5},{:>5}, , ,\n'.format(key.stock_code, key.stock_name, '', '',
                                                                             '00.00', '00.00'))

    with open('data/track/today.txt', mode='a', encoding='utf-8') as f:
        for key in stock_list:
            if key.stock_code not in stock_code_list:
                f.write("{}\n".format(key.stock_code))

    with open('data/track/today_dow.txt', mode='w', encoding='utf-8') as f:
        for key in stock_list:
            if key.stock_code not in stock_code_list:
                stock_code = key.stock_code
                f.write("{}\n".format(('1' if stock_code.startswith('6') else '0') + stock_code))




