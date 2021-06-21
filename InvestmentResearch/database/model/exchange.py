# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from peewee import (
    Model,
    AutoField,
    CharField,
    ForeignKeyField,
)

from .. import db
from .country import Country


class Exchange(Model):
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
        database = db
        table_name = 'exchange'

    def __repr__(self):
        return f'<Exchange(' \
               f'symbol={self.symbol}, ' \
               f'name={self.name}, ' \
               f'fullname={self.fullname}, ' \
               f'url={self.url}, ' \
               f'country={self.country}' \
               f')>'
