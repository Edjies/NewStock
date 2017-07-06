# -*-coding:utf-8 -*-
import StockIndicator
import StockConfig
import StockIO
import numpy as np
import StockConfig
from functools import wraps


def filtrate_high_price(func):
    """
    过滤掉高位票
    """
    #@wraps
    def wrapper(*args, **kwargs):
        stock_list = func(*args, **kwargs)
        result = []
        for stock in stock_list:
            if not is_high_price(stock):
                result.append(stock)
        return result

    return wrapper


def filtrate_stop_trade(func):
    """
    过滤掉停牌的票
    """
    #@wraps
    def wrapper(*args, **kwargs):
        stock_list = func(*args, **kwargs)
        result = []
        for stock in stock_list:
            if not is_stop_trade(stock):
                result.append(stock)
        return result
    return wrapper


def is_stop_trade(stock):
    """
    是否停牌, 以工商银行为例， 若日线最后一条数据的日期不相同时，则被认为停牌
    :param stock:
    :param last_date:
    :return:
    """
    kline_ref = StockIO.get_kline('601398', kline_type=StockConfig.kline_type_day)
    kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_day)
    date_ref = kline_ref[:, 0]
    date = kline[:, 0]
    if date[-1] == date_ref[-1]:
        return False
    return True


def is_high_price(stock):
    """
    高位票， 当周线 sma5 > sma10 > sma20 时，被认为是高位票
    :param stock:
    :return:
    """
    kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_week)
    sma5, sma10, sma20 = StockIndicator.sma(kline, 5, 10, 20)
    if sma5[-1] > sma10[-1] > sma20[-1]:
        return True
    return False





