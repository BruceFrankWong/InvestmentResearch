# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Any, Dict, List, Optional
from enum import Enum
import json
import datetime as dt

import requests

from ...utility import CONFIGS
from ..utility import normalize_stock_name


StockData = Dict[str, Any]


class StockTypeSSE(Enum):
    ListedOnMainBoardA = 1      # 已上市，主板A股
    ListedOnMainBoardB = 2      # 已上市，主板B股
    ListedOnStarBoard = 8       # 已上市，科创板
    ToBeListed = 3         # 待上市
    Paused = 4          # 暂停上市
    Terminated = 5      # 终止上市


def crawl(stock_type: StockTypeSSE, page: int = 1, page_size: int = 500) -> Optional[str]:
    """
    Crawl data, and return as <str>.
    """
    # The url which to be crawled.
    # TODO: the number, 97956, in string 'jsonpCallback97956', how to produce it?
    url: str = 'http://query.sse.com.cn/security/stock/getStockListData2.do' \
               '?&jsonCallBack=jsonpCallback97956&isPagination=false&stockCode=' \
               '&csrcCode=&areaName=&stockType={stock_type}&pageHelp.cacheSize=1&pageHelp.beginPage={page}' \
               '&pageHelp.pageSize={page_size}&pageHelp.pageNo={page}&_=1624790621466'

    # HTTP header.
    http_header: Dict[str, str] = CONFIGS['http_header']
    http_header['Host'] = 'query.sse.com.cn'
    http_header['Referer'] = 'http://www.sse.com.cn/'

    response = requests.get(
        url.format(
            stock_type=stock_type.value,
            page=page,
            page_size=page_size
        ),
        headers=http_header
    )
    if response.status_code == 200:
        response.encoding = 'utf-8'
        return response.text
    else:
        return None


def parse(data: Dict[str, Any]) -> List[StockData]:
    result: List[StockData] = []

    exchange: str = 'SSE'
    symbol: str

    for item in data['pageHelp']['data']:
        if item['SECURITY_CODE_A'] != '-':
            symbol = item['SECURITY_CODE_A']
            result.append(
                {
                    'exchange': exchange,
                    'symbol': symbol,
                    'name': normalize_stock_name(item['SECURITY_ABBR_A']),
                    'market': '科创板' if symbol[:3] == '688' else '主板',
                    'listing_date': dt.date.fromisoformat(item['LISTING_DATE']),
                    'terminated_date': None if item['CHANGE_DATE'] == '-' else dt.date.fromisoformat(
                        item['CHANGE_DATE']
                    )
                }
            )
        if item['SECURITY_CODE_B'] != '-':
            symbol = item['SECURITY_CODE_B']
            result.append(
                {
                    'exchange': exchange,
                    'symbol': symbol,
                    'name': normalize_stock_name(item['SECURITY_ABBR_B']),
                    'market': 'B股',
                    'listing_date': dt.date.fromisoformat(item['LISTING_DATE']),
                    'terminated_date': None if item['CHANGE_DATE'] == '-' else dt.date.fromisoformat(
                        item['CHANGE_DATE']
                    )
                }
            )
    return result


def get_stock_info_from_sse(stock_type: StockTypeSSE) -> List[StockData]:
    stock_data_list: List[StockData] = []

    total_page: int = 0
    current_page: int = 1

    # get total pages.
    result = crawl(
        stock_type=stock_type,
        page=current_page
    )
    if result:
        data = json.loads(result[19:-1])
        total_page = data['pageHelp']['pageCount']
    else:
        print(f'Error occurred when getting page count of {stock_type.name}')

    # Get each page.
    for current_page in range(1, total_page + 1):
        result = crawl(
            stock_type=stock_type,
            page=current_page
        )
        if result:
            data = json.loads(result[19:-1])
            stock_data_list.extend(parse(data))
        else:
            print(f'Error occurred when crawling {stock_type.name}')

    return stock_data_list


def get_all_stock_info_from_sse() -> List[StockData]:
    stock_type_list: List[StockTypeSSE] = [
        StockTypeSSE.ListedOnMainBoardA,
        StockTypeSSE.ListedOnMainBoardB,
        StockTypeSSE.ListedOnStarBoard,
        StockTypeSSE.Paused,
        StockTypeSSE.Terminated
    ]

    stock_data_dict: Dict[str, StockData] = {}
    temp: List[StockData]
    for stock_type in stock_type_list:
        print(f'crawling {stock_type.name} from SSE ...', end='')
        temp = get_stock_info_from_sse(stock_type)
        print(f' finished. {len(temp)} data found.')
        for item in temp:
            if item['symbol'] not in stock_data_dict.keys():
                stock_data_dict[item['symbol']] = item
            # elif stock_type == StockTypeSSE.Paused:
            #     # stock_data_list[item['symbol']] = item
            #     print(f'    {item["symbol"]} already exists, currently crawl {stock_type.name}.')
            # elif stock_type == StockTypeSSE.Terminated:
            #     # stock_data_list[item['symbol']] = item
            #     print(f'    {item["symbol"]} already exists, currently crawl {stock_type.name}.')
            # else:
            #     print(f'    {item["symbol"]} already exists, currently crawl {stock_type.name}.')

    stock_data_list: List[StockData] = [stock_data_dict[x] for x in stock_data_dict.keys()]
    return stock_data_list
