# -*- coding: UTF-8 -*-

__author__ = 'Bruce Frank Wong'


from typing import Dict, List, Any
import datetime as dt

import requests
from lxml import etree


def crawl_notice_from_dce():
    """
    Crawl notice from the DCE website.
    :return:
    """

    def crawl(url: str) -> str:
        response = requests.get(url)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text

    def get_page_count(text: str) -> int:
        html: etree.Element = etree.HTML(text)
        return int(html.xpath('//div[@class="pagination"]/input[@name="article_paging_list_hidden"]/@totalpage')[0])

    def phase_index(text: str) -> List[Dict[str, str]]:
        phased: List[Dict[str, str]] = []
        html: etree.Element = etree.HTML(text)
        title_list = html.xpath('//ul[@opentype="page"]/li/a/@title')
        date_list = html.xpath('//ul[@opentype="page"]/li/span/text()')
        url_list = html.xpath('//ul[@opentype="page"]/li/a/@href')

        if len(title_list) != len(date_list):
            raise RuntimeError('count different between TITLE and DATE.')
        if len(title_list) != len(url_list):
            raise RuntimeError('count different between TITLE and URL.')

        for t in range(len(title_list)):
            phased.append(
                {
                    'title': title_list[t],
                    'date': dt.date.fromisoformat(date_list[t]),
                    'url': f'http://www.dce.com.cn{url_list[t]}',
                }
            )
        return phased

    def phase_detailed(text: str) -> Dict[str, Any]:
        title: str
        date: dt.date
        code: str
        content: List[str]

        html: etree.Element = etree.HTML(text)
        title = html.xpath('//div[@class="tit_header"]/h2/text()')[0]
        date = html.xpath(
            '//div[@class="detail_content"]/span[@class="detail_content_footer"]/p[@class="notice_date"]/text()'
        )
        try:
            code = html.xpath('//div[@class="tit_header"]/p[@class="summary cj_date"]/text()')[0]
        except IndexError:
            code = ''
        content = html.xpath('//div[@class="detail_content"]/p/text()')
        return {
            'title': title,
            'date': date,
            'code': code.strip('\xa0'),
            'content': content,
        }

    # Main.
    message_index: str = 'Index page {page:3d} phased.'
    message_detailed: str = '\tDetail page {title} phased.'

    url_pattern: str = 'http://www.dce.com.cn/dalianshangpin/ywfw/jystz/ywtz/13305-{page}.html'

    raw: str = crawl(url_pattern.format(page=1))
    page_count: int = get_page_count(raw)

    result: List[Dict[str, Any]] = []
    for i in range(1, page_count+1):
        detailed_page_url_list: List[Dict[str, str]] = phase_index(
            crawl(
                url_pattern.format(page=i)
            )
        )
        print(message_index.format(page=i))
        for page in detailed_page_url_list:
            detailed = phase_detailed(
                crawl(page['url'])
            )
            result.append(
                {
                    'title': page['title'],
                    'date': page['date'],
                    'url': page['url'],
                    'code': detailed['code'],
                    'content': detailed['content'],
                }
            )
            print(message_detailed.format(title=page['title']))
    return result
