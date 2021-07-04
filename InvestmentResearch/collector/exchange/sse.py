# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Any, Dict, List
from enum import Enum
import json

import requests

from ...utility import CONFIGS
from ...database.model import Stock, Exchange


class StockType(Enum):
    ListedOnMainBoardA = 1      # 已上市，主板A股
    ListedOnMainBoardB = 2      # 已上市，主板B股
    ListedOnStarBoardB = 8      # 已上市，科创板
    Listing = 3         # 待上市
    Paused = 4          # 暂停上市
    Terminated = 5      # 终止上市


def get_stock_info_from_sse(stock_type: StockType) -> List[Stock]:
    result: List[Stock] = []
    temp: List[Dict[str, Any]] = []

    http_header: Dict[str, str] = CONFIGS['http_header']
    http_header['Referer'] = 'http://www.sse.com.cn/'

    page_size: int = 500

    # TODO: the number, 97956, in string 'jsonpCallback97956', how to produce it?
    url: str = 'http://query.sse.com.cn/security/stock/getStockListData2.do' \
               '?&jsonCallBack=jsonpCallback97956&isPagination=false&stockCode=' \
               '&csrcCode=&areaName=&stockType={stock_type}&pageHelp.cacheSize=1&pageHelp.beginPage={page}' \
               '&pageHelp.pageSize={page_size}&pageHelp.pageNo={page}&_=1624790621466'

    page_count: int = 0
    session = requests.Session()
    session.headers.update(http_header)
    response = session.get(url.format(stock_type=stock_type.value, page_size=page_size, page=1))

    if response.status_code == 200:
        response.encoding = 'utf-8'
        content: str = response.text
        data = json.loads(content[19:-1])
        if page_count == 0:
            page_count = data['pageHelp']['pageCount']
        print(page_count)
        print(data)
        # for k, v in result.items():
        #     print(k, ': ', v)
        for item in data['pageHelp']['data']:
            temp.append(
                {
                    'exchange': Exchange.get(Exchange.symbol == 'SSE'),
                    'symbol': item['SECURITY_CODE_A'],
                    'name': item['SECURITY_ABBR_A'],
                    'listing_date': item['LISTING_DATE'],
                }
            )
            print(item)
    else:
        print('Error')

        print('*' * 10)
        print('Session header:')
        print(session.headers)

        print('*' * 10)
        print('Response text:')
        print(response.text)

    for item in temp:
        print(item)
    return result
