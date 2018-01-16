# -*-coding:utf-8 -*-
import StockConfig
import json
from StockConfig import Stock
import numpy as np
import talib
import time
import datetime
import requests
# l1 = [Stock('1', 'a'), Stock('2', 'b'), Stock('3', 'c')]
# l2 = [Stock('1', 'a'), Stock('3', 'c')]
#
# print([x for x in l1 if x in l2])

# x = -1
# for i in range(4):
#     print(x - i)
#
#
#
#
# nparr2 = np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=float)
# print(talib.SMA(nparr2, timeperiod=5))
# print(nparr2[:-2][-2:])
#
# for index,i in enumerate(nparr2):
#     print(index, i)
#
# print(np.roll(nparr2, 1))


if __name__=='__main__':
    #url = 'http://192.168.1.115/backend/web/index-app.php'
    url = 'http://120.77.233.154/DST/backend/web/index-app.php'
    data = {'_loginkey': '8d6e0a3a9ac8fbf328439b5fdc5cf2b4',
            'curlng':'113.955454',
            'curlat':'22.547684',
            'keyword':'1号站',
            'act':'charge-station-new_search-with-keyword',
            'ver':'android2.0.4',
            #'r':'interfaces/charge-station-new/search-keyword'
            }

    r = requests.post(url,data)
    print(r.text)

