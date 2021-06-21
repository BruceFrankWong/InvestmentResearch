# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import List, Type
from pathlib import Path
import csv

from peewee import Model

from InvestmentResearch.utility import PACKAGE_PATH
from .interface import db
from .model import (
    Country,
    Holiday,
    Exchange,
)


INITIAL_DATA_PATH: Path = PACKAGE_PATH.joinpath('data')


def create_model_tables():
    model_list: List[Type[Model]] = [
        Country,
        Holiday,
        Exchange,
    ]
    db.create_tables(model_list)


def initialize_country():
    csv_path: Path = INITIAL_DATA_PATH.joinpath('country.csv')

    with open(csv_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        model_list = [
            Country(
                name_zh=row['name_zh'],
                name_en=row['name_en'],
                fullname_zh=row['fullname_zh'],
                fullname_en=row['fullname_en'],
                alpha2=row['alpha2'],
                alpha3=row['alpha3'],
                numeric=row['numeric']
            ) for row in reader
        ]
    
    Country.create_table()
    with db.atomic():
        Country.bulk_create(model_list, batch_size=100)


def initialize_holiday():
    csv_path: Path = INITIAL_DATA_PATH.joinpath('holiday.csv')

    with open(csv_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        model_list = [
            Holiday(
                begin=row['begin'],
                end=row['end'],
                name=row['name'],
                url=row['url'],
                country=Country.get(Country.alpha3 == row['country'])
            ) for row in reader
        ]
    
    Holiday.create_table()
    with db.atomic():
        Holiday.bulk_create(model_list, batch_size=100)


def initialize_exchange():
    csv_path: Path = INITIAL_DATA_PATH.joinpath('exchange.csv')

    with open(csv_path, mode='r', newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        model_list = [
            Exchange(
                symbol=row['symbol'],
                name=row['name'],
                fullname=row['fullname'],
                url=row['url'],
                country=Country.get(Country.alpha3 == row['country'])
            ) for row in reader
        ]
    
    Exchange.create_table()
    with db.atomic():
        Exchange.bulk_create(model_list, batch_size=100)


def initialize_all():
    create_model_tables()
    initialize_country()
    initialize_holiday()
    initialize_exchange()
