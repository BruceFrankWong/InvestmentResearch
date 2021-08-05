# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict, List, Optional, Union, Any
import datetime as dt
from pathlib import Path
import zipfile
import json

import peewee
import requests
from lxml import etree

from ...utility import CONFIGS, PACKAGE_PATH
from ...database.model import Country, Holiday, Exchange, FuturesProduct, FuturesContract
from ...database.model.quote import FuturesQuoteDaily


try:
    exchange_shfe = Exchange.get(Exchange.symbol == 'SHFE')
except peewee.OperationalError:
    Exchange.create_table()
    try:
        country = Country.get(Country.alpha3 == 'CHN')
    except peewee.OperationalError:
        Country.create_table()
        country = Country(
            name_zh='中国',
            name_en='China',
            fullname_zh='中华人民共和国',
            fullname_en="People's Republic of China",
            alpha2='CN',
            alpha3='CHN',
            numeric='156'
        )
        country.save()
    finally:
        exchange_shfe = Exchange(
            symbol='SHFE',
            name='上期所',
            fullname='上海期货交易所',
            url='http://www.shfe.com.cn/',
            country=Country.get(Country.alpha3 == 'CHN')
        )
        exchange_shfe.save()


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
            #     crawler=exchange_shfe,
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

    result: List[FuturesQuoteDaily] = []

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


def crawl_notice_from_shfe():
    """
    Crawl notice from the SHFE website.
    :return:
    """
    def crawl(url: str) -> str:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text

    def get_page_count(text: str) -> int:
        html: etree.Element = etree.HTML(text)
        return int(html.xpath('//div[@class="page-no"]/select/option')[-1].text)

    def phase_index(text: str) -> List[Dict[str, str]]:
        phased: List[Dict[str, str]] = []
        html: etree.Element = etree.HTML(text)
        title_list = html.xpath('//div[@class="p4 lawbox"]/ul/li/a/@title')
        date_list = html.xpath('//div[@class="p4 lawbox"]/ul/li/span/text()')
        url_list = html.xpath('//div[@class="p4 lawbox"]/ul/li/a/@href')

        if len(title_list) != len(date_list):
            raise RuntimeError('count different between TITLE and DATE.')
        if len(title_list) != len(url_list):
            raise RuntimeError('count different between TITLE and URL.')

        for t in range(len(title_list)):
            phased.append(
                {
                    'title': title_list[t],
                    'date': dt.date.fromisoformat(date_list[t][1:-1]),
                    'url': f'http://www.shfe.com.cn{url_list[t]}',
                }
            )
        return phased

    def phase_detailed(text: str) -> Dict[str, Any]:
        title: str
        date: dt.date
        code: str
        content: List[str]

        html: etree.Element = etree.HTML(text)
        article = html.xpath('//div[@class="article-detail-text"]')[0]
        title = article.xpath('//h1/text()')[0]
        date = dt.date.fromisoformat(article.xpath('//p[@class="article-date"]/text()')[0][-10:])
        try:
            code = article.xpath('//p[@style="text-align: center;" or @style="text-align: center"]/text()')[0]
        except IndexError:
            code = ''
        content = article.xpath('//p[not(@*)]/text()')
        return {
            'title': title,
            'date': date,
            'code': code.strip('\xa0'),
            'content': content,
        }

    url_front: str = 'http://www.shfe.com.cn/news/notice/index.html'
    url_pattern: str = 'http://www.shfe.com.cn/news/notice/index_{count}.html'
    message_index: str = 'Index page {page:3d} phased.'
    message_detailed: str = '\tDetail page {title} phased.'

    raw: str = crawl(url_front)
    page_count: int = get_page_count(raw)
    detailed_page_url_list: List[Dict[str, str]]
    result: List[Dict[str, Any]] = []

    detailed_page_url_list = phase_index(raw)
    print(message_index.format(page=1))
    for item in detailed_page_url_list:
        temp = phase_detailed(crawl(item['url']))
        # print('='*10)
        # print(temp)
        result.append(
            {
                'title': item['title'],
                'date': item['date'],
                'url': item['url'],
                'code': temp['code'],
                'content': temp['content'],
            }
        )
        print(message_detailed.format(title=item['title']))

    for i in range(2, page_count+1):
        detailed_page_url_list = phase_index(
            crawl(
                url_pattern.format(count=i)
            )
        )
        print(message_index.format(page=i))
        for item in detailed_page_url_list:
            temp = phase_detailed(crawl(item['url']))
            # print('='*10)
            # print(temp)
            result.append(
                {
                    'title': item['title'],
                    'date': item['date'],
                    'url': item['url'],
                    'code': temp['code'],
                    'content': temp['content'],
                }
            )
            print(message_detailed.format(title=item['title']))

    return result
