# -8- coding = utf-8 -*-
# @Time : 2021/4/18 17:28
# @Author : 大漠孤烟
# @File : run_spiders.py
# @Software : PyCharm

import schedule
import time

# 打猴子补丁
from gevent import monkey

monkey.patch_all()
import importlib
# 导入协程池
from gevent.pool import Pool

from settings import PROXIES_SPIDERS
from settings import RUN_SPIDER_INTERVAL
from core.proxy_validate.httpbin_validate import check_proxy
from core.db.mongo_pool import MongoPool
from utils.log import logger


# 创建一个Runspider类
class RunSpider(object):

    def __init__(self):
        # 创建MongoPool对象
        self.mongopool = MongoPool()
        # 3,使用异步来执行每一个爬虫任务

        # 3.1 在init方法中创建协程池队象
        self.coroutine_pool = Pool()

    def get_spider_from_settings(self):
        """根据配置文件信息，获取爬虫对象列表"""
        # 遍历配置文件中爬虫信息，获取每个爬虫全类名
        for full_class_name in PROXIES_SPIDERS:
            # core.proxy_spider.proxy_spiders.XiLaSpider
            # 获取模块名和类名
            # print(full_class_name.rsplit('.',maxsplit=1))
            module_name, class_name = full_class_name.rsplit('.', maxsplit=1)
            # 根据模块名导入模块
            module = importlib.import_module(module_name)
            # 根据类名从模块中获取类
            cls = getattr(module, class_name)
            # 创建爬虫对象
            spider = cls()
            # print(spider)
            # 也可以通过列表.append 然后返回列表
            yield spider

    # 提供一个运行爬虫的run方法
    def run(self):
        # 2.1 根据配置文件信息，获取爬虫对象列表
        spiders = self.get_spider_from_settings()
        # 2.2 遍历对象列表，获取爬虫对象，遍历爬虫对象的get_proxies方法，获取ip
        for spider in spiders:
            # 3.3 使用异步执行此方法
            # self.__excute_one_spider(spider)
            self.coroutine_pool.apply_async(self.__excute_one_spider, args=(spider,))
        # 3.4 调用协程的join方法，让当前线程等待协程任务的完成
        self.coroutine_pool.join()

    def __excute_one_spider(self, spider):
        # 3.2 在处理一个代理爬虫的代码抽到一个方法
        # 用于处理一个爬虫任务
        # 2.5 异常处理，防止一个爬虫出错影响其他的爬虫
        try:
            # 遍历爬虫对象的get_proxies方法，获取ip
            for proxy in spider.get_proxies():
                # print(proxy)
                # 2.3 检测代理ip
                proxy = check_proxy(proxy)
                # 2.4 如果可用，写入数据库
                # 如果speed不为-1，说明可用
                if proxy.speed != -1:
                    # 写入数据库
                    self.mongopool.insert_one(proxy)
        except Exception as ex:
            logger.exception(ex)

    @classmethod
    def start(cls):
        # 4 使用schedule模块，实现每个一定的时间，执行一次爬虫任务
        # 4.1 定义一个start的类方法
        # 4.2 创建当前类的对象，调用run方法
        rs = RunSpider()
        rs.run()
        # 4.3 使用schedule模块，每个一定时间，执行当前对象的run方法
        # 4.3.1 修改配置文件，增加爬虫运行时间间隔的配置，单位为小时
        schedule.every(RUN_SPIDER_INTERVAL).hours.do(rs.run)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    # rs = RunSpider()
    # rs.run()
    RunSpider.start()

    # 测试schedule
    # def task():
    #     print("呵呵。。")
    #
    # schedule.every(2).seconds.do(task)
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
