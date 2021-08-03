# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


import datetime as dt

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


class FuturesProduct(BasicModel):
    """
    Futures product.
    """
    id = AutoField(primary_key=True)
    exchange = ForeignKeyField(Exchange, backref='futures_list', on_delete='CASCADE')
    symbol = FixedCharField(verbose_name='品种代码', max_length=2, unique=True)
    name_zh = CharField(verbose_name='品种中文名称')
    name_en = CharField(verbose_name='品种英文名称', null=True)
    listing_date = DateField(verbose_name='上市日期', null=True)
    initial_contract = CharField(verbose_name='首批上市合约', null=True)
    announced_date = DateField(verbose_name='公告日期', null=True)
    announcement_url = CharField(verbose_name='公告URL', null=True)

    class Meta:
        depends_on = [
            Exchange,
        ]

    def __repr__(self):
        return f'<FuturesProduct(' \
               f'symbol={self.symbol}, ' \
               f'name_zh={self.name_zh}, ' \
               f'name_en={self.name_en}, ' \
               f'exchange={self.exchange}, ' \
               f'alpha2={self.alpha2}, ' \
               f'alpha3={self.alpha3}, ' \
               f'numeric={self.numeric}' \
               f')>'

    def __str__(self):
        return f'<FuturesProduct(exchange={self.exchange.symbol}, symbol={self.symbol})>'


class FuturesContractSpecification(BasicModel):
    """
    Futures contract specification.
    """
    id = AutoField(primary_key=True)
    product = ForeignKeyField(FuturesProduct, backref='contract_list', on_delete='CASCADE')
    symbol = FixedCharField(verbose_name='代码', max_length=4)
    enable_date = DateField(verbose_name='上市日期')
    multiplier = IntegerField(verbose_name='乘数')
    delivery_date_begin = DateField(verbose_name='交割开始日期')
    delivery_date_end = DateField(verbose_name='交割结束日期')

    class Meta:
        depends_on = [
            FuturesProduct,
        ]


class FuturesContract(BasicModel):
    """
    Futures contract.
    """
    id = AutoField(primary_key=True)
    product = ForeignKeyField(FuturesProduct, backref='contract_list', on_delete='CASCADE')
    delivery_month = FixedCharField(verbose_name='代码', max_length=4)
    listing_date = DateField(verbose_name='上市日期', formats='YYYY-mm-dd', null=True)
    expiration_date = DateField(verbose_name='交割日期', formats='YYYY-mm-dd', null=True)
    delivery_date_begin = DateField(verbose_name='交割开始日期', formats='YYYY-mm-dd', null=True)
    delivery_date_end = DateField(verbose_name='交割结束日期', formats='YYYY-mm-dd', null=True)

    class Meta:
        depends_on = [
            FuturesProduct,
        ]

    def __str__(self):
        x = self.expiration_date
        # expiration_date: dt.date = dt.date.fromisoformat(self.expiration_date.year, )
        return f'<FuturesContract(' \
               f'product={self.product.symbol}, ' \
               f'delivery={self.delivery_month}' \
               f')>'


class FuturesTransactionRule(BasicModel):
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
        depends_on = [
            FuturesProduct,
            FuturesContract,
        ]


class FuturesQuotationBase(BasicModel):
    """
    Quotation of futures.
    """
    id = AutoField(primary_key=True)
    product = ForeignKeyField(FuturesProduct, verbose_name='品种id', backref='transaction_list')
    contract = ForeignKeyField(FuturesContract, verbose_name='合约id', backref='transaction_list')
    open = FloatField(verbose_name='开盘价')
    high = FloatField(verbose_name='最高价')
    low = FloatField(verbose_name='最低价')
    close = FloatField(verbose_name='收盘价')
    settlement = FloatField(verbose_name='结算价')
    volume = IntegerField(verbose_name='成交量')
    open_interest = IntegerField(verbose_name='持仓量')

    class Meta:
        depends_on = [
            FuturesProduct,
            FuturesContract,
        ]


class FuturesQuotation1Minutely(FuturesQuotationBase):
    """
    Quotation of futures, 1 minutely.
    """
    date = DateField(verbose_name='日期')
    time = TimeField(verbose_name='时间')


class FuturesQuotation3Minutely(FuturesQuotationBase):
    """
    Quotation of futures, 3 minutely.
    """
    date = DateField(verbose_name='日期')
    time = TimeField(verbose_name='时间')


class FuturesQuotationDaily(FuturesQuotationBase):
    """
    Quotation of futures, daily.
    """
    date = DateField(verbose_name='日期')


class CommoditySupplyDemandBalance(BasicModel):
    """
    Supply-Demand Balance for commodity.
    """
    id = AutoField(primary_key=True)
    product = CharField(verbose_name='品种')
    is_estimate = BooleanField(verbose_name='是否预估')
    unit = CharField(verbose_name='单位')
    inventory = FloatField(verbose_name='期初库存')
    production = FloatField(verbose_name='产量')
    imports = FloatField(verbose_name='进口量')
    total_supply = FloatField(verbose_name='总供给')
    consumption = FloatField(verbose_name='消费量')
    exports = FloatField(verbose_name='出口量')
    total_demand = FloatField(verbose_name='总需求')
    gap = FloatField(verbose_name='供需缺口')

    def __repr__(self):
        return f'<CommoditySupplyDemandBalance(' \
               f'product={self.product}, ' \
               f'is_estimate={self.is_estimate}, ' \
               f'unit={self.unit}, ' \
               f'inventory={self.inventory}, '\
               f'production={self.production}, ' \
               f'imports={self.imports}, ' \
               f'total_supply={self.total_supply}, ' \
               f'consumption={self.consumption}, ' \
               f'exports={self.exports}, ' \
               f'total_demand={self.total_demand}, ' \
               f'gap={self.gap}' \
               f')>'


class CommodityImportsAndExportsMonthly(BasicModel):
    """
    Commodity import and exports data monthly, from the General Administration of Customs P.R.China.
    """
    id = AutoField(primary_key=True)
    product = CharField(verbose_name='品种')
    year = IntegerField(verbose_name='年份')
    month = IntegerField(verbose_name='月份')
    imports = IntegerField(verbose_name='进口量')
    exports = IntegerField(verbose_name='出口量')

    def __repr__(self):
        return f'<CommoditySupplyDemandBalance(' \
               f'product={self.product}, ' \
               f'year={self.is_estimate}, ' \
               f'month={self.unit}, ' \
               f'imports={self.inventory}, '\
               f'exports={self.production}, ' \
               f')>'
