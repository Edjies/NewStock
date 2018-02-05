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
    url = 'http://120.25.209.72/index-app.php'
    data = {
        #'_loginkey': '4a4815ef961500a7b47902abd09937f7',
            'act':'charge_get-charge-record',
            'ver':'android2.1.3',
            'mobile':'13545230029',
            'rows':'10',
            'page':'1'

            #'r':'interfaces/charge-station-new/search-keyword'
            }

    r = requests.post(url,data)
    print(r.text)

