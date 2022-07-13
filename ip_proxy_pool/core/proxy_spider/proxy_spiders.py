# -8- coding = utf-8 -*-
# @Time : 2021/4/18 17:28
# @Author : 大漠孤烟
# @File : proxy_spiders.py
# @Software : PyCharm

# from base_spider import BaseSpider

import time
import random
import requests

from utils.http import get_request_heasers
from core.proxy_spider.base_spider import BaseSpider
# """
# 1 实现西拉代理爬虫：http://www.xiladaili.com/http/2/
#     定义一个类，继承通用爬虫类
#     提供urls,group_xpath,detail_xpath
# """
#
# class XiLaSpider(BaseSpider):
#     # 准备url列表
#
#     urls = [f'http://www.xiladaili.com/http/{i}/' for i in range(1,3)]
#
#     # group_xpath：分组xpath，获取包含代理ip信息标签列表
#     group_xpath = '/html/body/div/div[3]/div[2]/table/tbody/tr'
#     # detail_xpath：组内xpath，获取代理ip详情的信息xpath，格式为（'ip':'xx','port':'xx','area':'xx'）
#     detail_xpath = {
#         'ip':'./td[1]/text()',
#         # 'ip':'list(./td[1]/text()[0].split(":")[0])',
#         # 'port':'./td[1]/text()[0].split(":")[1]',
#         'port':'./td[1]/text()',
#         'area':'./td[4]/text()',
#     }

"""
1 实现高可用全球免费代理IP库：https://ip.jiangxianli.com/?page=1
    定义一个类，继承通用爬虫类
    提供urls,group_xpath,detail_xpath
"""


class XiLaSpider(BaseSpider):
    # 准备url列表

    urls = [f'https://ip.jiangxianli.com/?page={i}' for i in range(1, 4)]

    # group_xpath：分组xpath，获取包含代理ip信息标签列表
    group_xpath = '/html/body/div[1]/div[2]/div[1]/div[1]/table/tbody/tr'
    # detail_xpath：组内xpath，获取代理ip详情的信息xpath，格式为（'ip':'xx','port':'xx','area':'xx'）
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()',
    }


"""
2 云代理：http://www.ip3366.net/free/
    定义一个类，继承通用爬虫类
    提供urls,group_xpath,detail_xpath
"""


class YunSpider(BaseSpider):
    # 准备url列表

    urls = [f'http://www.ip3366.net/free/?stype=1&page={i}' for i in range(1, 4)]

    # group_xpath：分组xpath，获取包含代理ip信息标签列表
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    # detail_xpath：组内xpath，获取代理ip详情的信息xpath，格式为（'ip':'xx','port':'xx','area':'xx'）
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()',
    }

    def get_page_from_url(self, url):
        """根据url发送请求，获取页面数据"""
        response = requests.get(url, headers=get_request_heasers())
        response.encoding = 'gbk'
        return response.text


"""
3 快代理：https://www.kuaidaili.com/free/
    定义一个类，继承通用爬虫类
    提供urls,group_xpath,detail_xpath
"""


class KuaiSpider(BaseSpider):
    # 准备url列表

    urls = [f'https://www.kuaidaili.com/free/inha/{i}/' for i in range(1, 4)]

    # group_xpath：分组xpath，获取包含代理ip信息标签列表
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    # detail_xpath：组内xpath，获取代理ip详情的信息xpath，格式为（'ip':'xx','port':'xx','area':'xx'）
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()',
    }

    # 当两个页面访问时间间隔太短，就报错
    def get_page_from_url(self, url):
        # 随机等待1~3秒
        time.sleep(random.uniform(1, 3))
        # 调用父类方法，发送请求，获取响应数据
        return super().get_page_from_url(url)


# """
# 4 proxylistplus代理：https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1
#     定义一个类，继承通用爬虫类
#     提供urls,group_xpath,detail_xpath
# """
#
# class ProxyListSpider(BaseSpider):
#     # 准备url列表
#
#     urls = [f'https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{i}' for i in range(1,4)]
#
#     # group_xpath：分组xpath，获取包含代理ip信息标签列表
#     group_xpath = '//*[@id="page"]/table[2]/tr[position()>2]'
#     # detail_xpath：组内xpath，获取代理ip详情的信息xpath，格式为（'ip':'xx','port':'xx','area':'xx'）
#     detail_xpath = {
#         'ip':'./td[2]/text()',
#         'port':'./td[3]/text()',
#         'area':'./td[5]/text()',
#     }


"""
4 89免费代理：https://www.89ip.cn/index.html
    定义一个类，继承通用爬虫类
    提供urls,group_xpath,detail_xpath
"""


class ProxyListSpider(BaseSpider):
    # 准备url列表

    urls = [f'https://www.89ip.cn/index_{i}.html' for i in range(1, 4)]

    # group_xpath：分组xpath，获取包含代理ip信息标签列表
    group_xpath = '//*[@class="layui-col-md8"]/div/div[1]/table/tbody/tr'
    # detail_xpath：组内xpath，获取代理ip详情的信息xpath，格式为（'ip':'xx','port':'xx','area':'xx'）
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()',
    }


"""
5 66免费代理：http://www.66ip.cn/index.html
    定义一个类，继承通用爬虫类
    提供urls,group_xpath,detail_xpath
"""


class Ip66Spider(BaseSpider):
    # 准备url列表

    urls = [f'http://www.66ip.cn/{i}.html' for i in range(1, 4)]

    # group_xpath：分组xpath，获取包含代理ip信息标签列表
    group_xpath = '//*[@id="main"]/div[1]/div[2]/div[1]/table/tr[position()>2]'
    # detail_xpath：组内xpath，获取代理ip详情的信息xpath，格式为（'ip':'xx','port':'xx','area':'xx'）
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()',
    }

    def get_page_from_url(self, url):
        """根据url发送请求，获取页面数据"""
        response = requests.get(url, headers=get_request_heasers())
        response.encoding = 'gbk'
        return response.text


if __name__ == '__main__':
    # spider = XiLaSpider()
    # spider = JiangSpider()
    # spider = YunSpider()
    # spider = KuaiSpider()
    # spider = ProxyListSpider()
    # spider = Ip66Spider()

    for proxy in spider.get_proxies():
        print(proxy)
