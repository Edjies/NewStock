# -*-coding:utf-8 -*-
import StockIO
import StockConfig
import StockFilter
import StockIndicator
import numpy as np


def stat_chg(stock_list, from_date, to_date, kline_type=StockConfig.kline_type_day):
    reports = []
    if len(stock_list) == 0:
        return reports

    for stock in stock_list:
        frome_position = StockIndicator.position(from_date, stock.stock_code, kline_type)
        to_position = StockIndicator.position(to_date, stock.stock_code, kline_type)
        if frome_position is not None and to_position is not None:
            kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_day)
            pre_close = float(kline[frome_position][2])
            close = float(kline[to_position][2])
            reports.append((stock.stock_code, stock.stock_name, close, close - pre_close, (close - pre_close)/pre_close * 100))

    reports.sort(key=lambda x: x[4])

    print("%-10s %-10s %8s %8s %8s" % ('code', 'name', 'price', 'chg', 'chg_per'))
    for report in reports:
        print("%-10s %-10s %8.2f %8.2f %8.2f" % (report[0], report[1], report[2], report[3], report[4]))
    return reports

