# coding=utf-8
from __future__ import print_function, absolute_import
from gm.api import *


def init(context):
    # 订阅浦发银行, bar频率为一天
    subscribe(symbols='SHSE.600000', frequency='12s', count=10)


def on_bar(context, bars):
    # 打印当前获取的bar信息
    print(bars)


if __name__ == '__main__':
    run(strategy_id='1a59545f-bc82-11e8-8dc8-2047477914bf',
        filename='t2.py',
        mode=1,
        token='f2abaec3366e095875b3e847ee2b707cb2d33d5b',
        backtest_start_time='2016-06-17 13:00:00', backtest_end_time='2017-08-21 15:00:00')
