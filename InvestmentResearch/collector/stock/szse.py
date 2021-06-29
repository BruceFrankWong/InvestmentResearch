# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict
from enum import Enum
import json

import requests


def get_stock_info_from_szse():
    header: Dict[str, str] = {
        'Accept': 'text/html,'
                  'application/xhtml+xml,'
                  'application/xml;q=0.9,'
                  'image/avif,'
                  'image/webp,'
                  'image/apng,'
                  '*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.114 Safari/537.36',
        'Host': 'www.szse.cn',
        'Referer': 'http://www.szse.cn/market/product/stock/list/index.html',
    }

    url: str = 'http://www.szse.cn/api/report/ShowReport/data' \
               '?SHOWTYPE=JSON&CATALOGID=1110&TABKEY=tab1&PAGENO=1&random=0.43792128180408896'
    content: str
    session = requests.Session()
    response = session.get(url, headers=header)

    if response.status_code == 200:
        print('OK')
        response.encoding = 'utf-8'
        content = response.text
        print(content)
        result = json.loads(content)
        print(type(result))
        print(result)
        # for k, v in result.items():
        #     print(k, ': ', v)
        for item in result:
            print(item)


if __name__ == '__main__':
    get_stock_info_from_szse()
