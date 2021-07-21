# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Any, Dict, List, Callable, Generator
from pathlib import Path
import datetime as dt
import struct

import pandas as pd

from ...utility import CONFIGS
from .definition import TdxExchangeEnum, TdxPeriodEnum, TdxResultTypeEnum


def _read_quote(exchange: TdxExchangeEnum, symbol: str, period: TdxPeriodEnum) -> bytes:
    tdx_path: Path = Path(CONFIGS['tdx'])
    quote_file: Path = tdx_path.joinpath(
        'vipdoc',
        exchange.value['directory'],
        period.value['directory'],
        f'{exchange.value["prefix"]}{exchange.value["directory"]}{symbol}.{period.value["suffix"]}'
    )

    with open(quote_file, 'rb') as f:
        raw = f.read()

    return raw


def _tuple_formatter_for_daily(raw: tuple) -> tuple:
    return (
        dt.datetime.strptime(str(raw[0]), "%Y%m%d").date(),
        float(format(raw[1] * 0.01, '.2f')),
        float(format(raw[2] * 0.01, '.2f')),
        float(format(raw[3] * 0.01, '.2f')),
        float(format(raw[4] * 0.01, '.2f')),
        raw[5],
        raw[6]
    )


def _tuple_formatter_for_minutely(raw: tuple) -> tuple:
    return (
        dt.date(year=(raw[0] // 2048) + 2004,
                month=(raw[0] % 2048) // 100,
                day=(raw[0] % 2048) % 100),
        dt.time(hour=(raw[1] // 60), minute=(raw[1] % 60)),
        # Decimal(item[3]).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        float(raw[2]),
        float(raw[3]),
        float(raw[4]),
        float(raw[5]),
        float(raw[6]),
        int(raw[7])
    )


def _dict_formatter_for_daily(raw: tuple) -> Dict[str, Any]:
    return {
        'date': dt.datetime.strptime(str(raw[0]), "%Y%m%d").date(),
        'open': float(format(raw[1] * 0.01, '.2f')),
        'high': float(format(raw[2] * 0.01, '.2f')),
        'low': float(format(raw[3] * 0.01, '.2f')),
        'close': float(format(raw[4] * 0.01, '.2f')),
        'amount': raw[5],
        'volume': raw[6]
    }


def _dict_formatter_for_minutely(raw: tuple) -> Dict[str, Any]:
    return {
        'date': dt.date(year=(raw[0] // 2048) + 2004,
                        month=(raw[0] % 2048) // 100,
                        day=(raw[0] % 2048) % 100),
        'time': dt.time(hour=(raw[1] // 60), minute=(raw[1] % 60)),
        'open': float(format(raw[1] * 0.01, '.2f')),
        'high': float(format(raw[2] * 0.01, '.2f')),
        'low': float(format(raw[3] * 0.01, '.2f')),
        'close': float(format(raw[4] * 0.01, '.2f')),
        'amount': raw[5],
        'volume': raw[6]
    }


def read_quote(
        exchange: TdxExchangeEnum,
        symbol: str,
        period: TdxPeriodEnum,
        result_type: TdxResultTypeEnum
) -> Generator:

    formatter: Callable
    if result_type == TdxResultTypeEnum.Dataframe:
        columns: List[str] = ['date', 'open', 'high', 'low', 'close', 'amount', 'volume'] \
            if period == TdxPeriodEnum.Day else \
            ['date', 'time', 'open', 'high', 'low', 'close', 'amount', 'volume']
        return pd.DataFrame(
            read_quote(exchange, symbol, period, TdxResultTypeEnum.Tuple),
            columns=columns
        )
    elif result_type == TdxResultTypeEnum.Tuple:
        if period == TdxPeriodEnum.Day:
            formatter = _tuple_formatter_for_daily
        else:
            formatter = _tuple_formatter_for_minutely
    else:   # result_type == ResultTypeEnum.Dict:
        if period == TdxPeriodEnum.Day:
            formatter = _dict_formatter_for_daily
        else:
            formatter = _dict_formatter_for_minutely

    pattern: struct.Struct
    if period == TdxPeriodEnum.Day:
        pattern = struct.Struct(r'<IIIIIfII')
    else:
        pattern = struct.Struct(r'<HHfffffII')

    offset: int
    raw: bytes = _read_quote(exchange, symbol, period)
    for offset in range(0, len(raw), pattern.size):
        yield formatter(pattern.unpack_from(raw, offset))
