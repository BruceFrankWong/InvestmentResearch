# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


import pytest

from pathlib import Path


@pytest.mark.run(order=5)
def test_database_interface():
    """
    Test for SQLite.
    """
    from src.utility import PACKAGE_PATH, CONFIGS

    sqlite_path: Path = PACKAGE_PATH.joinpath(CONFIGS['database']['database'])
    if sqlite_path.exists():
        sqlite_path.unlink()
    
    assert sqlite_path.exists() is False

    from src.database import db
    db.connect()
    db.execute_sql('CREATE TABLE test(name varchar);')
    db.commit()
    db.close()

    assert sqlite_path.exists() is True

    sqlite_path.unlink()
    assert sqlite_path.exists() is False
