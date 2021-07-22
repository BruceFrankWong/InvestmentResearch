# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from enum import Enum


class TdxExchangeEnum(Enum):
    """
    Exchange in TDX.
    """
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
        return f'<TdxExchangeEnum(' \
               f'directory={self.value["directory"]}, ' \
               f'prefix={self.value["prefix"]}' \
               f')>'


class TdxPeriodEnum(Enum):
    """
    Period in TDX.
    """
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

    def __repr__(self) -> str:
        return f'<TdxPeriodEnum(' \
               f'directory={self.value["directory"]}, ' \
               f'suffix={self.value["suffix"]}' \
               f')>'


class TdxQuoteTypeEnum(Enum):
    """
    The return type for read_quote.
    """
    Dict = 'Dict'
    Tuple = 'Tuple'
    Dataframe = 'Dataframe'

    def __repr__(self) -> str:
        return f'<TdxQuoteTypeEnum(value={self.value})>'


class TdxRecordTypeEnum(Enum):
    """
    The type of record file.
    """
    Cash = 'Cash'       # 现金，对应通达信软件的【银证转帐】
    Order = 'Order'     # 委托，对应通达信软件的【历史委托】
    Trade = 'Trade'     # 成交，对应通达信软件的【历史成交】
    Settle = 'Settle'   # 结算，对应通达信软件的【资金流水】

    def __repr__(self) -> str:
        return f'<TdxRecordTypeEnum(value={self.value})>'
