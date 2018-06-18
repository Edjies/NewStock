# -*- coding:utf-8 -*-
from StockUtils import data_to_tdx_phone
import StockConfig

def data_to_phone(from_file, to_file):
    sma_data = []
    with open('{}/{}'.format(StockConfig.path_track, from_file), 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if not line.startswith("#") and not '\n' == line:
                data = line.strip('\n').split(',')
                sma_data.append(data[0])


    with open('{}/{}'.format(StockConfig.path_track, to_file), mode='w', encoding='utf-8') as f:
        for stock_code in sma_data:
            f.write("{}\n".format(('1' if stock_code.startswith('6') else '0') + stock_code))

    #data_to_tdx_phone(sma_data=sma_data)
    pass

data_to_phone('2_sma_track.txt', 'his_sma.txt')
data_to_phone('2_dow_track.txt', 'his_dow.txt')