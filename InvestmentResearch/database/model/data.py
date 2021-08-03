# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from peewee import (
    AutoField,
    CharField,
    FixedCharField,
    IntegerField,
    ForeignKeyField,
)

from .base import BasicModel


class PlantingArea(BasicModel):
    id = AutoField()
    year = IntegerField(verbose_name='年份')
    product = IntegerField(verbose_name='种类')
    area = IntegerField(verbose_name='面积')
