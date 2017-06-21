# -*- coding:utf-8 -*-
import requests
import json
from StockConfig import Stock
from StockDownloader import write_stock_pool


def p_hs(output, min_hs=1, max_hs=10, page=1):
    url = 'http://screener.finance.sina.com.cn/znxg/data/json.php/SSCore.doView'
    session = requests.Session()
    session.trust_env = False
    r = session.post(url, data={'page':page, 'num':'20', 'sort':'', 'asc':'0',
                                'field0':'stocktype', 'field1':'sinahy', 'field2':'diyu',
                                'value0':'*', 'value1':'*', 'value2':'*',
                                'field3':'ssturnover', 'max3':max_hs, 'min3':min_hs})

    s = r.text[1:-1]
    s = s.replace('symbol','"symbol"')
    s = s.replace('name', '"name"')
    s = s.replace('ssturnover', '"ssturnover"')
    s = s.replace('items', '"items"')
    s = s.replace(',total:', ',"total":')
    s = s.replace('page_total', '"page_total"')
    s = s.replace(',page:', ',"page":')
    s = s.replace('num_per_page', '"num_per_page"')

    print(s)
    # 获取json对象
    r = json.loads(s)
    for item in r['items']:
        if not item['symbol'][2:].startswith('300') and not item['symbol'][2:].startswith('603'):
            output.append(Stock(item['symbol'][2:], item['name']))

    size = r['page_total']
    if page < size:
        page = page + 1
        p_hs(output, page=page)


result = []
p_hs(result)
write_stock_pool('hs', result)