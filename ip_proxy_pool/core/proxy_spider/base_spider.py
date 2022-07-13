# -8- coding = utf-8 -*-
# @Time : 2021/4/18 17:28
# @Author : 大漠孤烟
# @File : base_spider.py
# @Software : PyCharm

import requests

from utils.http import get_request_heasers
from lxml import etree
from domain import Proxy


# 1 在base_spider.py中定义一个BaseSpider类
class BaseSpider(object):
    # 2 提供三个类成员变量
    # urls：代理ip网址的url列表
    urls = []
    # group_xpath：分组xpath，获取包含代理ip信息标签列表的xpath
    group_xpath = ""
    # detail_xpath：组内xpath，获取代理ip详情的信息xpath，格式为
    # （'ip':'xx','port':'xx','area':'xx'）
    detail_xpath = {}

    # 3 提供初始化方法，传入爬虫url列表，分组xpath，组内xpath
    def __init__(self, urls=[], group_xpath='', detail_xpath={}):
        if urls:
            self.urls = urls
        if group_xpath:
            self.group_xpath = group_xpath
        if detail_xpath:
            self.detail_xpath = detail_xpath

    def get_page_from_url(self, url):
        """根据url发送请求，获取页面数据"""
        response = requests.get(url, headers=get_request_heasers())
        # response.encoding = 'gbk'
        return response.text

    def get_first_from_list(self, lis):
        """如果列表中有元素就返回第一个，否则就返回空串"""
        return lis[0] if len(lis) != 0 else ''

    def get_proxies_from_page(self, page):
        """解析页面，提取数据，封装为Proxy对象"""
        element = etree.HTML(page)
        # 获取包含代理的标签列表
        trs = element.xpath(self.group_xpath)
        # 遍历trs，获取代理ip相关信息
        for tr in trs:
            ip = self.get_first_from_list(tr.xpath(self.detail_xpath['ip']))
            port = self.get_first_from_list(tr.xpath(self.detail_xpath['port']))
            area = self.get_first_from_list(tr.xpath(self.detail_xpath['area']))
            proxy = Proxy(ip, port, area=area)
            # 使用yield返回提取到的数据
            yield proxy

    def get_proxies(self):
        # 4 对外提供一个获取代理ip的方法
        # 4.1 遍历url列表，获取url
        for url in self.urls:
            # 4.2 根据发动请求，获取页面数据
            page = self.get_page_from_url(url)
            # 4.3 解析页面，提取数据，封装为proxy对象
            proxies = self.get_proxies_from_page(page)
            # 4.4 返回proxy对象列表
            yield from proxies


if __name__ == '__main__':
    config = {
        'urls': [f'http://www.ip3366.net/free/?stype=1&page={i}' for i in range(1, 4)],
        'group_xpath': '//*[@id="list"]/table/tbody/tr',
        'detail_xpath': {
            'ip': './td[1]/text()',
            'port': './td[2]/text()',
            'area': './td[5]/text()'
        }
    }
    spider = BaseSpider(**config)
    for proxy in spider.get_proxies():
        print(proxy)
