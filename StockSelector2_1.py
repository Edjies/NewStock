# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import numpy as np
import StockFilterWrapper

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
        except:
            continue
        if kline.shape[0] < min_item:
            continue
        open = kline[:, 1].astype(np.float)
        close = kline[:, 2].astype(np.float)
        sma5, sma10, sma20 = StockIndicator.sma(kline, 5, 10, 20)

        if not close[x_position] < sma5[x_position]:
            continue

        print(stock)
        result.append(stock)

    return result


if __name__ == '__main__':
    stock_list = select(StockIO.get_stock('wsma10'), kline_type=StockConfig.kline_type_week, x_position=-2)
    print(stock_list)

    with open('C:/Users/panha/Desktop/xgfx/1004.txt', mode='w', encoding='utf-8') as f:
        for key in stock_list:
            f.write("{}\n".format(key.stock_code))



