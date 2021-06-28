# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


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


class StockStatus(BasicModel):
    """
    Status of stocks.
    上市
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
    name = CharField(verbose_name='品种中文名称')
    listing_date = DateField(verbose_name='上市日期', null=True)
    initial_contract = CharField(verbose_name='首批上市合约', null=True)
    terminated_dat = DateField(verbose_name='终止上市日期', null=True)
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
               f'exchange={self.exchange}, ' \
               f')>'
