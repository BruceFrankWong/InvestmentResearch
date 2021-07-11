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


class InfoTypeSZSE(Enum):
    StockListedOnA = {'catalog_id': '1110', 'tab_key': 1}       # A股
    StockListedOnB = {'catalog_id': '1110', 'tab_key': 2}       # B股
    StockListedCDR = {'catalog_id': '1110', 'tab_key': 3}       # CDR, Chinese Depository Receipt, 中国存托凭证
    StockListedOnAAndB = {'catalog_id': '1110', 'tab_key': 4}   # A+B股
    StockPaused = {'catalog_id': '1793_ssgs', 'tab_key': 1}         # 暂停上市
    StockTerminated = {'catalog_id': '1793_ssgs', 'tab_key': 2}     # 终止上市


class CatalogId(Enum):
    StockListed = '1110'
    StockTerminated = '1793_ssgs'


def crawl(stock_type: InfoTypeSZSE, page: int = 1) -> Optional[str]:
    """
    Crawl data, and return as <str>.
    """
    # The url which to be crawled.
    # TODO: the number followed <random>, 0.43792128180408896, how to produce it?
    url: str = 'http://www.szse.cn/api/report/ShowReport/data' \
               '?SHOWTYPE=JSON&CATALOGID={catalog}&TABKEY=tab{tab}&PAGENO={page}&random=0.43792128180408896'

    # HTTP header.
    http_header: Dict[str, str] = CONFIGS['http_header']
    http_header['Host'] = 'www.szse.cn'
    http_header['Referer'] = 'http://www.szse.cn/market/product/stock/list/index.html'

    response = requests.get(
        url.format(
            catalog=stock_type.value['catalog_id'],
            tab=stock_type.value['tab_key'],
            page=page
        ),
        headers=http_header
    )
    if response.status_code == 200:
        response.encoding = 'utf-8'
        return response.text
    else:
        return None


def get_stock_info_from_szse(stock_type: InfoTypeSZSE) -> List[StockData]:
    stock_data_list: List[StockData] = []

    result: str
    data: Dict[str, Any]
    current_page: int = 1
    total_page: int = 0

    # get total pages.
    result = crawl(stock_type=stock_type, page=current_page)
    if result:
        data = json.loads(result)
        total_page = data[stock_type.value['tab_key'] - 1]['metadata']['pagecount']
    else:
        print(f'Error occurred when getting page count of {stock_type.name}')

    # Get each page.
    for current_page in range(1, total_page + 1):
        result = crawl(stock_type=stock_type, page=current_page)
        if result:
            data = json.loads(result)[stock_type.value['tab_key'] - 1]
            for item in data['data']:
                if stock_type == InfoTypeSZSE.StockListedOnA:
                    stock_data_list.append(
                        {
                            'exchange': 'SZSE',
                            'symbol': item['agdm'],
                            'name': normalize_stock_name(item['agjc'][94:-8]),
                            'market': item['bk'],
                            'listing_date': dt.date.fromisoformat(item['agssrq']),
                        }
                    )
                elif stock_type == InfoTypeSZSE.StockListedOnB:
                    stock_data_list.append(
                        {
                            'exchange': 'SZSE',
                            'symbol': item['bgdm'],
                            'name': normalize_stock_name(item['bgjc'][94:-8]),
                            'market': 'B股',
                            'listing_date': dt.date.fromisoformat(item['bgssrq']),
                        }
                    )
                elif stock_type == InfoTypeSZSE.StockListedOnAAndB:
                    stock_data_list.append(
                        {
                            'exchange': 'SZSE',
                            'symbol': item['agdm'],
                            'name': normalize_stock_name(item['agjc'][94:-8]),
                            'market': '主板',
                            'listing_date': dt.date.fromisoformat(item['agssrq']),
                        }
                    )
                    stock_data_list.append(
                        {
                            'exchange': 'SZSE',
                            'symbol': item['bgdm'],
                            'name': normalize_stock_name(item['bgjc']),
                            'market': 'B股',
                            'listing_date': dt.date.fromisoformat(item['bgssrq']),
                        }
                    )
                elif stock_type == InfoTypeSZSE.StockPaused or stock_type == InfoTypeSZSE.StockTerminated:
                    symbol = item['zqdm']
                    if symbol[0] == '2':
                        market = 'B股'
                    elif symbol[0] == '3':
                        market = '创业板'
                    else:
                        market = '主板'
                    if stock_type == InfoTypeSZSE.StockPaused:
                        stock_data_list.append(
                            {
                                'exchange': 'SZSE',
                                'symbol': symbol,
                                'name': normalize_stock_name(item['zqjc']),
                                'market': market,
                                'listing_date': dt.date.fromisoformat(item['ssrq']),
                                'paused_date': dt.date.fromisoformat(item['ztrq'])
                            }
                        )
                    else:
                        stock_data_list.append(
                            {
                                'exchange': 'SZSE',
                                'symbol': symbol,
                                'name': normalize_stock_name(item['zqjc']),
                                'market': market,
                                'listing_date': dt.date.fromisoformat(item['ssrq']),
                                'terminated_date': dt.date.fromisoformat(item['zzrq'])
                            }
                        )
        else:
            print(f'Error occurred when getting page count of {stock_type.name}')

    return stock_data_list


def get_all_stock_info_from_szse() -> List[StockData]:
    stock_type_list: List[InfoTypeSZSE] = [
        InfoTypeSZSE.StockListedOnA,        # A股
        InfoTypeSZSE.StockListedOnB,        # B股
        InfoTypeSZSE.StockListedCDR,        # CDR, Chinese Depository Receipt, 中国存托凭证
        # It's not necessary, cause each item exists either in StockListedOnA or StockListedOnB.
        # InfoTypeSZSE.StockListedOnAAndB,  # A+B股.
        InfoTypeSZSE.StockPaused,           # 暂停上市
        InfoTypeSZSE.StockTerminated,       # 终止上市
    ]

    stock_data_dict: Dict[str, StockData] = {}
    temp: List[StockData]
    for stock_type in stock_type_list:
        print(f'crawling {stock_type.name} from SZSE ...', end='')
        temp = get_stock_info_from_szse(stock_type)
        print(f' finished. {len(temp)} data found.')
        for item in temp:
            if item['symbol'] not in stock_data_dict.keys():
                stock_data_dict[item['symbol']] = item
            elif stock_type == InfoTypeSZSE.StockPaused:
                stock_data_dict[item['symbol']] = item
            else:
                print(f'{item["symbol"]} already exists, currently crawl {stock_type.name}.')

    stock_data_list: List[StockData] = [stock_data_dict[x] for x in stock_data_dict.keys()]
    return stock_data_list
