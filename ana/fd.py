# -*- coding:utf-8 -*-
import requests
import csv
import os


def download_data(stock_code):
    res = requests.get('http://money.finance.sina.com.cn/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/{}/ctrl/all.phtml'.format(stock_code))
    with open('{}.csv'.format(stock_code), 'wb'.format(stock_code)) as f:
        f.write(res.content)


def read_data(stock_code):
    array = []
    with open('{}.csv'.format(stock_code)) as csvFile:
        spamreader = csv.reader(csvFile, delimiter='\t')
        row_len = 0
        for row in spamreader:
            if row_len == 0:
                row_len = len(row)

            while row_len != 0 and len(row) < row_len:
                row.append('0')
            array.append(row[:-1]) # 去掉最后一个的无用数据
    return array


