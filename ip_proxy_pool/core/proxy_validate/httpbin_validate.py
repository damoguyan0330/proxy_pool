#-8- coding = utf-8 -*-
#@Time : 2021/4/18 17:27
#@Author : 大漠孤烟
#@File : httpbin_validate.py
#@Software : PyCharm
import requests
import time
import json

from utils.http import get_request_heasers
from settings import TEST_TIMEOUT
from utils.log import logger
from domain import Proxy





def check_proxy(proxy):
    """
    用于检查指定代理ip响应速度，匿名程度，支持协议类型
    params proxy：代理ip模型对象
    return：检查后的代理ip模型对象
    """
    # 准备代理ip模型字典
    proxies = {
        'http':'http://{}:{}'.format(proxy.ip,proxy.port),
        'https':'http://{}:{}'.format(proxy.ip,proxy.port),
    }
    # 测试该代理ip
    http,http_nick_type,http_speed = __check_http_proxies(proxies)
    https,https_nick_type,https_speed = __check_http_proxies(proxies)

    # 代理ip支持的协议类型，http是0，https是1，http和https都支持是2
    if http and https:
        proxy.protocal = 2
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif http:
        proxy.protocal = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif https:
        proxy.protocal = 1
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed
    else:
        proxy.protocal = -1
        proxy.nick_type = -1
        proxy.speed = -1
    return proxy

def __check_http_proxies(proxies,is_http=1):
    # nick_type: 代理ip的匿名程度，高匿0，匿名1，透明2
    nick_type = -1
    # 响应速度
    speed = -1
    if is_http:
        test_url = "http://httpbin.org/get"
    else:
        test_url = 'https://httpbin.org/get'

    try:
        # 获取开始时间
        start = time.time()
        # 发送请求，获取响应数据
        response = requests.get(test_url,headers=get_request_heasers(),proxies=proxies)

        if response.ok:
            # 计算响应速度
            speed = round(time.time() - start,2)
            # 匿名程度
            # 把响应的json字符串转换成字典
            dict = json.loads(response.text)
            # 获取来源ip：origin
            origin = dict['origin']
            proxy_connection = dict['headers'].get['Proxy-Connection']
            # 1）如果响应的origin中有','分割的两个ip就是透明代理ip
            if ',' in origin:
                nick_type = 2
            # 2）如果headers中包含Proxy-Connection说明是匿名代理ip
            elif proxy_connection:
                nick_type = 1
            # 3）否则就是高匿代理ip
            else:
                nick_type = 0

            return True,nick_type,speed
        return False,nick_type,speed
    except Exception as e:
        # logger.exception(e)
        return False,nick_type,speed

if __name__ == '__main__':
    proxy = Proxy("150.255.131.139",port='9999')
    print(check_proxy(proxy))