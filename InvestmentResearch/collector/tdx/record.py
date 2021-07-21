# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict, List, Any
from pathlib import Path
import csv
import datetime as dt

from . import TdxRecordTypeEnum


def read_record(record_file: Path, type_: TdxRecordTypeEnum):
    record_list: List[Dict[str, Any]] = []
    with open(record_file, mode='r', newline='', encoding='gbk') as csv_file:
        reader = csv.DictReader(csv_file, delimiter='\t')

        if type_ == TdxRecordTypeEnum.Cash:
            for row in reader:
                print(row)
                record_list.append(
                    {
                        'date': dt.date(
                            year=int(row['发生日期'][2:6]),
                            month=int(row['发生日期'][6:8]),
                            day=int(row['发生日期'][8:10]),
                        ),
                        'time': dt.time.fromisoformat(row['转帐时间'][2:-1]),
                        'offset': row['业务名称'][2:-1],
                        'amount': float(row['转帐金额'][2:-1]),
                    }
                )
        elif type_ == TdxRecordTypeEnum.Order:
            for row in reader:
                print(row)
                record_list.append(
                    {
                        'date': dt.date(
                            year=int(row['委托日期'][2:6]),
                            month=int(row['委托日期'][6:8]),
                            day=int(row['委托日期'][8:10]),
                        ),
                        'time': dt.time.fromisoformat(row['委托时间'][2:-1]),
                        'symbol': row['证券代码'][2:-1],
                        'name': row['证券名称'][2:-1],
                        'offset': row['买卖标志'][2:-1],
                        'status': row['状态说明'][2:-1],
                        'price_order': float(row['委托价格']),
                        'volume_order': int(row['委托数量']),
                        'order_sn': row['委托编号'][2:-1],
                        'price_trade': float(row['成交价格']),
                        'volume_trade': float(row['成交数量']),
                        'mode': row['报价方式'][2:-1],
                        'account': row['股东代码'][2:-1]
                    }
                )
        elif type_ == TdxRecordTypeEnum.Trade:
            for row in reader:
                record_list.append(
                    {
                        'date': dt.date(
                            year=int(row['成交日期'][2:6]),
                            month=int(row['成交日期'][6:8]),
                            day=int(row['成交日期'][8:10]),
                        ),
                        'symbol': row['证券代码'][2:-1],
                        'name': row['证券名称'][2:-1],
                        'offset': row['买卖标志'][2:-1],
                        'price': float(row['成交价格']),
                        'volume': int(row['成交数量']),
                        'trade_sn': row['成交编号'][2:-1],
                        'order_sn': row['委托编号'][2:-1],
                        'account': row['股东代码'][2:-1]
                    }
                )
        else:
            for row in reader:
                print(row)
    [print(item) for item in record_list]
