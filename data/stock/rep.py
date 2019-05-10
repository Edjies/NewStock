
stock_list = []
with open('pool', mode='r', encoding='utf-8') as f:
    for line in f.readlines():
        if ',' in line:
            stock = line.strip('\n').split(',')
            stock_list.append((stock[1], stock[0]))

with open('gzw', mode='w', encoding='utf-8') as f:
    for stock in stock_list:
        f.write(stock[0]+','+stock[1] )
        f.write('\n')
print(stock_list)