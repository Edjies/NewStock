
# -*-coding:utf-8 -*-
import time
import requests
import json
from StockIO import *


def get_stock_pool(source):
    """
    数据维护之获取全部股票代码，并保存在本地：
    :param source:  数据源
    """
    if source == source_sina:
        write_stock_pool('sha', get_stock_pool_from_sina(sina_node_sh_a, 1))
        write_stock_pool('sza', get_stock_pool_from_sina(sina_node_sz_a, 1))


def download_stock_kline(source, kline_type):
    """
    数据维护之获取K线数据
    :param source:
    :param kline_type:
    """
    if source == source_tencent:
        get_kline_from_tencent(get_stock('sha'), kline_type)
        get_kline_from_tencent(get_stock('sza'), kline_type)


def get_stock_pool_from_sina(node, page):
    """
    sina批量获取当日行情信息排名接口, 现用于获取全部股票数据
    :param node:
    :param page:
    :return:
    """
    stock_list = []
    time.sleep(1)
    print('start load {} page'.format(str(page)))
    url = "http://gu.sina.cn/hq/api/openapi.php/Wap_Market_Center.getHQNodeData?" \
          "num=40&sort=changepercent&asc=0&_s_r_a=init&node={node}&page={page}&dpc=1" \
          .format(node=node, page=page)

    session = requests.Session()
    session.trust_env = False
    r = session.get(url)
    # 解析数据
    json_obj = json.loads(r.text)
    for item in json_obj['result']['data']['data']:
        stock_list.append(Stock(item['code'], item['name']))
    #print(stock_list)
    size = json_obj['result']['data']['status']['pagetatol']
    if page < size:
        stock_list += get_stock_pool_from_sina(node, page + 1)
    return stock_list


def get_kline_from_tencent(stock_list, stock_type):
    """
    从tencent接口获取k线信息，并保存在本地
    :param stock_list:
    :param stock_type:
    :return:
    """
    end = True
    try:
        for stock in stock_list:
            time.sleep(0.1)
            code = stock.stock_code
            if code.startswith('6'):
                code = 'sh' + code
            else:
                code = 'sz' + code

            path = '{}/{}/{}'.format(path_kline, stock_type, stock.stock_code)
            if not os.path.exists(path):
                end = False
                #time.sleep(100)
                print("开始下载 {} 的数据".format(stock.stock_code))
                url = "http://183.57.48.75/ifzqgtimg/appstock/app/fqkline/get?p=1&param={code},{type},,,640,qfq"\
                    .format(code=code, type=stock_type)
                print(url)
                session = requests.Session()
                session.trust_env = False
                r = session.get(url)
                #print(r.text)
                json_obj = json.loads(r.text)
                print(json_obj['code'])
                if json_obj['code'] == 0:
                    if 'qfq{}'.format(stock_type) in json_obj['data'][code]:
                        data = json_obj['data'][code]['qfq{}'.format(stock_type)]
                    else:
                        data = json_obj['data'][code].get('{}'.format(stock_type))
                    #print(data)
                    for index, item in enumerate(data):
                        data[index] = item[0:6]
                    save_kline(path, json.dumps(data))
    except Exception as e:
        if not end:
            print(e)
            time.sleep(2)
            get_kline_from_tencent(stock_list, stock_type)


def upate_kline_day(node, page):
    """
    :param node:
    :param page:
    :return:
    """
    url = "http://gu.sina.cn/hq/api/openapi.php/Wap_Market_Center.getHQNodeData?" \
          "num=40&sort=changepercent&asc=0&_s_r_a=init&node={node}&page={page}&dpc=1" \
        .format(node=node, page=page)

    session = requests.Session()
    session.trust_env = False
    r = session.get(url)
    jsonObj = json.loads(r.text)
    date = jsonObj['result']['data']['status']['date']
    for item in jsonObj['result']['data']['data']:
        # 最新数据
        new_item = [date, str(item['open']), str(item['trade']), str(item['high']), str(item['low']), str(item['volume'])]
        # 旧数据
        code = item['code']
        print('正在更新{}'.format(code))
        try:
            with open('{}/{}'.format(path_kline_day, code), 'r', encoding='utf-8') as f:
                text = f.readline()
                old_kline = json.loads(text)
                last_item = old_kline[-1]
                if last_item[0] == new_item[0]:
                    print('update', new_item, last_item)
                    old_kline[-1] = new_item
                    json_str = json.dumps(old_kline)  # 生成
                    save_kline('{}/{}'.format(path_kline_day, code), json_str)
                else:
                    print('append', new_item, last_item)
                    old_kline.append(new_item)
                    json_str = json.dumps(old_kline)  # 生成
                    save_kline('{}/{}'.format(path_kline_day, code), json_str)
                    # data['data'].append()
        except EnvironmentError  as e:
            print(e)


    size = jsonObj['result']['data']['status']['pagetatol']
    if page < size:
        upate_kline_day(node, page + 1)


def save_kline(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def filter_stock(stock_list):
    """
    StockPool去重
    :param stock_list:
    :return:
    """
    r_stock_list = []
    for stock in stock_list:
        if stock not in r_stock_list:
            r_stock_list.append(stock)
    return r_stock_list


def write_stock_pool(stock_pool_name, stock_list):
    """
    保存Stock池数据
    :param stock_pool_name:  Stock池的名称
    :param stock_list:  Stock列表
    :return:
    """
    stock_list = filter_stock(stock_list)
    print(stock_list)
    stock_list = sorted(stock_list, key=lambda stock_item: stock_item.stock_code)
    print(stock_list)
    if not os.path.exists('data/stock'):
        os.mkdir('data/stock')
    with open('data/stock/{}'.format(stock_pool_name), 'w', encoding='utf-8') as f:
        for stock in stock_list:
            f.write("{},{}\n".format(stock.stock_code, stock.stock_name))

def update_sina_hy_bk():
    pass


def update_sina_gn_bk():
    pass
4

if __name__ == '__main__':
    if not os.path.exists(path_kline_day):
        os.makedirs(path_kline_day)
    if not os.path.exists(path_kline_week):
        os.makedirs(path_kline_week)
    if not os.path.exists(path_kline_month):
        os.makedirs(path_kline_month)

    get_stock_pool(source_sina)
    #update_stock_kline(source_tencent, kline_type_day)
    download_stock_kline(source_tencent, kline_type_day)
    #download_stock_kline(source_tencent, kline_type_week)
    #download_stock_kline(source_tencent, kline_type_month)
    #upate_kline_day(sina_node_sh_a, 1)
    #upate_kline_day(sina_node_sz_a, 1)