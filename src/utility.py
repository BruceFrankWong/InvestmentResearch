# -*- coding: utf-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict, Any
from pathlib import Path
import json


__all__ = ['PACKAGE_NAME', 'PACKAGE_PATH', 'CONFIG_PATH', 'CONFIGS']


# The package name.
PACKAGE_NAME: str = 'InvestmentResearch'


# The package path <InvestmentWorkshop>
PACKAGE_PATH: Path = Path(__file__).parent


# Tha path of the user custom config file.
CONFIG_PATH: Path = Path.home().joinpath(f'.{PACKAGE_NAME}')
if not CONFIG_PATH.exists():
    CONFIG_PATH.mkdir()


# The default config.
CONFIGS: Dict[str, Any] = {
    # 数据库
    'database': {
        'driver': 'sqlite',
        'host': '',
        'port': '',
        'database': f'{PACKAGE_NAME}.sqlite',
        'user': '',
        'password': '',
    },

    # 路径
    'path': {
        'data_downloaded': 'data_downloaded',
        'picture_path': 'picture',
    },

    # 外部软件
    'tdx': r'C:\\new_tdx',
}


def load_json(json_file: Path) -> dict:
    with open(json_file, mode='r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def save_json(data: dict, json_file: Path) -> None:
    with open(json_file, mode='w+', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# Updating <CONFIGS> from user custom config file..
config_file: Path = CONFIG_PATH.joinpath('config.json')
if config_file.exists():
    CONFIGS.update(load_json(config_file))
