# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from peewee import (
    Model,
    AutoField,
    CharField,
    FixedCharField,
    DateField,
    BooleanField,
    IntegerField,
    ForeignKeyField,
)

from .. import db
from .exchange import Exchange


class FuturesProduct(Model):
    """
    Futures product.
    """
    id = AutoField(primary_key=True)
    symbol = FixedCharField(verbose_name='品种代码', max_length=2, unique=True)
    name_zh = CharField(verbose_name='品种中文名称')
    name_en = CharField(verbose_name='品种英文名称')
    # section = IntegerField(verbose_name='交易节数量')
    # optional_section = IntegerField(verbose_name='可选交易节序号')
    exchange = ForeignKeyField(Exchange, backref='futures_list', on_delete='CASCADE')

    class Meta:
        database = db
        table_name = 'futures_product'

    def __repr__(self):
        return f'<Futures(' \
               f'symbol={self.symbol}, ' \
               f'name_zh={self.name_zh}, ' \
               f'name_en={self.name_en}, ' \
               f'exchange={self.exchange}, ' \
               f'alpha2={self.alpha2}, ' \
               f'alpha3={self.alpha3}, ' \
               f'numeric={self.numeric}' \
               f')>'


class FuturesContract(Model):
    """
    Futures contract.
    """
    id = AutoField(primary_key=True)
    product = ForeignKeyField(FuturesProduct, backref='contract_list', on_delete='CASCADE')
    symbol = FixedCharField(verbose_name='代码', max_length=4)
    listing_date = DateField(verbose_name='上市日期')
    expiration_date = DateField(verbose_name='上市日期')
    delivery_date_begin = DateField(verbose_name='交割开始日期')
    delivery_date_end = DateField(verbose_name='交割结束日期')

    class Meta:
        database = db
        table_name = 'futures_contract'


class FuturesTransactionRule(Model):
    """
    交易细节。
    """
    id = AutoField(primary_key=True)
    date = DateField(verbose_name='日期')
    product = ForeignKeyField(FuturesProduct, verbose_name='品种id', backref='transaction_list')
    contract = ForeignKeyField(FuturesContract, verbose_name='合约id', backref='transaction_list')
    margin_speculation_long = IntegerField(verbose_name='投机多单保证金率')      # margin = 1 means margin = 1%
    margin_speculation_short = IntegerField(verbose_name='投机空单保证金率')      # margin = 1 means margin = 1%
    margin_hedging_long = IntegerField(verbose_name='套保多单保证金率')      # margin = 1 means margin = 1%
    margin_hedging_short = IntegerField(verbose_name='套保空单保证金率')      # margin = 1 means margin = 1%
    limit_up = IntegerField(verbose_name='涨停板')      # margin = 1 means margin = 1%
    limit_down = IntegerField(verbose_name='涨停板')      # margin = 1 means margin = 1%
    is_fixed_transaction_fee = BooleanField(verbose_name='是否固定手续费')
    transaction_fee = IntegerField(verbose_name='手续费')

    class Meta:
        database = db
        table_name = 'futures_transaction_rule'
