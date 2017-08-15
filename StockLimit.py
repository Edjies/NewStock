# -*- coding:utf-8 -*-
import requests
import json
import StockIO
import StockConfig
import numpy as np
from StockDownloader import write_stock_pool



def limit(stock_list, output_file='',high_limit_point=8, low_limit_point=5):
    result = []
    for stock in stock_list:
        try:
            kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_week)
        except Exception as e:
            print(e)
            continue

        close = kline[:, 2].astype(np.float)
        cur = close[-2]
        # 获取最低价和最高价
        up = cur * (1 + high_limit_point / 100)
        down = cur * (1 - low_limit_point / 100)
        result.append((stock.stock_code, down, up, stock.stock_name))

    path = '{root}/{name}'.format(root=StockConfig.path_track, name=output_file)
    with open(path, mode='w', encoding='utf-8') as f:
        for item in result:
            print(item[0], item[1], item[2], item[3])
            f.write("{}, {}, {}, {}, {}\n".format(item[0], '%05.2f' % item[1], '%05.2f' % item[2], item[3], '(* 振荡)'))


if __name__ == '__main__':
    limit(StockIO.get_stock('level_1'), 'level_1_week_track.txt')

