# -8- coding = utf-8 -*-
# @Time : 2021/4/18 17:29
# @Author : 大漠孤烟
# @File : proxy_api.py
# @Software : PyCharm
"""
实现代理池的api模块——为爬虫提供高可用代理的服务接口--proxy_api.py

- 实现根据协议类型和域名，提供随机获取高可用代理ip的服务
- 实现根据协议类型和域名，提供获取多个高可用代理ip的服务
- 实现给指定ip追加不可用域名的服务
- 实现
1 在proxy_api.py模块中创建一个ProxyApi类
2 实现初始方法
    - 2.1 初始一个Flask的web服务器
    - 2.2 实现根据协议类型和域名，提供随机获取高可用代理ip的服务
      - 可通过protocol和domain参数对ip进行过滤
      - protocol：当前请求的协议类型
      - domain：当前请求域名
    - 2.3 实现根据协议类型和域名，提供获取多个高可用代理ip的服务
      - 可用通过protocol和domain参数对ip进行过滤
    - 2.4 实现给指定ip追加不可用域名的服务
      - 如果在获取ip的时候，有指定域名参数，将不再获取该ip，从而进一步提高代理ip的可用性
3 实现run方法，用于启动flask的web服务
4 实现start类方法，用于通过类名启动服务

"""
from flask import Flask, request
import json

from core.db.mongo_pool import MongoPool
from settings import PROXIES_MAX_COUNT


class ProxyApi(object):

    def __init__(self):
        # 实现初始方法
        # 2.1 初始一个Flask的web服务器
        self.app = Flask(__name__)
        # 创建MongoPool对象用于操作数据库
        self.mongo_pool = MongoPool()

        @self.app.route('/random')
        def random():
            """
            2.2 实现根据协议类型和域名，提供随机获取高可用代理ip的服务
              - 可通过protocol和domain参数对ip进行过滤
              - protocol：当前请求的协议类型
              - domain：当前请求域名
            """
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            # print(protocol)
            # print(domain)
            proxy = self.mongo_pool.random_proxies(protocol, domain, count=PROXIES_MAX_COUNT)

            if protocol:
                return f"{protocol}://{proxy.ip}:{proxy.port}"
            else:
                return f"{proxy.ip}:{proxy.port}"

            # return '测试'

        @self.app.route('/proxies')
        def proxies():
            """
            2.3 实现根据协议类型和域名，提供获取多个高可用代理ip的服务
            可用通过protocol和domain参数对ip进行过滤
            :return:
            """
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxies = self.mongo_pool.get_proxies(protocol, domain, count=PROXIES_MAX_COUNT)
            # proxies是一个Proxy对象的列表，但是proxy对象不能进行json序列化，需要转换为字典列表
            proxies = [proxy.__dict__ for proxy in proxies]
            # 返回json格式值串
            return json.dumps(proxies)

        # 2.4 实现给指定ip追加不可用域名的服务
        @self.app.route('/disable')
        def disable_domain():
            ip = request.args.get('ip')
            domain = request.args.get('domain')

            if ip is None:
                return '请提供ip参数'
            if domain is None:
                return '请提供domain参数'

            self.mongo_pool.disable_domain(ip, domain)
            return f"{ip}禁用域名{domain}成功"

    def run(self):
        # 3 实现run方法，用于启动flask的web服务
        self.app.run('0.0.0.0', port=16888)

    @classmethod
    def start(cls):
        # 4 实现start类方法，用于通过类名启动服务
        proxy_api = cls()
        proxy_api.run()


if __name__ == '__main__':
    # proxy_api = ProxyApi()
    # proxy_api.run()
    ProxyApi.start()
