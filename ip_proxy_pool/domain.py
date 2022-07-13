# -8- coding = utf-8 -*-
# @Time : 2021/4/18 17:29
# @Author : 大漠孤烟
# @File : domain.py
# @Software : PyCharm

from settings import MAX_SCORE


class Proxy(object):

    def __init__(self, ip, port, protocol=-1, nick_type=1, speed=-1, area=None, score=MAX_SCORE, disable_domains=[]):
        # ip:代理的IP地址
        self.ip = ip
        # port:代理ip的端口号
        self.port = port
        # protocol:代理ip支持的协议类型，http是0，https是1，http和https都支持是2
        self.protocol = protocol
        # nick_type:代理ip的匿名程度，高匿0，匿名1，透明2
        self.nick_type = nick_type
        # speed:代理ip的响应速度，单位s
        self.speed = speed
        # area:代理ip所在地区
        self.area = area
        # score:代理ip的评分，用于衡量代理的可用性
        self.score = score
        # 默认分值通过配置文件进行配置，在进行代理可用性检测时，没遇到一次请求失败减1分，减到0的时候从池中删除,如果检查代理可用就恢复默认分值
        # disable_domains:不可用域名列表，有些代理IP在某些域名不可用，在其他域名可用
        self.disable_domains = disable_domains

    def __str__(self):
        # 返回数据字符串
        return str(self.__dict__)
