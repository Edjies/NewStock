# -*-coding:utf-8 -*-
import StockConfig
import json
from StockConfig import Stock

l1 = [Stock('1', 'a'), Stock('2', 'b'), Stock('3', 'c')]
l2 = [Stock('1', 'a'), Stock('3', 'c')]

print([x for x in l1 if x in l2])
