# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Any, Dict, List, Optional
from enum import Enum
import json
import datetime as dt

import requests

from ...utility import CONFIGS


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


def crawl(url: str) -> Optional[str]:
    # about HTTP.
    http_header: Dict[str, str] = CONFIGS['http_header']
    http_header['Host'] = 'www.szse.cn'
    http_header['Referer'] = 'http://www.szse.cn/market/product/stock/list/index.html'

    response = requests.get(url, headers=http_header)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        return response.text
    else:
        return None


def get_stock_info_from_szse(info_type: InfoTypeSZSE) -> List[StockData]:
    stock_data_list: List[StockData] = []

    url: str = 'http://www.szse.cn/api/report/ShowReport/data' \
               '?SHOWTYPE=JSON&CATALOGID={catalog}&TABKEY=tab{tab}&PAGENO={page}&random=0.43792128180408896'

    # # 暂停上市
    # url_x = 'http://www.szse.cn/api/report/ShowReport/data' \
    #         '?SHOWTYPE=JSON&CATALOGID=1793_ssgs&TABKEY=tab1&random=0.2969686199255954'
    #
    # # 终止上市
    # url_t = 'http://www.szse.cn/api/report/ShowReport/data' \
    #         '?SHOWTYPE=JSON&CATALOGID=1793_ssgs&TABKEY=tab2&PAGENO=1&random=0.4133067961976815'
    #
    current_page: int = 1
    total_page: int = 0

    # get total pages.
    result = crawl(
        url.format(
            catalog=info_type.value['catalog_id'],
            tab=info_type.value['tab_key'],
            page=current_page
        )
    )
    if result:
        data = json.loads(result)[info_type.value['tab_key'] - 1]
        # print(data)
        total_page = data['metadata']['pagecount']
        # print(total_page)

    # Get each page.
    for current_page in range(1, total_page + 1):
        result = crawl(
            url.format(
                catalog=info_type.value['catalog_id'],
                tab=info_type.value['tab_key'],
                page=current_page
            )
        )
        if result:
            data = json.loads(result)[info_type.value['tab_key'] - 1]
            for item in data['data']:
                # print(item)
                if info_type == InfoTypeSZSE.StockListedOnA:
                    stock_data_list.append(
                        {
                            'exchange': 'SZSE',
                            'symbol': item['agdm'],
                            'name': item['agjc'][94:-8],
                            'market': item['bk'],
                            'listing_date': dt.date.fromisoformat(item['agssrq']),
                        }
                    )
                elif info_type == InfoTypeSZSE.StockListedOnB:
                    stock_data_list.append(
                        {
                            'exchange': 'SZSE',
                            'symbol': item['bgdm'],
                            'name': item['bgjc'][94:-8],
                            'market': 'B股',
                            'listing_date': dt.date.fromisoformat(item['bgssrq']),
                        }
                    )
                elif info_type == InfoTypeSZSE.StockListedOnAAndB:
                    stock_data_list.append(
                        {
                            'exchange': 'SZSE',
                            'symbol': item['agdm'],
                            'name': item['agjc'][94:-8],
                            'market': '主板',
                            'listing_date': dt.date.fromisoformat(item['agssrq']),
                        }
                    )
                    stock_data_list.append(
                        {
                            'exchange': 'SZSE',
                            'symbol': item['bgdm'],
                            'name': item['bgjc'],
                            'market': 'B股',
                            'listing_date': dt.date.fromisoformat(item['bgssrq']),
                        }
                    )
                elif info_type == InfoTypeSZSE.StockPaused or info_type == InfoTypeSZSE.StockTerminated:
                    symbol = item['zqdm']
                    if symbol[0] == '2':
                        market = 'B股'
                    elif symbol[0] == '3':
                        market = '创业板'
                    else:
                        market = '主板'
                    if info_type == InfoTypeSZSE.StockPaused:
                        stock_data_list.append(
                            {
                                'exchange': 'SZSE',
                                'symbol': symbol,
                                'name': item['zqjc'],
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
                                'name': item['zqjc'],
                                'market': market,
                                'listing_date': dt.date.fromisoformat(item['ssrq']),
                                'terminated_date': dt.date.fromisoformat(item['zzrq'])
                            }
                        )

    return stock_data_list


def get_all_stock_info_from_szse() -> Dict[str, StockData]:
    stock_type_list: List[InfoTypeSZSE] = [
        InfoTypeSZSE.StockListedOnA,        # A股
        InfoTypeSZSE.StockListedOnB,        # B股
        InfoTypeSZSE.StockListedCDR,        # CDR, Chinese Depository Receipt, 中国存托凭证
        # It's not necessary, cause each item exists either in StockListedOnA or StockListedOnB.
        # InfoTypeSZSE.StockListedOnAAndB,  # A+B股.
        InfoTypeSZSE.StockPaused,           # 暂停上市
        InfoTypeSZSE.StockTerminated,       # 终止上市
    ]

    stock_data_list: Dict[str, StockData] = {}
    temp: List[StockData]
    for stock_type in stock_type_list:
        temp = get_stock_info_from_szse(stock_type)
        for item in temp:
            if item['symbol'] not in stock_data_list.keys():
                stock_data_list[item['symbol']] = item
            elif stock_type == InfoTypeSZSE.StockPaused:
                stock_data_list[item['symbol']] = item
            else:
                print(f'{item["symbol"]} already exists, currently crawl {stock_type.name}.')
    return stock_data_list
