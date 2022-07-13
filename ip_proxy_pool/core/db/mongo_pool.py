# -8- coding = utf-8 -*-
# @Time : 2021/4/18 17:26
# @Author : 大漠孤烟
# @File : mongo_pool.py
# @Software : PyCharm
from pymongo import MongoClient
import pymongo
import random

from utils.log import logger
from domain import Proxy


class MongoPool():
    # 1 与数据库建立连接
    def __init__(self):
        # 1.1 建立数据连接，获取要操作的集合
        self.client = MongoClient('localhost', 27017)
        # 1.2 获取要操作的集合
        self.proxies = self.client['proxies_pool']['proxies']

    def __del__(self):
        # 1.3 关闭数据库连接
        self.client.close()

    # 2 实现数据库的增删改查功能
    def insert_one(self, proxy):
        # 2.1 实现插入的功能

        count = self.proxies.count_documents({'_id': proxy.ip})
        if count == 0:
            # 使用proxy的ip作为MongoDB中的主键_id
            dict = proxy.__dict__
            dict['_id'] = proxy.ip
            self.proxies.insert_one(dict)
            logger.info(f"插入新的代理{proxy}")
        else:
            logger.warning(f"已存在代理:{proxy}")

    def update_one(self, proxy):
        """2.2 实现修改的功能"""
        self.proxies.update_one({'_id': proxy.ip}, {'$set': proxy.__dict__})

    def delete_one(self, proxy):
        """2.3 实现删除代理：根据代理的ip删除代理"""
        self.proxies.delete_one({'_id': proxy.ip})
        logger.info(f'删除代理ip：{proxy}')

    def find_all(self):
        """2.4 查询所有代理ip的功能"""
        cursor = self.proxies.find()
        for item in cursor:
            # 删除_id这个key
            item.pop('_id')
            print(item)
            proxy = Proxy(**item)
            yield proxy

    # 3 返回满足要求的代理ip列表
    def find(self, conditions={}, count=0):
        """
        3.1 实现查询功能：根据条件进行查询，可以指定查询数量，先分数降序，速度升序，保证优质的代理ip在上面
        params：conditions:查询条件字典
        count：限制最多取出多少个代理ip
        return：返回满足要求的代理ip列表
        """
        cursor = self.proxies.find(conditions, limit=count).sort \
            ([('score', pymongo.DESCENDING), ('speed', pymongo.ASCENDING)])
        # 准备列表，用于存储查询代理ip
        proxy_list = []
        # 遍历cursor
        for item in cursor:
            item.pop('_id')
            proxy = Proxy(**item)
            proxy_list.append(proxy)
        return proxy_list

    def get_proxies(self, protocol=None, domain=None, count=0, nick_type=0):
        """
        3.2 实现根据协议类型和要访问的网站域名，获取代理ip列表
        :param protocol: 协议：http，https
        :param domain: 域名
        :param count: 限制获取多个代理ip，默认获取所有的
        :param nick_type: 匿名类型，默认高匿
        :return: 满足要求的代理ip列表
        """
        # 定义查询条件
        conditions = {'nick_type': nick_type}
        # 根据协议，指定查询条件
        if protocol is None:
            # 如果没有传入协议类型，返回支持http和https协议的代理ip
            conditions['protocol'] = 2
        elif protocol.lower == 'http':
            conditions['protocol'] = {'$in': [0, 2]}
        else:
            conditions['protocol'] = {'$in': [1, 2]}

        if domain:
            conditions['disable_domain'] = {'$nin': [domain]}

        return self.find(conditions, count=count)

    def random_proxies(self, protocol=None, domain=None, count=0, nick_type=0):
        """
        3.3 实现根据协议类型和要访问的网站域名，随机获取代理一个ip
        :param protocol: 协议：http，https
        :param domain: 域名
        :param count: 限制获取多个代理ip，默认获取所有的
        :param nick_type: 匿名类型，默认高匿
        :return: 满足要求的随机的一个代理ip
        """
        proxy_list = self.get_proxies(protocol=protocol, domain=domain, count=count, nick_type=nick_type)
        return random.choice(proxy_list)

    def disable_domain(self, ip, domain):
        """
        3.4 实现把指定域名添加到指定ip的disable_domain列表中
        :param ip: IP地址
        :param domain: 域名
        :return: 如果返回True，表示添加成功，否则添加失败
        """
        # print(self.proxies.count_documents({'_id':ip,'disable_domain':domain}))
        if self.proxies.count_documents({'_id': ip, 'disable_domain': domain}) == 0:
            # 如果disable_domains字段中没有这个域名才添加
            self.proxies.update_one({'_id': ip}, {'$push': {'disable_domains': domain}})
            return True
        return False


if __name__ == '__main__':
    mongo = MongoPool()
    # proxy = Proxy("150.255.131.135",port='8080')
    # proxy = Proxy("150.255.131.138",port='8080')
    # proxy = Proxy("110.77.134.112",port='8080')
    # proxy = Proxy("178.19.97.1",port='8088')
    proxy = Proxy("71.41.27.245", port='8080')
    # proxy = Proxy("176.106.120.82",port='8080')
    # proxy = Proxy("190.104.170.234",port='8080')
    # proxy = Proxy("	203.160.163.58",port='8080')
    # mongo.insert_one(proxy)
    # proxy = Proxy("150.255.131.139", port='8888')
    # mongo.update_one(proxy)
    mongo.delete_one(proxy)
    # for proxy in mongo.find_all():
    #     print(proxy)

    # dic = {'ip': '150.255.131.600', 'port': '8080', 'protocol': 0, 'nick_type': 1, 'speed': 8.2, 'area': None, 'score': 50, 'disable_domains': ['www.jd.com']}
    # dic = {'ip': '150.255.131.700', 'port': '8888', 'protocol': 1, 'nick_type': 1, 'speed': 1.2, 'area': None, 'score': 50, 'disable_domains': ['www.tb.com']}
    # dic = {'ip': '150.255.131.800', 'port': '8080', 'protocol': 2, 'nick_type': 1, 'speed': 5.4, 'area': None, 'score': 50, 'disable_domains': ['www.mt.com']}
    # dic = {'ip': '150.255.131.900', 'port': '8080', 'protocol': 2, 'nick_type': 1, 'speed': -1, 'area': None, 'score': 50, 'disable_domains': ['www.mt.com']}
    # proxy = Proxy(**dic)
    # mongo.insert_one(proxy)

    # for proxy in mongo.find({'protocol':2},count=1):
    #     print(proxy)

    # for proxy in mongo.get_proxies(protocol='https'):
    #     print(proxy)

    mongo.disable_domain('150.255.131.135', 'baidu.com')
