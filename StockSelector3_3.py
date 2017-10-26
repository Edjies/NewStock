# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
import StockShape
from StockFilterWrapper import filtrate_stop_trade, filtrate_high_price
import numpy as np
import StockAlgrithm

@filtrate_high_price
@filtrate_stop_trade
def select(stock_list, kline_type=StockConfig.kline_type_week, x_position=-3,
    shadow_min_vb = 3.5, shadow_ratio=0.4,
    min_chg=-100, max_chg=100, min_vb = 6, max_vb=20,
    min_item=120):
    """
    根据 振幅区间 和 涨幅区间排序
    :param stock_list:
    :param kline_type:
    :param avg:d
    :return:
    """
    result = []

    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
            open = kline[:, 1].astype(np.float)
            close = kline[:, 2].astype(np.float)
            high = kline[:, 3].astype(np.float)
            low = kline[:, 4].astype(np.float)
            sma5, sma10, sma20 = StockIndicator.sma(kline, 5, 10, 20)
            chg = StockIndicator.chg(kline)
            vb = StockIndicator.vibration(kline)
        except:
            continue
        if kline.shape[0] < min_item:
            continue

        if close[x_position] < sma5[x_position] < sma10[x_position] < sma20[x_position]:
            continue

        if max_chg > chg[x_position] > min_chg and max_vb > vb[x_position] > min_vb:
            result.append(stock)
            continue

        if StockShape.is_lower_shadow(open[x_position], close[x_position], high[x_position], low[x_position],
                                      min_vb=shadow_min_vb, ratio=shadow_ratio, red=False):
            result.append(stock)
            continue

        # if sma5[x_position] > sma10[x_position] > sma20[x_position] and vb[x_position] > shadow_min_vb:
        #     result.append(stock)
            continue

    return result

if __name__ == '__main__':
    result = {}
    for x in range(-5, 0):
        print('x = ', x)
        stock_list = select(StockIO.get_stock('sza'), x_position=x, kline_type=StockConfig.kline_type_day)
        print(stock_list)

        for stock in stock_list:
            result[stock] = result.get(stock, 0) + 1

    print(sorted(result.items(), key=lambda d: d[1], reverse=True))
    with open('C:/Users/panha/Desktop/xgfx/1002.txt', mode='w', encoding='utf-8') as f:
        for key in result:
            if result[key] >= 3:
                f.write("{}\n".format(key.stock_code))


