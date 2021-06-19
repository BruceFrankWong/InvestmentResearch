# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict, List
from pathlib import Path
import csv

from peewee import Model

from utility import PACKAGE_PATH
from .interface import db
from .model import (
    Country,
)


INITIAL_DATA_PATH: Path = PACKAGE_PATH.joinpath('data')


def create_model_tables():
    model_list: List[Model] = [
        Country,
    ]
    db.create_tables(model_list)


def initialize_country():
    csv_path: Path = INITIAL_DATA_PATH.joinpath('country.csv')

    model_list: List[Model] = []
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
    
    with db.atomic():
        Country.bulk_create(model_list, batch_size=100)


def initialize_all():
    initialize_country()
