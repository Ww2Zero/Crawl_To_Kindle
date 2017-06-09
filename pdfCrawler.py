#-*-coding=utf-8-*-
import logging
import os
import re
import time

try:
    from urllib.parse import urlparse  # py3
except:
    from urlparse import urlparse  # py2

import pdfkit
import requests
from bs4 import BeautifulSoup

import config

class Crawler(object):
    """
    爬虫基类，所有爬虫都应该继承此类
    """
    name = None

    def __init__(self, name, start_url):
        """
        初始化
        :param name: 保存问的PDF文件名,不需要后缀名
        :param start_url: 爬虫入口URL
        """
        self.name = name
        self.start_url = start_url
        self.domain = '{uri.scheme}://{uri.netloc}'.format(
            uri=urlparse(self.start_url))

    def crawl(self, url):
        """
        抓取url
        :return:response 爬虫返回的response对象
        """
        response = requests.get(url)
        return response

    def parse_menu(self, response):
        """
        解析目录结构,获取所有URL目录列表:由子类实现
        :param response 爬虫返回的response对象
        :return: url 可迭代对象(iterable) 列表,生成器,元组都可以
        """
        raise NotImplementedError

    def parse_body(self, response):
        """
        解析正文,由子类实现
        :param response: 爬虫返回的response对象
        :return: 返回经过处理的html文本
        """
        raise NotImplementedError

    def run(self):
        start = time.time()
        
        htmls = []
        for index, url in enumerate(self.parse_menu(self.crawl(self.start_url))):
            html = self.parse_body(self.crawl(url))
            f_name = ".".join([str(index), "html"])
            with open(f_name, 'wb') as f:
                f.write(html)
            htmls.append(f_name)

        pdfkit.from_file(htmls, self.name + ".pdf", options=config.OPTIONS)
        for html in htmls:
            os.remove(html)
        total_time = time.time() - start
        print(u"总共耗时：%f 秒" % total_time)

