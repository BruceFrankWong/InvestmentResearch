# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


import pytest

from pathlib import Path


PROJECT_NAME: str = 'InvestmentResearch'


# @pytest.mark.run(order=1)
# def test_config_path():
#     config_path: Path = Path.home().joinpath(f'.{PROJECT_NAME}')
#     if config_path.exists():
#         for item in config_path.iterdir():
#             item.unlink()
#         config_path.rmdir()
#     assert config_path.exists() is False
#
#     from InvestmentResearch.utility import CONFIG_PATH
#     assert config_path.exists() is True


@pytest.mark.run(order=2)
def test_package_name():
    from InvestmentResearch.utility import PACKAGE_NAME
    assert PACKAGE_NAME == PROJECT_NAME


@pytest.mark.run(order=3)
def test_package_path():
    from InvestmentResearch import utility
    from InvestmentResearch.utility import PACKAGE_PATH
    assert PACKAGE_PATH == Path(utility.__file__).parent


@pytest.mark.run(order=4)
def test_configs():
    from InvestmentResearch.utility import CONFIGS

    assert isinstance(CONFIGS, dict) is True
