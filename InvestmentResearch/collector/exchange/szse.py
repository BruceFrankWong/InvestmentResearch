# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict
from enum import Enum
import json

import requests

from ...utility import CONFIGS


def get_stock_info_from_szse():
    http_header: Dict[str, str] = CONFIGS['http_header']
    http_header['Host'] = 'www.szse.cn'
    http_header['Referer'] = 'http://www.szse.cn/market/product/stock/list/index.html'

    url: str = 'http://www.szse.cn/api/report/ShowReport/data' \
               '?SHOWTYPE=JSON&CATALOGID=1110&TABKEY=tab1&PAGENO=1&random=0.43792128180408896'
    content: str
    session = requests.Session()
    session.headers.update(http_header)
    response = session.get(url)

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
