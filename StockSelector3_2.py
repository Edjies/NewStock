# -*- coding:utf-8 -*-

import StockIO
import StockConfig
import StockIndicator
from StockFilterWrapper import filtrate_stop_trade, filtrate_high_price
import numpy as np
import StockAlgrithm
def select(stock_list, kline_type=StockConfig.kline_type_week, period = 10, x_position=-1, min_vb = 5, min_item=120):
    """
    取一段时间内的最高(收盘价 or 开盘价) 和最低 (开盘价 or 收盘价) 计算 最高价 和 最低价穿过这两条线的次数
    根据 振幅区间 和 涨幅区间排序
    :param stock_list:
    :param kline_type:
    :param avg:d
    :return:
    """
    result = {}
    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)

        except:
            continue
        if kline.shape[0] < min_item:
            continue

        from_position = x_position - period + 1
        to_position = None if x_position == -1 else (x_position + 1)


        open = kline[:, 1].astype(np.float)[from_position:to_position]
        close = kline[:, 2].astype(np.float)[from_position:to_position]
        high = kline[:, 3].astype(np.float)[from_position:to_position]
        low = kline[:, 4].astype(np.float)[from_position:to_position]

        chg = StockIndicator.chg(kline)
        vb = StockIndicator.vibration(kline)

        support_line = min(np.min(open), np.min(close))
        pressure_line = max(np.max(open), np.max(close))

        if stock.stock_code == '000760':
            print(support_line, pressure_line)

        if (pressure_line - support_line)/support_line * 100 < min_vb:
            continue

        up = 0
        down = 0
        for i in range(-period, 0):
            if low[i] < pressure_line < high[i]:
                up = 1
            if low[i] < support_line < high[i]:
                down=1

            if up ==1 and down == 1:
                result[stock] = result.get(stock, 0) + 1
                up = 0
                down = 0
    return result

if __name__ == '__main__':
    # 周线
    for x in range(3, 5):
        result = select(StockIO.get_stock('level_1'), period=x, x_position=-2, min_vb= 8, kline_type=StockConfig.kline_type_week)
        print("周线 period = ", str(x), ":", sorted(result.items(), key=lambda d: d[1], reverse=True))
    # 日线
    result = select(StockIO.get_stock('level_1'), period=10, x_position=-2, min_vb= 4, kline_type=StockConfig.kline_type_day)
    print("日线:", sorted(result.items(), key=lambda d: d[1], reverse=True))

