# -*-coding:utf-8 -*-
import requests
import json


def query_report(stock_list):
    if(len(stock_list) == 0):
        return
    reports = []
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
            reports.append((item_obj['code'][1:], item_obj['price'], item_obj['updown'], item_obj['percent'] * 100))
        except Exception:
            pass

    reports.sort(key=lambda x:x[3])

    print("%-10s %8s %8s %8s" % ('code', 'price', 'chg', 'chg_per'))
    for report in reports:
        print("%-10s %8.2f %8.2f %8.2f" % (report[0], report[1], report[2], report[3]))

