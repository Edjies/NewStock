# -*- coding:utf-8 -*-
import requests
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook
import xlrd
import csv





# res = requests.get('http://money.finance.sina.com.cn/corp/go.php/vDOWN_ProfitStatement/displaytype/4/stockid/000826/ctrl/all.phtml')
# with open('data/temp/aa.csv', 'wb') as f:
#     f.write(res.content)
# data = np.loadtxt('data/temp/aa.csv',   delimiter=None, dtype=str, max_rows=2)
# print(data)
# print(data.shape)
array = []
with open('data/temp/aa.csv') as csvFile:
    spamreader  = csv.reader(csvFile, delimiter='\t')
    row_len = 0
    for row in spamreader:

        if row_len == 0:
            row_len = len(row)

        while row_len != 0 and len(row) < row_len:
            row.append('0')

        array.append(row[:-1])

### find rows
def find_rows(tag):
    for row in array:
        if row[0] == tag:
            return row[1:]


y_data = find_rows("营业收入")
print(y_data)
y_data.reverse()

y_data = [(float(i) / (100 * 10000)) for i in y_data]
print(y_data)

x_data = array[0][1:]
x_data.reverse()
x = np.array(x_data, dtype=str)
y = np.array(y_data, dtype=float)
plt.figure()
plt.yticks(np.arange(min(y_data), max(y_data) + 1, (max(y_data) - min(y_data)) / 20))
plt.xticks(rotation='vertical')
plt.plot(x, y)
plt.show()

# x=np.linspace(0,10,1000)#X轴数据
# y1=np.sin(x)#Y轴数据
# y2=np.cos(x**2)#Y轴数据  x**2即x的平方
#
#
# plt.figure(figsize=(8,4))
#
# plt.plot(x,y1,label="$sin(x)$",color="red",linewidth=2)#将$包围的内容渲染为数学公式
# plt.plot(x,y2,"b--",label="$cos(x^2)$")
# plt.show()
