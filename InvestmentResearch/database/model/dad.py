# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from peewee import (
    AutoField,
    CharField,
    FixedCharField,
    ForeignKeyField,
)

from .base import BasicModel


class DomesticAdministrativeDivisions(BasicModel):
    """
    Domestic Administrative Divisions.
    """
    id = AutoField()
    symbol = FixedCharField(verbose_name='代码', max_length=17)
    name = FixedCharField(verbose_name='名称/简称', max_length=3)
    fullname = CharField(verbose_name='全称')

    upper = ForeignKeyField('self', null=True, backref='lower')

    def __repr__(self):
        return f'<DomesticAdministrativeDivisions(' \
               f'symbol={self.symbol}, ' \
               f'name={self.name}, ' \
               f'fullname={self.fullname}' \
               f')>'


class Province(BasicModel):
    """
    Domestic Administrative Divisions, Province.
    """
    id = AutoField()
    symbol = FixedCharField(verbose_name='代码', max_length=2)
    name = CharField(verbose_name='名称')

    abbr = FixedCharField(verbose_name='简称', max_length=3, null=True)
    abbr_single = FixedCharField(verbose_name='简称，单字', max_length=1, null=True)

    upper = ForeignKeyField('self', null=True, backref='lower')

    def __repr__(self):
        return f'<DomesticProvince(' \
               f'symbol={self.symbol}, ' \
               f'name={self.name}, ' \
               f'abbr={self.abbr}' \
               f')>'


class County(BasicModel):
    """
    Domestic Administrative Divisions, county and above.
    """
    id = AutoField()
    symbol = FixedCharField(verbose_name='代码', max_length=6)
    name = CharField(verbose_name='名称')
