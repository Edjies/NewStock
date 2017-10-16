# -*-coding:utf-8 -*-
import requests
import tkinter as tk
import json
import os
import numpy as np
import datetime
import StockConfig

track_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, os.pardir, os.pardir, 'stock', 'track'))
def track():
    """
    :param targets: 需要追踪的目标集合
    @:param code:
    @:param price:
    :return:
    """
    # 读取本地数据
    data = []
    with open('{}/1_vb_track.txt'.format(StockConfig.path_track), 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if not line.startswith("#"):
                data.append(line.strip('\n').split(','))

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
    result = []
    for target in data:
        target_code = target[0]
        price_uts = float(target[1])
        price_dtb = float(target[2])
        if target_code.startswith('6'):
            target_code = '0' + target_code
        else:
            target_code = '1' + target_code
        cur_price = quote[target_code]['price']
        # analysis
        if cur_price >= price_uts or cur_price <= price_dtb:
            result.append([target[0], cur_price, price_uts, price_dtb, 's' if cur_price >= price_uts else 'b', datetime.datetime.now().strftime('%H:%m')])

    print(result)
    return result

    # tk显示结果


# while True:
#     time.sleep(5)
#     try:
#         track()
#     except Exception as e:
#         print(e)
def main():
    root = tk.Tk()
    w = 200  # width for the Tk root
    h = 250  # height for the Tk root
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen
    x = ws - w - 20
    y = hs - h - 80

    print('%dx%d+%d+%d' % (w, h, x, y))
    # set the dimensions of the screen
    # and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    # root.configure(background='gold')
    root.call('wm', 'attributes', '.', '-topmost', '1')
    root.lift()
    # write list
    listbox = tk.Listbox(root)
    listbox.configure(width=0)
    listbox.pack()

    # listbox.delete(2, 'end')
    def render(mydata):
        listbox.delete(0, 'end')
        for item in mydata:
            listbox.insert('end', item)

    def task():
        render(track())
        root.after(5000, task)

    root.after(1000, task)

    root.mainloop()  # starts the mainloop


main()