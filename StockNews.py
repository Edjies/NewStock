# -*- conding:utf-8 -*-
import sqlite3
import requests
import json

def init_stock_table():
    conn = sqlite3.connect('newstock.db')
    cursor = conn.cursor()
    cursor.execute('create table cnstock24_gg ('
                   'id integer primary key autoincrement, '
                   'news_id varchar(20),'
                   'datetime varchar(20), '
                   'des text, '
                   'stock_code varchar(10), '
                   'stock_name varchar(10))')

    cursor.execute('create table cnstock24_bk ('
                   'id integer primary key autoincrement, '
                   'news_id varchar(20), '
                   'datetime varchar(20), '
                   'des text, '
                   'bk_code varchar(10), '
                   'bk_name varchar(10))')
    cursor.close()
    conn.commit()
    conn.close()

def init_news_list():
    last_id = get_last_news_id()
    first = True
    minid = 0
    session = requests.Session()
    session.trust_env = False
    while minid > 10  or first:
        url = 'http://app.cnstock.com/api/theme/get_theme_list?maxid=0&minid={}&size=20'.format(minid)
        r = session.get(url)
        j = json.loads(r.text)
        print(r.text)
        first = False
        if j['status'] == 1:
            items = j.get('item', [])
            for item in items:
                news_id = item['id']
                datetime = item['datetime']
                des = item['des']
                minid = item['order']
                xggg = item.get('xggg', [])
                xgbk = item.get('xgbk', [])
                if news_id <= last_id:
                    return
                conn = sqlite3.connect('newstock.db')
                cursor = conn.cursor()
                for stock in xggg:
                    cursor.execute('INSERT INTO cnstock24_gg (news_id, datetime, des, stock_code, stock_name)  VALUES (?, ?, ?, ?, ?)', (news_id, datetime, des, stock['code'][2:], stock['name']))
                for stock in xgbk:
                    cursor.execute('INSERT INTO cnstock24_bk (news_id, datetime, des, bk_code, bk_name)  VALUES (?, ?, ?, ?, ?)',(news_id, datetime, des, stock['bk_id'], stock['name']))
                cursor.close()
                conn.commit()
                conn.close()



def get_last_news_id():
    id = ''
    conn = sqlite3.connect('newstock.db')
    cursor = conn.cursor()
    cursor.execute('select news_id from cnstock24_gg limit 1')
    if cursor.rowcount == 1:
       id = cursor.fetchone()[0]
    cursor.close()
    conn.commit()
    conn.close()
    return id




if __name__=='__main__':
    # init_stock_table()
    # init_news_list()
    conn = sqlite3.connect('newstock.db')
    cursor = conn.cursor()
    cursor.execute(
    'select stock_code, stock_name, count(*) as count from cnstock24_gg'
               '  where datetime > \'2017-07-00 00:00:00\' and datetime < \'2017-07-20 00:00:00\''
               ' group by stock_code'
               ' having count > 1'
               ' order by count desc')

    for item in cursor.fetchall():
        print(item)

    cursor.execute(
    'select bk_code, bk_name, count(*) as count from cnstock24_bk'
    ' where datetime > \'2017-07-00 00:00:00\' and datetime < \'2017-07-20 00:00:00\''
    ' group by bk_code'
    ' having count > 1'
    ' order by count desc')

    for item in cursor.fetchall():
        print(item)
    cursor.close()
    conn.commit()
    conn.close()


