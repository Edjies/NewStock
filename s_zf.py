# -*- coding:utf-8 -*-
import StockIO
import StockConfig
import StockIndicator
import numpy as np
def filter_by_zf(stock_list, kline_type=StockConfig.kline_type_day, x_position=-1, period=10, limit_chg=(30, 100), limit_avg_zf=(8, 200), limit_bottom=20, min_item=360):
    result=[]
    for stock in stock_list:
        origin_kline = StockIO.get_kline(stock.stock_code, kline_type=kline_type)
        if origin_kline.shape[0] < min_item:
            continue

        print(stock.stock_code)
        from_position = x_position - period + 1
        to_position = None if x_position == -1 else  x_position + 1
        kline = origin_kline[from_position:to_position]
        open = kline[:, 1].astype(np.float)
        close = kline[:, 2].astype(np.float)
        high = kline[:, 3].astype(np.float)
        low = kline[:, 4].astype(np.float)
        zf = abs((high - low) / low * 100)
        zf = np.delete(zf, [np.argmax(zf), np.argmin(zf)])  # 去掉最大值和最小值
        chg = (np.max(close) - np.min(close)) / np.min(close) * 100
        print(close)
        print(np.max(close), np.min(close))
        avg_zf = np.average(zf)
        #print(chg, avg_zf)
        if limit_chg[0] < chg < limit_chg[1] and limit_avg_zf[0] < avg_zf < limit_avg_zf[1]:
            last_close = close[-1]
            if (close[-1] - np.min(close)) / (np.max(high) - np.min(close)) * 100 < limit_bottom:
                result.append([stock, chg, avg_zf,  close[-1]])

    return result

if __name__ == '__main__':
    position = StockIndicator.position('2017-01-16', '601398', kline_type=StockConfig.kline_type_day)
    print(filter_by_zf(StockIO.get_stock('sha'), x_position=-2, kline_type=StockConfig.kline_type_week, min_item=120))
    # for test single stock
    #stock_list = [StockConfig.Stock('600072', '')]
    #print(filter_by_zf(stock_list, x_position=position))
