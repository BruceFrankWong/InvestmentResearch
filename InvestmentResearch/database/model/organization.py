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
from .country import Country


class Organization(BasicModel):
    """
    Organization.
    """
    id = AutoField(primary_key=True)
    country = ForeignKeyField(Country, backref='organization_list', on_delete='CASCADE')
    name_zh = CharField(verbose_name='中文名称')
    name_en = CharField(verbose_name='英文名称', null=True)

    class Meta:
        depends_on = [
            Country,
        ]
