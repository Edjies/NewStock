# -*- coding:utf-8 -*-
from ana import fd
import numpy as np
import matplotlib.pyplot as plt

def simple(stock_code, *profit_tag):
    fd.download_data(stock_code)
    arr_data = fd.read_data(stock_code)
    fig, axe_list = plt.subplots(len(profit_tag), 1)
    plt.xticks(rotation='vertical')
    for index, tag in enumerate(profit_tag):
        profit_data = []
        for row in arr_data:
            if row[0] == tag:
                 profit_data = row[1:]
                 profit_data.reverse()
                 profit_data = [(float(i) / (10000 * 10000)) for i in profit_data]  # 以亿为单位的浮点数数组

        x_data = arr_data[0][1:]
        x_data.reverse()
        y_data = profit_data
        x = np.array(x_data, dtype=str)
        y = np.array(y_data, dtype=float)
        #plt.yticks(np.arange(min(y_data), max(y_data) + 1, (max(y_data) - min(y_data)) / 20))
        axe_list[index].grid()
        axe_list[index].plot(x[-40:], y[-40:])
    plt.show()


simple('002217', '营业收入', '五、净利润')







