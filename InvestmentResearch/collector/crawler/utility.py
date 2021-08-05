# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict, List, Tuple

import requests

from InvestmentResearch.database.model.crawler import PageVisitedRecord


class Crawler:
    """
    the crawler object.
    """
    def __init__(self, name: str, header: Dict[str, str]):
        self._name = name
        self._header = header
        self._session = requests.Session()

    def crawl(self, url: str) -> str:
        response = self._session.get(url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text


def normalize_stock_name(name: str) -> str:
    char_mapper_list: List[Tuple[str, str]] = [
        # 去空格
        (' ', ''),
        # 全角转半角
        ('Ａ', 'A'),
        ('Ｂ', 'B'),
        # web 空格
        ('&nbsp;', ''),
    ]
    result: str = name
    for char_mapper in char_mapper_list:
        result = result.replace(char_mapper[0], char_mapper[1])
    return result
