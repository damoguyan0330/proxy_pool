# -8- coding = utf-8 -*-
# @Time : 2021/4/18 17:28
# @Author : 大漠孤烟
# @File : proxy_test.py
# @Software : PyCharm


"""
1)在proxy_test.py中，创建ProxyTest类
2)提供一个run方法，用于处理检测代理IP的核心逻辑
  - 2.1）从数据库中获取代理IP
  - 2.2）遍历代理IP列表
  - 2.3）检查代理IP可用性
    2.4)如果不可用，该代理-1，若分数变为0，就从数据库中删除该ip，否则更新该代理ip
    2.5)如果可用，则回复该代理ip的分数，更新到数据库中
3)为了提高检查速度，使用异步来执行检测任务

    - 3.1）把要检测的代理IP放到队列中
    - 3.2）把检查一个代理可用性的代码抽取到一个方法中，从队列中获取IP，进行检查，检查完毕调取队列中的task_done方法
    - 3.3）通过异步回调，使用死循环不断执行此方法
    - 3.4）开启多个异步任务，来处理代理IP的检测，通过配置文件指定异步数量

4）使用schedule模块，每个一段时间，执行一次检测任务

- 4.1）定义一个start的类方法
- 4.2）创建当前类的对象，调用run方法
- 4.3）使用schedule模块，每个一定时间，执行当前对象的run方法
"""
from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool
from queue import Queue
import time
import schedule

from core.db.mongo_pool import MongoPool
from settings import MAX_SCORE, TEST_PROXIES_ASYNC_COUNT, TEST_PROXIES_INTERVAL
from core.proxy_validate.httpbin_validate import check_proxy


# 在proxy_test.py中，创建ProxyTest类
class ProxyTest(object):

    def __init__(self):
        # 创建mongopool对象
        self.mongo_pool = MongoPool()
        # 3.1 在init方法，创建队列和协程池
        self.queue = Queue()
        self.coroutine_pool = Pool()

    def __check_callback(self, temp):
        # 死循环
        self.coroutine_pool.apply_async(self._check_one_proxy, callback=self.__check_callback)

    def run(self):
        # 2)提供一个run方法，用于处理检测代理IP的核心逻辑
        # - 2.1）从数据库中获取代理IP
        proxies = self.mongo_pool.find_all()
        # 2.2）遍历代理IP列表
        for proxy in proxies:
            print(proxy)
            self.queue.put(proxy)

        # 3.4）开启多个异步任务，来处理代理IP的检测，通过配置文件指定异步数量
        for i in range(TEST_PROXIES_ASYNC_COUNT):
            # 3.3）通过异步回调，使用死循环不断执行此方法
            self.coroutine_pool.apply_async(self._check_one_proxy, callback=self.__check_callback)

        # 让当前线程等待任务完成
        self.queue.join()

    def _check_one_proxy(self):
        # 3.2）把检查一个代理可用性的代码抽取到一个方法中，
        # 从队列中获取IP，进行检查，检查完毕
        proxy = self.queue.get()

        proxy = check_proxy(proxy)
        if proxy.speed == -1:
            # 如果不可用，该代理 - 1，
            proxy.score -= 1
            # 若分数变为0，就从数据库中删除该ip，
            if proxy.score == 0:
                self.mongo_pool.delete_one(proxy)
            # 否则更新该代理ip
            else:
                self.mongo_pool.update_one(proxy)
            print(proxy.score)
        else:
            # 如果可用，则回复该代理ip的分数，更新到数据库中
            proxy.score = MAX_SCORE
            self.mongo_pool.update_one(proxy)
        # 调取队列中的task_done方法
        self.queue.task_done()

    # 4）使用schedule模块，每个一段时间，执行一次检测任务
    @classmethod
    def start(cls):
        # - 4.1）定义一个start的类方法
        # - 4.2）创建当前类的对象，调用run方法
        pt = cls()
        pt.run()
        # - 4.3）使用schedule模块，每个一定时间，执行当前对象的run方法
        schedule.every(TEST_PROXIES_INTERVAL).hours.do(pt.run)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    # pt = ProxyTest()
    # pt.run()
    ProxyTest.start()
