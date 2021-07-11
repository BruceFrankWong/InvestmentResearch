# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import List, Tuple


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
