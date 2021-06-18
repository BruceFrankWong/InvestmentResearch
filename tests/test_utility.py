# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


import pytest

from pathlib import Path


PROJECT_NAME: str = 'InvestmentResearch'


def test_config_path():
    config_path: Path = Path.home().joinpath(f'.{PROJECT_NAME}')
    if config_path.exists():
        for item in config_path.iterdir():
            item.unlink()
        config_path.rmdir()
    assert config_path.exists() is False

    import src.utility
    assert config_path.exists() is True


def test_package_name():
    from src.utility import PACKAGE_NAME
    assert PACKAGE_NAME == PROJECT_NAME


def test_package_path():
    from src.utility import PACKAGE_PATH
    assert PACKAGE_PATH == Path(r'D:\Development\Jupyter\InvestmentResearch\src')


def test_configs():
    from src.utility import CONFIGS

    assert isinstance(CONFIGS, dict) is True
