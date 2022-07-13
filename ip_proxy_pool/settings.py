# -8- coding = utf-8 -*-
# @Time : 2021/4/18 17:30
# @Author : 大漠孤烟
# @File : settings.py
# @Software : PyCharm
import logging
import os

# print(os.getcwd())
# 默认分值通过配置文件进行配置，在进行代理可用性检测时，没遇到一次请求失败减1分，减到0的时候从池中删除，如果检查代理可用就恢复默认分值
# 默认最高分数为50
MAX_SCORE = 50

# 日志配置信息
# 默认的配置
LOG_LEVEL = logging.DEBUG  # 默认等级
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'  # 默认格式
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
LOG_FILENAME = 'log.log'  # 默认日志文件名称

# 测试代理ip的超时时间
TEST_TIMEOUT = 10

# MongoDB数据库的URL
MONGO_URL = 'mongodb:127.0.0.1:27017'

PROXIES_SPIDERS = [
    # 爬虫的全类名，路径：模块.类名
    'core.proxy_spider.proxy_spiders.XiLaSpider',
    'core.proxy_spider.proxy_spiders.YunSpider',
    'core.proxy_spider.proxy_spiders.KuaiSpider',
    'core.proxy_spider.proxy_spiders.ProxyListSpider',
    'core.proxy_spider.proxy_spiders.Ip66Spider',
]

# 4.3.1 修改配置文件，增加爬虫运行时间间隔的配置，单位为小时
RUN_SPIDER_INTERVAL = 12

# 通过配置检测代理ip的异步数量
TEST_PROXIES_ASYNC_COUNT = 10

# 配置检测代理ip的时间间隔，单位为小时
TEST_PROXIES_INTERVAL = 2

# 配置获取的代理IP的最大数量，这个值越小可用性就越高，但是随机性越差
PROXIES_MAX_COUNT = 50
