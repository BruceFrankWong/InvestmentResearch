# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from peewee import (
    AutoField,
    CharField,
    FixedCharField,
    DateField,
    ForeignKeyField,
)

from .base import BasicModel
from .country import Country


class Holiday(BasicModel):
    """
    Holiday.
    """
    id = AutoField()
    begin = DateField(verbose_name='开始日期')
    end = DateField(verbose_name='结束日期')
    name = FixedCharField(verbose_name='节假日名称', max_length=3)
    url = CharField(verbose_name='发文URL', null=True)
    country = ForeignKeyField(Country, backref='holiday_list')

    class Meta:
        depends_on = [
            Country,
        ]

    def __repr__(self):
        return f'<Holiday(' \
               f'name={self.name}, ' \
               f'begin={self.begin}, ' \
               f'end={self.end}, ' \
               f'url={self.url}, ' \
               f'country={self.country}' \
               f')>'
