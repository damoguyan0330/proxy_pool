# -8- coding = utf-8 -*-
# @Time : 2021/4/18 17:30
# @Author : 大漠孤烟
# @File : main.py
# @Software : PyCharm
"""
- - 1） 定义一个run方法用于启动代理池
    - 1.1） 定义一个列表，用于存储要启动的进程
    - 1.2）创建启动爬虫的进程，添加到列表中
    - 1.3）创建启动检测代理ip的进程，添加到列表中
    - 1.4）创建启动web服务的进程，添加到列表中
    - 1.5）遍历进程列表，启动所有进程
    - 1.6）遍历进程列表，让主进程等待子进程完成

- 2）在if __name__ == '__main__':中调用run方法
"""
from multiprocessing import Process
from core.proxy_spider.run_spiders import RunSpider
from core.proxy_test import ProxyTest
from core.proxy_api import ProxyApi


def run():
    # 1） 定义一个run方法用于启动代理池
    # - 1.1） 定义一个列表，用于存储要启动的进程
    process_list = []
    # - 1.2）创建启动爬虫的进程，添加到列表中
    process_list.append(Process(target=RunSpider.start))
    # - 1.3）创建启动检测代理ip的进程，添加到列表中
    process_list.append(Process(target=ProxyTest.start))
    # - 1.4）创建启动web服务的进程，添加到列表中
    process_list.append(Process(target=ProxyApi.start))
    # - 1.5）遍历进程列表，启动所有进程
    for process in process_list:
        # 设置进程守护
        process.daemon = True
        process.start()
    # - 1.6）遍历进程列表，让主进程等待子进程完成
    for process in process_list:
        process.join()


if __name__ == '__main__':
    run()
