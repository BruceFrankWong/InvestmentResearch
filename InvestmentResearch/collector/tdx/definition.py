# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Any, Dict
from enum import Enum


class TdxExchangeEnum(Enum):
    SSE = {
        'directory': 'sh',
        'prefix': '',
    }
    SZSE = {
        'directory': 'sz',
        'prefix': '',
    }
    CZCE = {
        'directory': 'ds',
        'prefix': '28#',
    }
    DCE = {
        'directory': 'ds',
        'prefix': '29#',
    }
    SHFE = {
        'directory': 'ds',
        'prefix': '30#',
    }
    HKEX = {
        'directory': 'ds',
        'prefix': '31#',
    }
    CFFEX = {
        'directory': 'ds',
        'prefix': '47#',
    }
    INE = {
        'directory': 'ds',
        'prefix': '30#',
    }

    def __repr__(self) -> str:
        return f'<TdxExchangeEnum>(exchange={self.exchange}, symbol={self.symbol})'


class TdxPeriodEnum(Enum):
    Minute1 = {
        'directory': 'minline',
        'suffix': 'lc1',
    }
    Minute5 = {
        'directory': 'fzline',
        'suffix': 'lc5',
    }
    Day = {
        'directory': 'lday',
        'suffix': 'day',
    }


class TdxResultTypeEnum(Enum):
    Dict = 'Dict'
    Tuple = 'Tuple'
    Dataframe = 'Dataframe'


class TdxRecordTypeEnum(Enum):
    Cash = 'Cash'       # 现金，对应通达信软件的【银证转帐】
    Order = 'Order'     # 委托，对应通达信软件的【历史委托】
    Trade = 'Trade'     # 成交，对应通达信软件的【历史成交】
    Settle = 'Settle'   # 结算，对应通达信软件的【资金流水】
