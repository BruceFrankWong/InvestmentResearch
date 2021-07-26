# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


import pytest

from InvestmentResearch.collector.exchange.ssic import (
    SSICIndustryClassificationEnum,
    get_trading_calendar,
    get_industry,
)


@pytest.mark.run(order=9)
def test_get_trading_calendar():
    """
    Test for get_trading_calendar.
    """
    result = get_trading_calendar()
    assert len(result.data) == result.count


@pytest.mark.run(order=9)
def test_get_industry():
    """
    Test for get_industry.
    """
    result = get_industry(SSICIndustryClassificationEnum.SSIC)
    assert len(result.data) == result.count
