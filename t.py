# -*-coding:utf-8 -*-
import StockConfig
import json
from StockConfig import Stock
import numpy as np
import talib
import time

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

    nparr = np.array([[1, 2, 3, 4, -1],[4, 3, 2, 1, -1], [5, 6, 7, 8, 1]], dtype=np.int)
    nparr = nparr + [1, 2, 3, 4, 5]
    for i in nparr:
        i
