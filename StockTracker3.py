# -*-coding:utf-8 -*-
import requests
import json
import os
import numpy as np
import StockConfig
from tkinter import messagebox
import time

track_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, os.pardir, 'stock', 'track'))
def track(track_file='position_track.txt'):
    """
    :param targets: 需要追踪的目标集合
    @:param code:
    @:param price:
    :return:
    """
    # 读取本地数据
    stock_data = []
    with open('{}/{}'.format(StockConfig.path_track, track_file), 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if not line.startswith("#"):
                stock_data.append(line.strip('\n').split(','))

    page = 0
    pageNum = 40

    print(len(stock_data))
    result = []
    while page * pageNum < len(stock_data):
        time.sleep(3)
        from_position = page * pageNum
        to_position = min((page + 1) * pageNum, len(stock_data))

        data = stock_data[from_position:to_position]
        #data = stock_data[(page * pageNum):(min((page + 1) * pageNum, len[stock_data]))]
        page += 1
        data = np.array(data)
        # 请求网络数据
        codes = ''
        for code in data[:, 0]:
            if code.startswith('6'):
                code = '0' + code
            else:
                code = '1' + code
            codes = codes + code + ','

        session = requests.Session()
        session.trust_env = False
        url = 'http://api.money.126.net/data/feed/{}'.format(codes)[:-1]
        print(url)
        r = session.get(url)
        quote = json.loads(r.text[len('_ntes_quote_callback('): -2])

        print(data)
        # 分析数据
        for target in data:
            print(target)
            target_code = target[0]
            low_to = float(0 if target[1] == '' else float(target[1]))
            high_to = float(0 if target[2] == '' else float(target[2]))
            if target_code.startswith('6'):
                target_code = '0' + target_code
            else:
                target_code = '1' + target_code
            cur_price = float(quote[target_code]['price'])
            if target[0] == '000982':
                print(cur_price)
            message = ''
            if low_to != 0 and cur_price <= low_to:
                message = target_code[1:] + '跌到目标价位:' +str(low_to)
            elif high_to != 0 and cur_price >= high_to:
                print(cur_price, high_to)
                message = target_code[1:] + '涨到目标价位:' + str(high_to)

            if message != '':
                result.append((target[0], cur_price, low_to, high_to, target[3]))
                #messagebox.showinfo("tips", message)


            # # analysis
            # if cur_price >= price_uts or cur_price <= price_dtb:
            #     result.append([target[0], cur_price, price_uts, price_dtb, 's' if cur_price >= price_uts else 'b', datetime.datetime.now().strftime('%H:%m')])
        print(len(result))
        print(result)
    return result

    # tk显示结果

if __name__=="__main__":

    #while True:
        try:
            print(track('level_1_track.txt'))

        except Exception as e:
            print(e)
            pass
        time.sleep(15)

        # 如果当前时间下午15点，则中止
