# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict, List, Optional, Union
import datetime as dt
from pathlib import Path
import zipfile
import json

import requests
# import openpyxl

from ...utility import CONFIGS, PACKAGE_PATH
from ...database.model import Country, Holiday, Exchange, FuturesProduct, FuturesContract
from ...database.model.futures import FuturesQuotationDaily


exchange_shfe = Exchange.get(Exchange.symbol == 'SHFE')


def handle_date_list(data_begin: dt.date, day: Optional[Union[dt.date, List[dt.date]]] = None) -> List[dt.date]:
    result: List[dt.date]
    if day is not None:
        if isinstance(day, dt.date):
            if day < data_begin:
                raise ValueError(
                    f'SHFE could not provide data before {data_begin}, so <year> should not less than {data_begin}.'
                )
            else:
                result = [day]
        else:
            result = []
            for d in day:
                if d >= data_begin:
                    result.append(d)
    else:
        result = []
        country: Country = Country.get(Country.alpha3 == 'CHN')
        holiday_list: List[dt.date] = Holiday.select().where(Holiday.country == country)
        for x in range((dt.date.today() - data_begin).days + 1):
            d = data_begin + dt.timedelta(days=x)
            if d not in holiday_list:
                result.append(d)
    return result


def str2date(string: str) -> dt.date:
    return dt.date(
        year=int(string[:4]),
        month=int(string[4:6]),
        day=int(string[6:8]),
    )


def get_contract_from_shfe(day: Optional[Union[dt.date, List[dt.date]]] = None):
    result: List[FuturesContract] = []
    url: str = 'http://www.shfe.com.cn/data/instrument/ContractBaseInfo{date}.dat'
    response = requests.get(url.format(date=day.isoformat().replace('-', '')))
    if response.status_code == 200:
        print('data got.')
        data: dict = json.loads(response.text)
        product: str
        for item in data['ContractBaseInfo']:
            print(item)
            instrument_id = item['INSTRUMENTID'].strip()
            print(
                f'Symbol: {instrument_id}, '
                f'Product: {instrument_id[:2]}, '
                f'Delivery: {instrument_id[-4:]}, '
                f'Listed on: {str2date(item["OPENDATE"])}, '
                f'Expired on: {str2date(item["EXPIREDATE"])}, '
                f'Delivery begin on: {str2date(item["STARTDELIVDATE"])}, '
                f'Delivery end on: {str2date(item["ENDDELIVDATE"])}, '
                f'Basis price: {float(item["BASISPRICE"])}, '
            )
            # product, _ = FuturesProduct.get_or_create(
            #     exchange=exchange_shfe,
            #     symbol=item['INSTRUMENTID'][:2],
            #     delivery_month=item['INSTRUMENTID'][3:],
            #     defaults={
            #         'name_zh': item['PRODUCTNAME'].strip(),
            #     }
            # )
            # result.append(
            #     FuturesContract(
            #         product=product,
            #     )
            # )


def get_futures_info_from_shfe(day: Optional[Union[dt.date, List[dt.date]]] = None):
    data_begin: dt.date = dt.date.fromisoformat('2002-01-07')

    download_list: List[dt.date]
    if day is not None:
        if isinstance(day, dt.date):
            if day < data_begin:
                raise ValueError(
                    f'SHFE could not provide data before {data_begin}, so <year> should not less than {data_begin}.'
                )
            else:
                download_list = [day]
        else:
            download_list = []
            for d in day:
                if d >= data_begin:
                    download_list.append(d)
    else:
        download_list = []
        country: Country = Country.get(Country.alpha3 == 'CHN')
        holiday_list: List[dt.date] = Holiday.select().where(Holiday.country == country)
        for x in range((dt.date.today() - data_begin).days + 1):
            d = data_begin + dt.timedelta(days=x)
            if d not in holiday_list:
                download_list.append(d)
    print(download_list)

    result: List[FuturesQuotationDaily] = []

    http_header: Dict[str, str] = CONFIGS['http_header']
    http_header['Referer'] = 'http://www.sse.com.cn/'

    url: str = 'http://www.shfe.com.cn/data/dailydata/kx/kx{date}.dat'

    exchange = Exchange.get(Exchange.symbol == 'SHFE')

    product_skip_list: List[str] = [
        'sc_tas',
    ]
    delivery_skip_list: List[str] = [
        '小计',
    ]
    response = requests.get(url.format(date=day.isoformat().replace('-', '')))
    if response.status_code == 200:
        print('data got.')
        data: dict = json.loads(response.text)
        for item in data['o_curinstrument']:
            print(item)
            product_id = item['PRODUCTGROUPID'].strip()
            if len(product_id) == 0 or product_id in product_skip_list:
                continue
            product, _ = FuturesProduct.get_or_create(
                exchange=exchange,
                symbol=product_id,
                defaults={
                    'name_zh': item['PRODUCTNAME'].strip(),
                }
            )
            print(product, type(product), _)

            delivery_month = item['DELIVERYMONTH'].strip()
            if delivery_month in delivery_skip_list:
                continue
            print(delivery_month)
            contract, _ = FuturesContract.get_or_create(
                product=product,
                delivery_month=delivery_month,
            )
            print(contract, type(contract), _)
        # for k, v in data['o_curinstrument'][0].items():
        #     print(k, v)


def get_option_info_from_shfe(day: dt.date) -> List[FuturesProduct]:
    result: List[FuturesProduct] = []

    http_header: Dict[str, str] = CONFIGS['http_header']
    http_header['Referer'] = 'http://www.sse.com.cn/'

    url: str = 'http://www.shfe.com.cn/data/dailydata/option/kx/kx20210715.dat'

    response = requests.get(url.format(date=day.isoformat().replace('-', '')))

    return result


def get_year_info_from_shfe(year: Optional[Union[int, List[int]]] = None):
    data_begin: int = 2009

    url: str = 'http://www.shfe.com.cn/historyData/MarketData_Year_{year}.zip'

    # Handle download year(s).
    download_list: List[int]
    if year is not None:
        if isinstance(year, int):
            if year < data_begin:
                raise ValueError(
                    f'SHFE could not provide data before {data_begin}, so <year> should not less than {data_begin}.'
                )
            else:
                download_list = [year]
        else:
            download_list = []
            for y in year:
                if y >= data_begin:
                    download_list.append(y)
    else:
        download_list = [x for x in range(data_begin, dt.date.today().year + 1)]
    print(download_list)

    # Download path, make sure it existed.
    download_path: Path = PACKAGE_PATH.joinpath('data_downloaded')
    if not download_path.exists():
        download_path.mkdir()

    file_path: Path
    for y in download_list:
        file_path = download_path.joinpath(f'SHFE_{y}.zip')

        # 流式下载
        # response = requests.get(url.format(year=y), stream=True)
        # with open(file_path, 'wb') as f:
        #     for chunk in response.iter_content(chunk_size=1024*1024):  # 每次加载1024字节
        #         f.write(chunk)

        # 普通下载
        response = requests.get(url.format(year=y))
        with open(file_path, 'wb') as f:
            f.write(response.content)

        # 解压文件

