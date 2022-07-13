# -8- coding = utf-8 -*-
# @Time : 2021/4/18 23:40
# @Author : 大漠孤烟
# @File : test.py
# @Software : PyCharm

import requests
from lxml import etree

# dict = {'id':1,'ip':2}
# print(dict.pop('id'))
# print(dict)
# url = 'https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-2'
# url = 'https://ip.jiangxianli.com/?page=1'
url = 'https://www.89ip.cn/index_1.html'
# url = 'http://www.66ip.cn/index.html'
page_response = requests.get(url)
# print(page_response.status_code)
page_text = page_response.text
# print(page_text)

element = etree.HTML(page_text)
# trs = element.xpath('//*[@id="main"]/div[1]/div[2]/div[1]/table/tr[position()>1]')
# trs = element.xpath('//*[@id="page"]/table[2]/tr[position()>2]')
# trs = element.xpath('/html/body/div[1]/div[2]/div[1]/div[1]/table/tbody/tr')
# trs = element.xpath('//div[1]/div/div[1]/table/tbody/tr[1]')
trs = element.xpath('//*[@class="layui-col-md8"]/div/div[1]/table/tbody/tr')
for tr in trs:
    ip_port = tr.xpath('./td[1]/text()')
    area = tr.xpath('./td[3]/text()')
    # ip_port = list(tr.xpath('./td[1]/text()')[0].split(':')[0])
    # print(ip_port)
    # ip_port = "".join(ip_port)
    print(ip_port, area)

    # ip_port = tr.xpath('./td[1]/text()')[0]
    # ip,port = ip_port.split(':')
    # print(ip,port)
    # break

# import schedule
# import time
#
#
# # 测试schedule
# def task():
#     print("呵呵。。")
#
#
# schedule.every(2).seconds.do(task)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
