import re

from futu import *

global quote_ctx
global all_stock


def init():
    global quote_ctx
    global all_stock

    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    ret, data = quote_ctx.get_stock_basicinfo(Market.SH, SecurityType.STOCK)
    if ret != RET_OK:
        print('get stock basic info error:', data)
        raise Exception("get stock basic info error")
    all_stock = data[['code', 'name']]


def search_stock_code(name):
    filtered_stock = all_stock[all_stock['name'].str.contains(name, case=False, na=False)]
    if filtered_stock is None or len(filtered_stock) == 0:
        return None
    return filtered_stock.head(1)['code'].values[0]


def get_stock_snapshot(code):
    ret, data = quote_ctx.get_market_snapshot([code])
    if ret == RET_OK:
        if data is None or len(data) == 0:
            return None
        return data.head(1)
    else:
        print('get stock snapshot error:', data)


def search_stock_snapshot(name):
    code = search_stock_code("长虹")
    if code is None:
        return None
    return get_stock_snapshot(code)


def stop():
    quote_ctx.close()
