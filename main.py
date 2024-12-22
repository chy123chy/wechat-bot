import os
import asyncio

from urllib.parse import quote

from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    ScanStatus,
)

import stock
from stock import *


def extract_chinese_before_keyword(text, keyword):
    # 使用正则表达式查找包含keyword的字符串
    pattern = rf'([\u4e00-\u9fa5]+)(?={keyword})'
    match = re.search(pattern, text)

    if match:
        # 提取并返回匹配的中文字符串
        return match.group(1)
    else:
        return None


def str_of_num(num):
    """
    递归实现，精确为最大单位值 + 小数点后三位
    """

    def str_of_size(num, level):
        if level >= 2:
            return num, level
        elif num >= 10000:
            num /= 10000
            level += 1
            return str_of_size(num, level)
        else:
            return num, level

    units = ['', '万', '亿']
    num, level = str_of_size(num, 0)
    if level > len(units):
        level -= 1
    return '{}{}'.format(round(num, 3), units[level])


async def on_message(msg: Message):
    """
    Message Handler for the Bot
    """
    name = extract_chinese_before_keyword(msg.text(), "行情")
    if name is not None:
        data = stock.search_stock_snapshot(name)
        if data is None:
            return
        reply = data['name'].values[0] + " " + data['update_time'].values[0] + "\n" + \
                "最新价格：" + str(data['last_price'].values[0]) + "\n" + \
                "今开价格：" + str(data['open_price'].values[0]) + "\n" + \
                "昨收价格：" + str(data['prev_close_price'].values[0]) + "\n" + \
                "最高价格：" + str(data['high_price'].values[0]) + "\n" + \
                "最低价格：" + str(data['low_price'].values[0]) + "\n" + \
                "成交数量：" + str_of_num(data['volume'].values[0]) + "\n" + \
                "成交金额：" + str_of_num(data['turnover'].values[0]) + "\n" + \
                "换手率：" + str(data['turnover_rate'].values[0]) + "%"
        await msg.talker().say(reply)


async def on_scan(
        qrcode: str,
        status: ScanStatus,
        _data,
):
    """
    Scan Handler for the Bot
    """
    print('Status: ' + str(status))
    print('View QR Code Online: https://wechaty.js.org/qrcode/' + quote(qrcode))


async def on_login(user: Contact):
    """
    Login Handler for the Bot
    """
    print(user)
    # TODO: To be written


async def main():
    """
    Async Main Entry
    """
    #
    # Make sure we have set WECHATY_PUPPET_SERVICE_TOKEN in the environment variables.
    # Learn more about services (and TOKEN) from https://wechaty.js.org/docs/puppet-services/
    #
    # It is highly recommanded to use token like [paimon] and [wxwork].
    # Those types of puppet_service are supported natively.
    # https://wechaty.js.org/docs/puppet-services/paimon
    # https://wechaty.js.org/docs/puppet-services/wxwork
    #
    # Replace your token here and umcommt that line, you can just run this python file successfully!
    # os.environ['token'] = 'puppet_paimon_your_token'
    # os.environ['token'] = 'puppet_wxwork_your_token'
    #
    if 'WECHATY_PUPPET_SERVICE_TOKEN' not in os.environ:
        print('''
            Error: WECHATY_PUPPET_SERVICE_TOKEN is not found in the environment variables
            You need a TOKEN to run the Python Wechaty. Please goto our README for details
            https://github.com/wechaty/python-wechaty-getting-started/#wechaty_puppet_service_token
        ''')

    bot = Wechaty()

    bot.on('scan', on_scan)
    bot.on('login', on_login)
    bot.on('message', on_message)

    stock.init()
    await bot.start()

    print('[Python Wechaty] Ding Dong Bot started.')


asyncio.run(main())
