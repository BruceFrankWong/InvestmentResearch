# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from peewee import Model

from .. import db


class BasicModel(Model):
    class Meta:
        database = db
        legacy_table_names = False
