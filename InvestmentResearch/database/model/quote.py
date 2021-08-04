# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from enum import Enum

from peewee import (
    AutoField,
    FixedCharField,
    DateField,
    DateTimeField,
    IntegerField,
    FloatField,
    ForeignKeyField,
)

from .base import BasicModel
from .stock import Stock
from .futures import FuturesProduct, FuturesContract


class QuotePeriod(Enum):
    Tick = 'Tick'
    Minute1 = 'Minute1'
    Minute3 = 'Minute3'
    Minute5 = 'Minute5'
    Minute15 = 'Minute15'
    Minute30 = 'Minute30'
    Minute30N = 'Minute30N'
    Hour1 = 'Hour1'
    Hour1N = 'Hour1N'
    Day = 'Day'
    Week = 'Week'


class StockQuoteDaily(BasicModel):
    """
    Quote of stocks, daily.
    """
    id = AutoField(primary_key=True)
    date = DateField(verbose_name='日期')

    symbol = ForeignKeyField(Stock, verbose_name='代码id', backref='quote_daily_list')

    open = FloatField(verbose_name='开盘价')
    high = FloatField(verbose_name='最高价')
    low = FloatField(verbose_name='最低价')
    close = FloatField(verbose_name='收盘价')
    volume = IntegerField(verbose_name='成交量')
    amount = FloatField(verbose_name='成交额')

    class Meta:
        depends_on = [
            Stock,
        ]


class StockQuoteTick(BasicModel):
    """
    Quote of stocks, tick.
    """
    id = AutoField(primary_key=True)
    datetime = DateTimeField(verbose_name='日期时间')

    symbol = ForeignKeyField(Stock, verbose_name='代码id', backref='quote_daily_list')

    open = FloatField(verbose_name='开盘价')
    high = FloatField(verbose_name='最高价')
    low = FloatField(verbose_name='最低价')
    close = FloatField(verbose_name='收盘价')
    volume = IntegerField(verbose_name='成交量')
    amount = FloatField(verbose_name='成交额')

    class Meta:
        depends_on = [
            Stock,
        ]


class StockQuoteMinutely(BasicModel):
    """
    Quote of stocks, minutely.
    """
    id = AutoField(primary_key=True)
    datetime = DateTimeField(verbose_name='日期时间')
    period = FixedCharField(verbose_name='周期', max_length=9)

    symbol = ForeignKeyField(Stock, verbose_name='代码id', backref='quote_daily_list')

    open = FloatField(verbose_name='开盘价')
    high = FloatField(verbose_name='最高价')
    low = FloatField(verbose_name='最低价')
    close = FloatField(verbose_name='收盘价')
    volume = IntegerField(verbose_name='成交量')
    amount = FloatField(verbose_name='成交额')

    class Meta:
        depends_on = [
            Stock,
        ]


class FuturesQuoteDaily(BasicModel):
    """
    Quote of futures.
    """
    id = AutoField(primary_key=True)
    date = DateField(verbose_name='日期')

    product = ForeignKeyField(FuturesProduct, verbose_name='品种id', backref='quote_list')
    contract = ForeignKeyField(FuturesContract, verbose_name='合约id', backref='quote_list')

    open = FloatField(verbose_name='开盘价')
    high = FloatField(verbose_name='最高价')
    low = FloatField(verbose_name='最低价')
    close = FloatField(verbose_name='收盘价')
    volume = IntegerField(verbose_name='成交量')
    amount = FloatField(verbose_name='成交额')
    settlement = FloatField(verbose_name='结算价')
    open_interest = IntegerField(verbose_name='持仓量')

    class Meta:
        depends_on = [
            FuturesProduct,
            FuturesContract,
        ]


class FuturesQuoteTick(BasicModel):
    """
    Quotation of futures, tick.
    """
    id = AutoField(primary_key=True)
    datetime = DateTimeField(verbose_name='日期时间')

    product = ForeignKeyField(FuturesProduct, verbose_name='品种id', backref='quote_list')
    contract = ForeignKeyField(FuturesContract, verbose_name='合约id', backref='quote_list')

    open = FloatField(verbose_name='开盘价')
    high = FloatField(verbose_name='最高价')
    low = FloatField(verbose_name='最低价')
    close = FloatField(verbose_name='收盘价')
    volume = IntegerField(verbose_name='成交量')
    amount = FloatField(verbose_name='成交额')
    settlement = FloatField(verbose_name='结算价')
    open_interest = IntegerField(verbose_name='持仓量')

    class Meta:
        depends_on = [
            FuturesProduct,
            FuturesContract,
        ]


class FuturesQuotationMinutely(BasicModel):
    """
    Quotation of futures, 1 minute.
    """
    id = AutoField(primary_key=True)
    datetime = DateTimeField(verbose_name='日期时间')
    period = FixedCharField(verbose_name='周期', max_length=9)

    product = ForeignKeyField(FuturesProduct, verbose_name='品种id', backref='quote_list')
    contract = ForeignKeyField(FuturesContract, verbose_name='合约id', backref='quote_list')

    open = FloatField(verbose_name='开盘价')
    high = FloatField(verbose_name='最高价')
    low = FloatField(verbose_name='最低价')
    close = FloatField(verbose_name='收盘价')
    volume = IntegerField(verbose_name='成交量')
    amount = FloatField(verbose_name='成交额')
    settlement = FloatField(verbose_name='结算价')
    open_interest = IntegerField(verbose_name='持仓量')

    class Meta:
        depends_on = [
            FuturesProduct,
            FuturesContract,
        ]
