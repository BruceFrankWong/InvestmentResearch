# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import List, Optional, Union
import csv
from pathlib import Path
from enum import Enum
import datetime as dt
from contextlib import closing

import pandas as pd
from tqsdk import TqApi, TqAuth, TqSim
from tqsdk.tools import DataDownloader

from ...utility import CONFIGS, PACKAGE_PATH


class Symbol:
    def __init__(self, exchange: str, product: str, delivery: str):
        self.exchange = exchange
        self.product = product
        self.delivery = delivery


class Period(Enum):
    Tick = 'Tick'
    Second = 'Second'
    Minute = 'Minute'
    Hour = 'Hour'
    Day = 'Day'
    Week = 'Week'
    Month = 'Month'
    Year = 'Year'

    def to_second(self) -> int:
        if self.value == 'Tick':
            return 0
        elif self.value == 'Second':
            return 1
        elif self.value == 'Minute':
            return 60
        elif self.value == 'Hour':
            return 60 * 60
        elif self.value == 'Day':
            return 60 * 60 * 24
        elif self.value == 'Week':
            return 60 * 60 * 24 * 5
        elif self.value == 'Month':
            return 60 * 60 * 24 * 5 * 4
        elif self.value == 'Year':
            return 60 * 60 * 24 * 5 * 4 * 12

    def to_english(self) -> str:
        if self.value == 'Tick':
            return 'Tick'
        elif self.value == 'Second':
            return 'Second'
        elif self.value == 'Minute':
            return 'Minute'
        elif self.value == 'Hour':
            return 'Hour'
        elif self.value == 'Day':
            return 'Day'
        elif self.value == 'Week':
            return 'Week'
        elif self.value == 'Month':
            return 'Month'
        elif self.value == 'Year':
            return 'Year'

    def to_chinese(self) -> str:
        if self.value == 'Tick':
            return 'Tick'
        elif self.value == 'Second':
            return '秒'
        elif self.value == 'Minute':
            return '分钟'
        elif self.value == 'Hour':
            return '小时'
        elif self.value == 'Day':
            return '日'
        elif self.value == 'Week':
            return '周'
        elif self.value == 'Month':
            return '月'
        elif self.value == 'Year':
            return '年'

    def __str__(self, chinese: bool = False):
        if chinese:
            return self.to_chinese()
        else:
            return self.to_english()


class DownloadRequest:
    symbol: str
    start: Union[dt.datetime, dt.date]
    end: Union[dt.datetime, dt.date]
    period: Period

    def __init__(self,
                 symbol: str,
                 period: Period,
                 start: Union[dt.datetime, dt.date],
                 end: Optional[Union[dt.datetime, dt.date]] = None
                 ):
        self.symbol = symbol
        self.period = period
        self.start = start
        if end:
            if isinstance(end, dt.date):
                self.end = end if end < dt.date.today() else dt.date.today()
            else:
                self.end = end if end < dt.datetime.now() else dt.datetime.now()
        else:
            if isinstance(start, dt.date):
                self.end = dt.date.today()
            else:
                self.end = dt.datetime.now()


def tq_download(download_request_list: List[DownloadRequest]):
    # TqSDK api.
    tq_api: TqApi = TqApi(
        auth=TqAuth(
            CONFIGS['TQ']['account'],
            CONFIGS['TQ']['password']
        )
    )

    # Download path, make sure it existed.
    download_path: Path = PACKAGE_PATH.joinpath('data_downloaded')
    if not download_path.exists():
        download_path.mkdir()

    # csv header.
    bar_column_list: List[str] = [
        'open', 'high', 'low', 'close', 'volume', 'open_oi', 'close_oi'
    ]
    tick_column_list: List[str] = [
        'last_price', 'highest', 'lowest',
        'bid_price1', 'bid_volume1', 'ask_price1', 'ask_volume1',
        'volume', 'amount', 'open_interest'
    ]

    # Do the download.
    task_name: str
    file_path: Path
    task: DataDownloader
    with closing(tq_api):
        download_request: DownloadRequest
        for download_request in download_request_list:
            task_name = download_request.symbol
            file_path = download_path.joinpath(
                f'{download_request.symbol}_{download_request.period.to_english()}.csv'
            )
            task = DataDownloader(
                tq_api,
                symbol_list=download_request.symbol,
                dur_sec=download_request.period.to_second(),
                start_dt=download_request.start,
                end_dt=download_request.end,
                csv_file_name=str(file_path)
            )

            while not task.is_finished():
                tq_api.wait_update()
                print(
                    f'正在下载 [{task_name}] 的 {download_request.period.to_chinese()} 数据，'
                    f'已完成： {task.get_progress():>7.3f}%。'
                )

            # 处理下载好的 csv 文件的 header, 也就是 pandas.DataFrame 的 column.
            if task.is_finished():
                df = pd.read_csv(file_path)
                if download_request.period.to_second() == Period.Tick:
                    column_list = tick_column_list
                else:
                    column_list = bar_column_list
                for column in column_list:
                    column_x = ''.join([download_request.symbol, '.', column])
                    if column_x in df.columns:
                        df.rename(columns={column_x: column}, inplace=True)
                df.to_csv(file_path, index=False)
