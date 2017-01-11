# -*-coding:utf-8 -*-
import requests
import json
import StockIndicator
import StockConfig
import StockIO


def query_close(stock_list, date):
    reports = []
    if len(stock_list) == 0:
        return reports

    for stock in stock_list:
        position = StockIndicator.position(date, stock.stock_code, kline_type=StockConfig.kline_type_day)
        if position is not None:
            kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_day)
            kline_item = kline[position]
            pre_close = float(kline[position - 1][2] if kline.shape[0] > abs(position) else kline_item[1])
            close = float(kline_item[2])
            reports.append((stock.stock_code, stock.stock_name, close, close - pre_close, (close - pre_close)/pre_close * 100))

    reports.sort(key=lambda x: x[4])

    print("%-10s %-10s %8s %8s %8s" % ('code', 'name', 'price', 'chg', 'chg_per'))
    for report in reports:
        print("%-10s %-10s %8.2f %8.2f %8.2f" % (report[0], report[1], report[2], report[3], report[4]))
    return reports




def query_report(stock_list):
    reports = []
    if len(stock_list) == 0:
        return reports
    codes = ''
    for stock in stock_list:
        code = stock.stock_code
        if code.startswith('6'):
            code = '0' + code
        else:
            code = '1' + code
        codes = codes + code + ','

    url = 'http://api.money.126.net/data/feed/{}'.format(codes)[:-1]
    session = requests.Session()
    session.trust_env = False
    r = session.get(url)
    text = r.text[len('_ntes_quote_callback('): -2]
    json_obj = json.loads(text)
    for key in json_obj.keys():
        item_obj = json_obj[key]
        try:
            reports.append((item_obj['code'][1:], item_obj['name'], item_obj['price'], item_obj['updown'], item_obj['percent'] * 100))
        except Exception:
            pass

    reports.sort(key=lambda x:x[4])

    print("%-10s %-10s %8s %8s %8s" % ('code', 'name', 'price', 'chg', 'chg_per'))
    for report in reports:
        print("%-10s %-10s %8.2f %8.2f %8.2f" % (report[0], report[1], report[2], report[3], report[4]))


if __name__ == '__main__':
    query_close([StockConfig.Stock('002040', '南京港')], '2017-01-09')