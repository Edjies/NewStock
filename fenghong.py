# -*-coding:utf-8 -*-
"""
根据分红派息情况选股
以2016年的分红派息情况作为参考，根据当前的股票价格，算出预期分红点数，并做排名
"""
import StockIO
import StockConfig
import requests
import json

result = [] #[stock, price, profit, per, date]
stock_list = StockIO.get_stock('sha')
for stock in stock_list:
    kline = StockIO.get_kline(stock.stock_code, StockConfig.kline_type_day)
    result.append([stock, float(kline[:, 2][-1]), 0, 0, ''])
print(result)
for item in result:
    stock_code = item[0].stock_code
    stock_code = 'sh' + stock_code if stock_code.startswith('6') else 'sz' + stock_code
    url = 'http://183.57.48.75/ifzqgtimg/stock/corp/cwbb/search?symbol={}&type=sum&jianjie=1'.format(stock_code)
    session = requests.Session()
    session.trust_env = False
    r = session.get(url)
    json_obj = json.loads(r.text)
    if json_obj['code'] == 0:
        gegu = json_obj['data']['gegu']
        if 'fenhong' in gegu:
            fenhong = gegu['fenhong']
            if len(fenhong) > 1:
                fenhong = fenhong[0]
                date = fenhong['cqr']
                if date.startswith('2016'):
                    item[2] = float(fenhong['fh'])
                    item[3] = item[2] * 10 / item[1]
                    item[3] = float('%.2f'% item[3]) # 格式化为两位小数点
                    item[4] = date
                    continue

result.sort(key=lambda x:x[3])
print(result)

    # 获取分红派息情况






