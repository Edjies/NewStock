# -*-coding:utf-8 -*-
import StockIndicator
import StockConfig
import StockIO
import numpy as np
import StockConfig


def is_stop_trade(stock, last_date):
    """
    是否停牌
    :param stock:
    :param last_date:
    :return:
    """
    kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_day)
    date = kline[:, 0]
    if date[-1] == last_date:
        return False
    return True


def intersection(l1, l2):
    """
    取两个列表的交集
    :param l1:
    :param l2:
    :return:
    """
    return [x for x in l1 if x in l2]


def between(x, min=0, max=20):
    return min <= x <= max







