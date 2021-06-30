# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict, List

from ...utility import CONFIGS
from ...database.model import FuturesProduct


def get_futures_info_from_shfe() -> List[FuturesProduct]:
    result: List[FuturesProduct] = []

    http_header: Dict[str, str] = CONFIGS['http_header']
    http_header['Referer'] = 'http://www.sse.com.cn/'

    return result
