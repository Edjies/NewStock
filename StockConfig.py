# -*-coding:utf-8 -*-
import os
source_sina = 'sina'
source_tencent = 'tencent'
source_gzw = 'gzw'

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
    __slots__ = ['stock_code', 'stock_name', 'stock_updown', 'max_exceed','vb', 'count']

    def __init__(self, stock_code, stock_name):
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.count = 0
        if self.stock_name.startswith('N'):
            self.stock_name = self.stock_name[1:]

    def __repr__(self):
        return repr((self.stock_code, self.stock_name))

    def __eq__(self, other):
        return self.stock_code == other.stock_code

    def __hash__(self):
        return self.stock_code.__hash__()


class KlineItem(object):
    __slots__ = ['openp', 'close', 'high', 'low','vb', 'upper_shadow', 'lower_shadow', 'entity']

    def __init__(self, openp, close, high, low):
        self.openp = openp
        self.close = close
        self.high = high
        self.low = low
        self.entity = round((close - openp) / low * 100, 2)
        self.upper_shadow = round((high - max(openp, close)) / low * 100, 2)
        self.lower_shadow = round((min(openp, close) - low) / low * 100, 2)
        self.vb = round((high - low) / low * 100, 2)

    def type(self):
        # 小阴星, 小阳星
        if abs(self.entity) < 1:
            pass
        #小阳线, 小阴线
        if abs(self.upper_shadow + self.lower_shadow) < 1:
            pass

        #上影线
        if self.lower_shadow > 3 and self.upper_shadow < 1:
           pass

        #下影线
        if self.upper_shadow > 3 and self.lower_shadow < 1:
           pass

        # 大阳线, 大阴线  (光头, 光脚, 穿头破脚)
        if abs(self.entity / self.lower_shadow) > 2 and abs(self.entity / self.upper_shadow) > 2 and self.entity > 3:
            pass



        pass


if not os.path.exists(path_track):
    os.makedirs(path_track)


if __name__=='__main__':
    kline = KlineItem(29.30, 32.41, 32.70, 28.92)
    print(kline.vb, kline.entity, kline.upper_shadow, kline.lower_shadow)