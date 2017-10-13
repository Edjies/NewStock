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
    print('1' > '2')
    vol = 10
    sma = 10
    print(eval('vol < 50 and sma10 == 10'))
    eval('print(1 + 2)')
    # while True:
    #     try:
    #         with open('test.txt', mode='a', encoding='utf-8') as f:
    #             f.write(time.strftime( '%Y-%m-%d %X', time.gmtime(time.time())))
    #     except Exception as e:
    #         print(e)
    #         pass
    #     time.sleep(15)