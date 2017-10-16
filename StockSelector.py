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

        if sma5[x_position] > sma10[x_position] > sma20[x_position]:
            if open[x_position] < close[x_position]:
                print(stock)
                result.append(stock)



    return result


if __name__ == '__main__':

    result = {}
    for x in range(-3, 0):
        print('x = ', x)
        stock_list = select(StockIO.get_stock('sha'), kline_type=StockConfig.kline_type_week, x_position=x)
        print(stock_list)

        for stock in stock_list:
            result[stock] = result.get(stock, 0) + 1
    print(sorted(result.items(), key=lambda d: d[1], reverse=True))

    with open('stock_list.txt', mode='w', encoding='utf-8') as f:
        for stock in result:
            if result.get(stock, 0) > 1:
                f.write(stock.stock_code)
                f.write('\n')

    # result = {}
    # for x in range(-5, 0):
    #     print('x = ', x)
    #     stock_list = select(StockIO.get_stock('sha'), kline_type=StockConfig.kline_type_week, x_position=x)
    #     print(stock_list)
    #
    #     for stock in stock_list:
    #         result[stock] = result.get(stock, 0) + 1
    #
    # result2 = {}
    # for x in range(-3, 0):
    #     print('x = ', x)
    #     stock_list = select(StockIO.get_stock('sha'), kline_type=StockConfig.kline_type_week, x_position=x)
    #     print(stock_list)
    #
    #     for stock in stock_list:
    #         result2[stock] = result2.get(stock, 0) + 1
    #
    # result3 = {}
    # for x in result:
    #     if result.get(x, 0) != result2.get(x, 0):
    #         result3[x] = result.get(x, 0)
    #
    # print(sorted(result3.items(), key=lambda d: d[1], reverse=True))