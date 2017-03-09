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
        origin_kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
        if origin_kline.shape[0] < min_item:
            continue

        sma = StockIndicator.sma(origin_kline, sma_period)[0]
        open = origin_kline[:, 1].astype(np.float)
        close = origin_kline[:, 2].astype(np.float)
        high = origin_kline[:, 3].astype(np.float)
        low = origin_kline[:, 4].astype(np.float)
        if low[x_position] < sma[x_position] < high[x_position]:
            if open[x_position] > close[x_position]:
                if sma[x_position - 1] < sma[x_position ]:
                    result.append(stock)

    return result


if __name__ == '__main__':
    print(filter_by_sma(StockIO.get_stock('sha'), kline_type=StockConfig.kline_type_week, sma_period=20, x_position=-4, min_item=80))