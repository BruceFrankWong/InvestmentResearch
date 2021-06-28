# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict
from enum import Enum
import json

import requests


class StockType(Enum):
    ListedOnMainBoardA = 1      # 已上市，主板A股
    ListedOnMainBoardB = 2      # 已上市，主板B股
    ListedOnStarBoardB = 8      # 已上市，科创板
    Listing = 3         # 待上市
    Paused = 4          # 暂停上市
    Terminated = 5      # 终止上市


def get_stock_info_from_sse(stock_type: StockType):
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
        'Referer': 'http://www.sse.com.cn/',
    }

    url: str = 'http://query.sse.com.cn/security/stock/getStockListData2.do' \
               '?&jsonCallBack=jsonpCallback97956&isPagination=false&stockCode=' \
               '&csrcCode=&areaName=&stockType={stock_type}&pageHelp.cacheSize=1&pageHelp.beginPage=1' \
               '&pageHelp.pageSize=100&pageHelp.pageNo=1&_=1624790621466'
    content: str
    session = requests.Session()
    response = session.get(url.format(stock_type=stock_type), headers=header)

    if response.status_code == 200:
        if 'Set-Cookie' not in response.headers.keys():
            print('OK, 2')
            response.encoding = 'utf-8'
            content = response.text
            print(content)
            result = json.loads(content[19:-1])
            print(type(result))
            print(result)
            for k, v in result.items():
                print(k, ': ', v)
            for item in result['result']:
                print(item)


if __name__ == '__main__':
    get_stock_info_from_sse(StockType.ListedOnMainBoardA)
