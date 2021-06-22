# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


import pytest

from typing import Any, Dict, List
import datetime as dt


@pytest.mark.run(order=8)
def test_product():
    """
    Test for simulation.
    """
    # To pass test_utility.test_config_path, any import about InvestmentResearch should in test case.
    from InvestmentResearch.database import db, Exchange
    from InvestmentResearch.database.model.futures import FuturesProduct

    # Create models but not commit into database with simulation data.
    product_data_list: List[Dict[str, Any]] = [
        {
            'exchange': 'SHFE',
            'symbol': 'HC',
            'name_zh': '热轧卷板',
            'name_en': 'Hot rolled coils',
            'listing_date': dt.date.fromisoformat('2014-03-21'),
            'initial_contract': '1407;1408;1409;1410;1411;1412;1501;1502;1503',
            'announced_date': dt.date.fromisoformat('2014-03-17'),
            'announcement_url': 'http://www.shfe.com.cn/news/notice/911319760.html',
        },
        {
            'exchange': 'SHFE',
            'symbol': 'RB',
            'name_zh': '螺纹钢',
            'name_en': 'Steel Rebar',
            'listing_date': dt.date.fromisoformat('2009-03-27'),
            'initial_contract': '0909;0910;0911;0912;1001;1002;1003',
            'announced_date': dt.date.fromisoformat('2014-03-23'),
            'announcement_url': 'http://www.shfe.com.cn/news/notice/92235792.html',
        },
    ]

    product_list: List[FuturesProduct] = [
        FuturesProduct(
            exchange=Exchange.get(Exchange.symbol == data['exchange']),
            symbol=data['symbol'],
            name_zh=data['name_zh'],
            name_en=data['name_en'],
            listing_date=data['listing_date'],
            initial_contract=data['initial_contract'],
            announced_date=data['announced_date'],
            announcement_url=data['announcement_url']
        ) for data in product_data_list
    ]

    # Commit into database.
    if FuturesProduct.table_exists():
        FuturesProduct.drop_table()
    with db.atomic():
        FuturesProduct.create_table()
        FuturesProduct.bulk_create(product_list, batch_size=100)


@pytest.mark.run(order=8)
def test_contract():
    """
    Test for simulation.
    """
    # To pass test_utility.test_config_path, any import about InvestmentResearch should in test case.
    from InvestmentResearch.database import db
    from InvestmentResearch.database.model.futures import FuturesProduct, FuturesContract

    # Contract.
    contract_data_list: List[Dict[str, Any]] = [
        {
            'product': 'HC',
            'symbol': '2107',
            'listing_date': '2020-07-16',
            'expiration_date': '2021-07-15',
            'delivery_date_begin': '2021-07-16',
            'delivery_date_end': '2021-07-20',
        },
        {
            'product': 'HC',
            'symbol': '2108',
            'listing_date': '2020-08-18',
            'expiration_date': '2021-08-16',
            'delivery_date_begin': '2021-08-17',
            'delivery_date_end': '2021-08-19',
        },
        {
            'product': 'HC',
            'symbol': '2109',
            'listing_date': '2020-09-16',
            'expiration_date': '2021-09-15',
            'delivery_date_begin': '2021-09-16',
            'delivery_date_end': '2021-09-22',
        },
    ]

    contract_list: List[FuturesContract] = [
        FuturesContract(
            product=FuturesProduct.get(FuturesProduct.symbol == data['product']),
            symbol=data['symbol'],
            listing_date=dt.date.fromisoformat(data['listing_date']),
            expiration_date=dt.date.fromisoformat(data['expiration_date']),
            delivery_date_begin=dt.date.fromisoformat(data['delivery_date_begin']),
            delivery_date_end=dt.date.fromisoformat(data['delivery_date_end'])
        ) for data in contract_data_list
    ]

    # TransactionRule.create_table()
    if FuturesContract.table_exists():
        FuturesContract.drop_table()
    with db.atomic():
        FuturesContract.create_table()
        FuturesContract.bulk_create(contract_list, batch_size=100)

    db.close()
