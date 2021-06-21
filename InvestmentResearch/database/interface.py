# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Callable, Dict

from peewee import (
    Database,
    SqliteDatabase,
    MySQLDatabase,
    PostgresqlDatabase
)

from utility import CONFIGS, PACKAGE_PATH


def create_sqlite_database(settings: Dict[str, str]) -> SqliteDatabase:
    return SqliteDatabase(
        PACKAGE_PATH.joinpath(settings['database']),
        pragmas={
            'journal_mode': 'wal',
            'encoding': 'utf8',
            'cache_size': -640000,  # 64MB
            'foreign_keys': 1,  # Enforce foreign-key constraints
        }
    )


def create_mysql_database(settings: Dict[str, str]) -> MySQLDatabase:
    return MySQLDatabase(
        settings['database'],
        user=settings['user'],
        password=settings['password'],
        host=settings['host'],
        port=settings['port']
    )


def create_postgresql_database(settings: Dict[str, str]) -> PostgresqlDatabase:
    return PostgresqlDatabase(
        settings['database'],
        user=settings['user'],
        password=settings['password'],
        host=settings['host'],
        port=settings['port']
    )


def create_database() -> Database:
    driver_mapper: Dict[str, Callable] = {
        'SQLITE': create_sqlite_database,
        'MYSQL': create_mysql_database,
        'POSTGRESQL': create_postgresql_database,
    }

    driver: str = CONFIGS['database']['driver'].upper()

    assert driver in driver_mapper.keys()

    return driver_mapper[driver](CONFIGS['database'])


db: Database = create_database()
