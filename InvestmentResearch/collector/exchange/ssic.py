# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


"""
    SSIC Data API.
    深证信（深圳证券信息有限公司）数据 API。
"""


__all__ = [
    'ResultOfSSIC',
    'SSICResultFormatEnum',
    'SSICIndustryClassificationEnum',
    'get_trading_calendar',
    'get_industry',
]


from typing import Any, Dict, List, Optional
from enum import Enum
import json
import datetime as dt

import requests

from ...utility import CONFIGS


SSIC_API = Dict[str, str]

SSIC_URL: str = 'http://webapi.cninfo.com.cn/api/{category}/{interface}?access_token={token}'


class ResultOfSSIC:
    """
    Result of SSIC.
    """
    _total: int
    _count: int
    _data: List[Dict[str, Any]]

    def __init__(self,
                 total: Optional[int] = 0,
                 count: Optional[int] = 0,
                 data: Optional[List[Dict[str, Any]]] = None
                 ) -> None:
        self._total = total
        self._count = count
        if data:
            self._data = data
        else:
            self._data = []

    @property
    def total(self) -> int:
        return self._total

    @total.setter
    def total(self, value: int) -> None:
        self._total = value

    @property
    def count(self) -> int:
        return self._count

    @count.setter
    def count(self, value: int) -> None:
        self._count = value

    @property
    def data(self) -> List[Dict[str, Any]]:
        return self._data

    @data.setter
    def data(self, value: List[Dict[str, Any]]) -> None:
        self._data = value

    def append(self, value: Dict[str, Any]) -> None:
        self._data.append(value)


class SSICResultFormatEnum(Enum):
    XML = 'xml'
    JSON = 'json'
    CSV = 'csv'
    DBF = 'dbf'


class SSICIndustryClassificationEnum(Enum):
    CSRC = '008001'     # 证监会行业分类标准
    SSIC = '008002'     # 巨潮行业分类标准
    SWS = '008003'      # 申银万国行业分类标准
    XCF = '008004'      # 新财富行业分类标准
    SASAC = '008005'    # 国资委行业分类标准
    SSIC_DETAIL = '008006'  # 巨潮产业细分标准
    TX = '008007'       # 天相行业分类标准
    GICS = '008008'     # 全球行业分类标准（GICS）


def get_ssic_token() -> str:
    """
    Get token from SSIC.
    :return: str.
    """
    url = 'http://webapi.cninfo.com.cn/api-cloud-platform/oauth2/token'
    post_data = {
        'grant_type': 'client_credentials',
        'client_id': CONFIGS['SSIC']['access_key'],
        'client_secret': CONFIGS['SSIC']['access_secret']
    }
    response = requests.post(url, data=post_data)
    token_dict = json.loads(response.text)
    return token_dict['access_token']


def _str2date(value: str) -> Optional[dt.date]:
    if value is None:
        return None
    else:
        return dt.date.fromisoformat(value)


def get_trading_calendar(
        date_start: Optional[dt.date] = None,
        date_end: Optional[dt.date] = None,
        state: Optional[bool] = None,
        result_format: Optional[SSICResultFormatEnum] = None
) -> ResultOfSSIC:
    """
    Get trading calendar.
    :param date_start:
    :param date_end:
    :param state:
    :param result_format:
    :return: ResultOfSSIC.
    """
    category: str = 'stock'
    interface: str = 'p_public0001'

    parameter: str = ''
    if date_start:
        parameter = parameter.join(['&sdate=', date_start.isoformat()])
    if date_end:
        parameter = parameter.join(['&edate=', date_end.isoformat()])
    if state:
        parameter = parameter.join(['&state=', '1' if state else '0'])
    if result_format:
        parameter = parameter.join(['&format=', result_format.value])
    url: str = SSIC_URL.format(
        category=category,
        interface=interface,
        token=get_ssic_token()
    )
    if len(parameter) > 0:
        url = ''.join([url, parameter])

    response = requests.get(url)
    raw: Dict[str, Any] = json.loads(response.content)

    result: ResultOfSSIC = ResultOfSSIC(total=raw['total'], count=raw['count'])
    for i in range(raw['count']):
        result.append(
            {
                'date': _str2date(raw['records'][i]['F001D']),                  # 日期
                'previous_trading_day': _str2date(raw['records'][i]['F011D']),  # 前一交易日
                'next_trading_day': _str2date(raw['records'][i]['F012D']),      # 后一交易日
                'is_week_beginning': True if raw['records'][i]['F002C'] == '1' else False,          # 是否周初
                'is_week_end': True if raw['records'][i]['F003C'] == '1' else False,                # 是否周末
                'is_month_beginning': True if raw['records'][i]['F004C'] == '1' else False,         # 是否月初
                'is_month_end': True if raw['records'][i]['F005C'] == '1' else False,               # 是否月末
                'is_trading_day': True if raw['records'][i]['F006C'] == '1' else False,             # 是否交易日
                'is_quarter_end': True if raw['records'][i]['F007C'] == '1' else False,             # 是否季末
                'is_half_year_end': True if raw['records'][i]['F008C'] == '1' else False,           # 是否半年末
                'is_year_end': True if raw['records'][i]['F009C'] == '1' else False,                # 是否年末
                'is_interbank_trading_day': True if raw['records'][i]['F010C'] == '1' else False,   # 是否银行间交易日
                'is_hkex_trading_day': True if raw['records'][i]['F013C'] == '1' else False,        # 是否港交所交易日
                'is_ah_trading_day': True if raw['records'][i]['F014C'] == '1' else False,          # 港股通交易日
                'is_ha_trading_day': True if raw['records'][i]['F015C'] == '1' else False           # 陆股通交易日
            }
        )
    return result


def get_industry(
    industry_type: SSICIndustryClassificationEnum
) -> ResultOfSSIC:
    category: str = 'stock'
    interface: str = 'p_public0002'

    url: str = SSIC_URL.format(
        category=category,
        interface=interface,
        token=get_ssic_token()
    )
    url = ''.join([url, '&indtype=', industry_type.value])

    response = requests.get(url)
    raw: Dict[str, Any] = json.loads(response.content)

    result: ResultOfSSIC = ResultOfSSIC(total=raw['total'], count=raw['count'])
    for i in range(raw['count']):
        result.append(
            {
                'parent': raw['records'][i]['PARENTCODE'],         # 父类编码
                'code': raw['records'][i]['SORTCODE'],             # 类目编码
                'name': raw['records'][i]['SORTNAME'],             # 类目名称
                'name_en': raw['records'][i]['F001V'],             # 类目名称（英文）
                'expiration_date': raw['records'][i]['F002D'],     # 终止日期
                'industry_type_code': raw['records'][i]['F003V'],  # 行业类型编码
                'industry_type': raw['records'][i]['F004V']        # 行业类型
            }
        )
    return result
