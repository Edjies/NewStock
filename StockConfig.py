# -*-coding:utf-8 -*-
import os
source_sina = 'sina'
source_tencent = 'tencent'

kline_type_day = 'day'
kline_type_week = 'week'
kline_type_month = 'month'

sina_node_sh_a = 'sh_a'
sina_node_sz_a = 'sz_a'

path_kline_day = 'data/kline/day'
path_kline_week = 'data/kline/week'
path_kline_month = 'data/kline/month'
path_stock = 'data/stock'
path_kline = 'data/kline'
path_track = 'data/track'


class Stock(object):
    __slots__ = ['stock_code', 'stock_name', 'stock_updown']

    def __init__(self, stock_code, stock_name):
        self.stock_code = stock_code
        self.stock_name = stock_name
        if self.stock_name.startswith('N'):
            self.stock_name = self.stock_name[1:]

    def __repr__(self):
        return repr((self.stock_code, self.stock_name))

    def __eq__(self, other):
        return self.stock_code == other.stock_code

    def __hash__(self):
        return self.stock_code.__hash__()


if not os.path.exists(path_track):
    os.makedirs(path_track)