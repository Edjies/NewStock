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
        high = kline[:, 3].astype(np.float)
        sma5, sma10, sma20, sma60 = StockIndicator.sma(kline, 5, 10, 20, 60)
        if not (close[x_position] > sma5[x_position] > sma10[x_position] and sma5[x_position] > sma20[x_position]):
            continue
        if not close[x_position] > max(np.max(open[x_position - 20 : x_position]), np.max(close[x_position - 20 : x_position])):
            continue

        print(stock)
        result.append(stock)

    return result


if __name__ == '__main__':
    # 该选股方法 每天要过滤的形态：

    position = -1
    date = '2018-03-12'
    # 过滤重复的
    stock_code_list = []
    with open('{}/{}'.format(StockConfig.path_track, 'zixuan_w.txt'), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if not line.startswith("#") and not '\n' == line:
                data = line.strip('\n')
                stock_code_list.append(data)

    new_list = select(StockIO.get_stock('sza'), x_position=position, kline_type=StockConfig.kline_type_week)
    new_list += select(StockIO.get_stock('sha'), x_position=position, kline_type=StockConfig.kline_type_week)
    # 新结果
    result_list = [x.stock_code for x in new_list if x.stock_code not in stock_code_list]
    with open('{}/{}.txt'.format(StockConfig.path_track, 'zixuan_w'), mode='a', encoding='utf-8') as f:
        f.write('#{}\n'.format(date))
        for stock_code in result_list:
            f.write("{}\n".format(stock_code))

    with open('{}/{}.txt'.format(StockConfig.path_track, 'today_w'), mode='w', encoding='utf-8') as f:
        f.write('\n#{}\n'.format(date))
        for stock_code in result_list:
            f.write("{}\n".format(stock_code))



