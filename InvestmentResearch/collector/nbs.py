# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


"""
    Crawl the National Bureau of Statistics of China web site.
"""


import requests
import lxml


def crawl(url: str) -> str:
    response = requests.get(url)
    if response.status_code == 200:
        response.encoding = 'utf-8'
        return response.text


def crawl_dad_from_mca():
    """
    Crawl the code of the domestic administrative divisions (county and above) from MCA.
    :return:
    """
    # Index pages.
    url: str = 'http://www.mca.gov.cn/article/sj/xzqh/1980/'
    print(crawl(url))
