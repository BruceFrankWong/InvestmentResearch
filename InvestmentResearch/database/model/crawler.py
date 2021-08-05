# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from peewee import (
    AutoField,
    CharField,
    DateTimeField,
)

from .base import BasicModel


class PageVisitedRecord(BasicModel):
    id = AutoField()
    url = CharField(verbose_name='URL')
    name = CharField(verbose_name='名称', null=True)
    last_modified = CharField(verbose_name='更改', null=True)
    last_visited = DateTimeField(verbose_name='最后访问')

    def __repr__(self):
        return f'<PageVisited(' \
               f'url={self.url}, ' \
               f'name={self.name}, ' \
               f'last_modified={self.last_modified}' \
               f'last_visited={self.last_visited}' \
               f')>'
