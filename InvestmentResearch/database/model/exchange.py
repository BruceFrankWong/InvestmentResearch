# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from peewee import (
    AutoField,
    CharField,
    DateField,
    ForeignKeyField,
)

from .base import BasicModel
from .country import Country


class Exchange(BasicModel):
    """
    Exchange.
    """
    id = AutoField()
    symbol = CharField(verbose_name='交易所代码', unique=True)
    name = CharField(verbose_name='交易所名称')
    fullname = CharField(verbose_name='交易所全称')
    url = CharField(verbose_name='交易所网站', null=True)
    country = ForeignKeyField(Country, backref='exchange_list')

    class Meta:
        depends_on = [
            Country,
        ]

    def __repr__(self):
        return f'<Exchange(' \
               f'symbol={self.symbol}, ' \
               f'name={self.name}, ' \
               f'fullname={self.fullname}, ' \
               f'url={self.url}, ' \
               f'country={self.country}' \
               f')>'


class ExchangeNotice(BasicModel):
    """
    Notice from exchange.
    """
    id = AutoField()
    exchange = ForeignKeyField(Exchange, backref='notice_list')
    title = CharField(verbose_name='公告标题')
    code = CharField(verbose_name='公告文号')
    date = DateField(verbose_name='公告时间')
    content = CharField(verbose_name='公告内容')
    url = CharField(verbose_name='公告URL')

    class Meta:
        depends_on = [
            Exchange,
        ]

    def __repr__(self):
        return f'<Notice(' \
               f'exchange={self.exchange.symbol}, ' \
               f'title={self.title}, ' \
               f'code={self.code}, ' \
               f'date={self.date}, ' \
               f'content={self.content}, ' \
               f'url={self.url}' \
               f')>'
