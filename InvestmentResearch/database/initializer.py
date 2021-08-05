# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import List, Type
from pathlib import Path
import csv

from peewee import Model

from InvestmentResearch.utility import PACKAGE_PATH, CONFIGS
from .interface import db
from .model import (
    Country,
    Holiday,
    Exchange,
    ExchangeNotice,
    StockStatus,
    StockStatusEnum,
    Announcement,
    Stock,
)


INITIAL_DATA_PATH: Path = PACKAGE_PATH.joinpath('data')


def initialize_country() -> None:
    """
    Initialize the Country model.
    :return: None.
    """
    Country.create_table()

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

    with db.atomic():
        Country.bulk_create(model_list, batch_size=100)


def initialize_holiday() -> None:
    """
    Initialize the Holiday model.
    :return: None.
    """
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


def initialize_exchange() -> None:
    """
    Initialize the Exchange model.
    :return: None.
    """
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


def initialize_exchange_notice() -> None:
    """
    Initialize the ExchangeNotice model.
    :return:
    """
    ExchangeNotice.create_table()


def initialize_stock_status() -> None:
    """
    Initialize the StockStatus model.
    :return: None.
    """
    model_list: List[StockStatus] = [StockStatus(status=status.value) for status in StockStatusEnum]

    StockStatus.create_table()
    with db.atomic():
        StockStatus.bulk_create(model_list, batch_size=100)


def initialize_all(drop: bool = False) -> None:
    """
    Initialize all the models.
    :return: None.
    """
    if CONFIGS['DEBUG'] is not True:
        model_list: List[Type[Model]] = [
            Country,            # 国家
            Holiday,            # 假日
            Exchange,           # 交易所
            ExchangeNotice,     # 交易所公告
            Stock,
            StockStatus,        # 股票状态
            Announcement,       # 披露
        ]
        if drop is True:
            print('Dropping tables:')
            for i in range(len(model_list), 0, -1):
                print(f'\t{model_list[i-1]} ...')
                model_list[i-1].drop_table()

        print('Creating tables:')
        for model in model_list:
            model.create_table()
            print(f'\t{model} ...')

        print('Initializing tables:')
        print('\t<Model: Country> ...')
        initialize_country()

        print('\t<Model: Holiday> ...')
        initialize_holiday()

        print('\t<Model: Exchange> ...')
        initialize_exchange()

        print('\t<Model: ExchangeNotice> ...')
        initialize_exchange_notice()

        print('\t<Model: StockStatus> ...')
        initialize_stock_status()
