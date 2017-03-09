# -*-coding:utf-8 -*-
import StockIO
import StockConfig
import StockFilter
import StockIndicator
import numpy as np


def stat_chg(stock_list, from_date, to_date, kline_type=StockConfig.kline_type_day):
    reports = []
    if len(stock_list) == 0:
        return reports

    for stock in stock_list:
        frome_position = StockIndicator.position(from_date, stock.stock_code, kline_type)
        to_position = StockIndicator.position(to_date, stock.stock_code, kline_type)
        if frome_position is not None and to_position is not None:
            kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_day)
            pre_close = float(kline[frome_position][2])
            close = float(kline[to_position][2])
            reports.append((stock.stock_code, stock.stock_name, close, close - pre_close, (close - pre_close)/pre_close * 100))

    reports.sort(key=lambda x: x[4])

    print("%-10s %-10s %8s %8s %8s" % ('code', 'name', 'price', 'chg', 'chg_per'))
    for report in reports:
        print("%-10s %-10s %8.2f %8.2f %8.2f" % (report[0], report[1], report[2], report[3], report[4]))
    return reports

def stat_vb(stock_list, peoriod=20, x_position=-10, min_item=360):
    vbs = []
    for stock in stock_list:
        origin_kline = StockIO.get_kline(stock.stock_code, kline_type=StockConfig.kline_type_day)
        if origin_kline.shape[0] < min_item:
            continue
        from_position = x_position - peoriod + 1
        to_position = None if x_position == -1 else x_position
        kline = origin_kline[from_position:to_position]
        open = kline[:, 1].astype(np.float)
        close = kline[:, 2].astype(np.float)
        high = kline[:, 3].astype(np.float)
        low = kline[:, 4].astype(np.float)
        zf = abs((high - low) / low * 100)
        zf = np.delete(zf, [np.argmax(zf), np.argmin(zf)]) # 去掉最大值和最小值
        chg = (np.max(high) - np.min(low))/ np.min(low) * 100
        vb_factor = np.sum(zf) / chg * 100
        buy_facotr = (close[-1] - np.min(low)) / (np.max(high) - np.min(low)) * 100
        vbs.append((stock, float('%.2f'% vb_factor), float('%.2f' % buy_facotr)))

    vbs.sort(key=lambda x:x[1])
    return vbs


if __name__ == '__main__':
    stock_list = [StockConfig.Stock('601766', 'ZGZC')]
    vbs = stat_vb(StockIO.get_stock('sha'))
    print(vbs)
    vbs.sort(key=lambda x:x[2])
    print(vbs)
