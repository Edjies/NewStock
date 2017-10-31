# -*-coding:utf-8 -*-
# import xlrd
# data = xlrd.open_workbook('data/market.xls') # 打开xls文件
# table = data.sheets()[0] # 打开第一张表
# nrows = table.nrows # 获取表的行数
# for i in range(nrows): # 循环逐行打印
#     print(table.row_values(i)[:4]) # 取前十三列
import requests
url = "http://screener.finance.sina.com.cn/znxg/data/json.php/SSCore.doView"
session = requests.Session()
session.trust_env = False
r = session.post(url, data={"page":"1", "num":"20", "sort":"","asc":"0","field0":"stocktype", "field1":"sinahy", "field2":"diyu", "value0":"*","value1":"*",
                            "value2":"*","field3":"ltag", "max3":"26192207", "min3":"1000"}, )
print(r.text)


print('2017-09-12' <= '2017-09-13')