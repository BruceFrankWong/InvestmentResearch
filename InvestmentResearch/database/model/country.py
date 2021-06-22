# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from peewee import (
    AutoField,
    CharField,
    FixedCharField,
)

from .base import BasicModel


class Country(BasicModel):
    """
    Country.
    """
    id = AutoField()
    name_zh = CharField(verbose_name='中文名称')
    name_en = CharField(verbose_name='英文名称')
    fullname_zh = CharField(verbose_name='中文全名', null=True)
    fullname_en = CharField(verbose_name='英文全名', null=True)
    alpha2 = FixedCharField(verbose_name='代码，2字母', max_length=2, unique=True)
    alpha3 = FixedCharField(verbose_name='代码，3字母', max_length=3, unique=True)
    numeric = FixedCharField(verbose_name='代码，3数字', max_length=3, unique=True)

    def __repr__(self):
        return f'<Country(' \
               f'name_zh={self.name_zh}, ' \
               f'name_en={self.name_en}, ' \
               f'fullname_zh={self.fullname_zh}, ' \
               f'fullname_en={self.fullname_en}, ' \
               f'alpha2={self.alpha2}, ' \
               f'alpha3={self.alpha3}, ' \
               f'numeric={self.numeric}' \
               f')>'
