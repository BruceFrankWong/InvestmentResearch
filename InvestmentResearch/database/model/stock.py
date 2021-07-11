# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from enum import Enum

from peewee import (
    AutoField,
    CharField,
    FixedCharField,
    DateField,
    TimeField,
    BooleanField,
    IntegerField,
    FloatField,
    ForeignKeyField,
)

from .base import BasicModel
from .exchange import Exchange


class StockStatusEnum(Enum):
    IPO = 'IPO'                 # 初始募集
    Listing = 'Listing'         # 挂牌交易
    Suspended = 'Suspended'     # 停牌
    Resumed = 'Resumed'         # 回复交易
    Terminated = 'Terminated'   # 终止上市


class StockStatus(BasicModel):
    """
    Status of stocks.
    股票状态。
    """
    id = AutoField(primary_key=True)
    status = FixedCharField(verbose_name='股票状态', max_length=6, unique=True)

    def __repr__(self):
        return f'<StockStatus(status={self.status})>'


class Stock(BasicModel):
    """
    Stock.
    """
    id = AutoField(primary_key=True)
    exchange = ForeignKeyField(Exchange, backref='stock_list', on_delete='CASCADE')
    symbol = FixedCharField(verbose_name='股票代码', max_length=6, unique=True)
    name = FixedCharField(verbose_name='股票中文简称', max_length=4)
    market = FixedCharField(verbose_name='市场', max_length=3)
    pinyin = FixedCharField(verbose_name='股票拼音', max_length=4, null=True)
    listing_date = DateField(verbose_name='上市日期', null=True)
    terminated_date = DateField(verbose_name='终止上市日期', null=True)
    announced_date = DateField(verbose_name='公告日期', null=True)
    announcement_url = CharField(verbose_name='公告URL', null=True)

    class Meta:
        depends_on = [
            Exchange,
        ]

    def __repr__(self):
        return f'<Stock(' \
               f'symbol={self.symbol}, ' \
               f'name={self.name}, ' \
               f'exchange={self.exchange.name}, ' \
               f')>'
