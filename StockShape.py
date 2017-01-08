# -*-coding:utf-8 -*-
import StockIndicator
import StockIO
import StockFilter


def bottom_shape(stock, kline_type, **args):
    """
    :param stock:
    :param kline_type:
    :param
    :return:
    """
    k_min = args.get('k_min', 0)
    k_max = args.get('k_max', 0)

    kline = StockIO.get_kline(stock.stock_code, kline_type)
    k, d = StockIndicator.kd(kline)
    sma5 = StockIndicator.sma(kline, 5)[0]
    # 形态确认
    #if(StockFilter.is_jx(k, d, True) or StockFilter.is_jx(k, d, False) or )
    # 强度确认
    return 9,20,

def top_shape():
    pass
