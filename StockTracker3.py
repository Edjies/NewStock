# -*-coding:utf-8 -*-
import requests
import json
import os
import numpy as np
import StockConfig
import StockIO
from tkinter import messagebox
import time
import datetime
import StockIndicator

track_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, os.pardir, 'stock', 'track'))


def get_track_data(track_file):
    data = []
    with open('{}/{}'.format(StockConfig.path_track, track_file), 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if not line.startswith("#") and not '\n' == line:
                data.append(line.strip('\n').split(','))

    data = np.array(data)
    return data

#1. 定义追踪格式
#2. 读取k线数据



def track():
    """
    :param targets: 需要追踪的目标集合
    @:param code:
    @:param price:
    :return:
    """
    # 读取本地数据
    track_data = get_track_data('2_sma_track.txt')
    kline_map = StockIO.get_kline_map(track_data[:, 0], StockConfig.kline_type_day)

    page = 0
    pageNum = 40
    result = []
    code_list = track_data[:, 0]
    while page * pageNum < len(code_list):
        from_position = page * pageNum
        to_position = min((page + 1) * pageNum, len(code_list))
        data = code_list[from_position:to_position]
        cur_track_data = track_data[from_position:to_position]
        page += 1
        # 请求网络数据
        codes = ''
        for code in data:
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
        for target in cur_track_data:
            target_code = target[0]
            target_sma = 0 if target[2].strip() == '' else int(target[2])
            if target_code.startswith('6'):
                target_code = '0' + target_code
            else:
                target_code = '1' + target_code
            new_date = datetime.datetime.strptime(quote[target_code]['time'], '%Y/%m/%d %H:%M:%S').strftime('%Y-%m-%d')
            kline = kline_map[target_code[1:]]
            old_kline_item = kline[-1]
            new_kline_item = np.array([new_date, quote[target_code]['open'], quote[target_code]['price'], quote[target_code]['high'], quote[target_code]['low'], quote[target_code]['volume']])
            if(new_kline_item[-1] == old_kline_item[-1]):
                kline[-1] = new_kline_item
            else:
                kline = np.row_stack((kline, new_kline_item))

            print(kline[-1])

            if target_sma == 0:
                sma5, sma10, sma20 = StockIndicator.sma(kline, 5, 10, 20)
                price = quote[target_code]['low']
                if(price < sma10[-1]):
                    message = target_code[1:] + '跌破10日线:'
                elif(price < sma20[-1]):
                    message = target_code[1:] + '跌破20日线:'
                else:
                    message = ''
                if message != '':
                    messagebox.showinfo("tips", message)
            else:
                sma, = StockIndicator.sma(kline, target_sma)
                price = quote[target_code]['low']
                if (price < sma[-1]):
                    message = target_code[1:] + '跌破{}日线:'.format(target_sma)
                elif (price < sma[-1]):
                    message = target_code[1:] + '跌破{}日线:'.format(target_sma)
                else:
                    message = ''
                if message != '':
                    messagebox.showinfo("tips", message)




            # # analysis
            # if cur_price >= price_uts or cur_price <= price_dtb:
            #     result.append([target[0], cur_price, price_uts, price_dtb, 's' if cur_price >= price_uts else 'b', datetime.datetime.now().strftime('%H:%m')])
    return result

    # tk显示结果

if __name__=="__main__":

    while True:
        try:
            print(track())

        except Exception as e:
            print(e)
            pass
        time.sleep(10)

        # 如果当前时间下午15点，则中止
