# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import numpy as np
import StockFilterWrapper
import StockFilter2

@StockFilterWrapper.filtrate_stop_trade
def select(x_position=-1):
    origin_stock = get_stock(x_position - 1)
    new_stock = get_stock(x_position)
    diff_stock = [x for x in new_stock if x in origin_stock]
    result = []

    for stock in diff_stock:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_day)
        except Exception as e:
            print(e)
            continue

        if kline.shape[0] < 10:
            continue

        close = kline[:, 2].astype(np.float)
        cjl = StockIndicator.cjl(kline)

        if close[x_position] > np.max(close[x_position - 5: x_position]):
            if cjl[x_position] > np.max(cjl[x_position - 5: x_position]):
                print(stock)
                result.append(stock)

    return result


def get_stock(x_position):
    stock_result = []
    stock_list = StockIO.get_stock('sha')
    stock_list += StockIO.get_stock('sza')

    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_day)
        except Exception as e:
            print(e)
            continue
        if kline.shape[0] < 41:
            continue

        close = kline[:, 2].astype(np.float)
        sma5, sma10, sma20, sma30 = StockIndicator.sma(kline, 5, 10, 20, 30)

        if close[x_position] > sma5[x_position] > sma10[x_position] > sma20[x_position] > sma30[x_position]:
            stock_result.append(stock)
    return stock_result


if __name__ == '__main__':
    select(-2)



