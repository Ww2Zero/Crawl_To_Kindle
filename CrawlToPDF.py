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


class LiaoxuefengPythonCrawler(Crawler):
    """
    廖雪峰Python3教程
    """

    def parse_menu(self, response):
        """
        解析目录结构,获取所有URL目录列表
        :param response 爬虫返回的response对象
        :return: url生成器
        """
        soup = BeautifulSoup(response.content, "html.parser")
        menu_tag = soup.find_all(class_="uk-nav uk-nav-side")[1]
        for li in menu_tag.find_all("li"):
            url = li.a.get("href")
            if not url.startswith("http"):
                url = "".join([self.domain, url])  # 补全为全路径
            yield url

    def parse_body(self, response):
        """
        解析正文
        :param response: 爬虫返回的response对象
        :return: 返回处理后的html文本
        """
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            body = soup.find_all(class_="x-wiki-content")[0]

            # 加入标题, 居中显示
            title = soup.find('h4').get_text()
            center_tag = soup.new_tag("center")
            title_tag = soup.new_tag('h1')
            title_tag.string = title
            center_tag.insert(1, title_tag)
            body.insert(1, center_tag)

            html = str(body)
            # body中的img标签的src相对路径的改成绝对路径
            pattern = "(<img .*?src=\")(.*?)(\")"

            def func(m):
                if not m.group(3).startswith("http"):
                    rtn = "".join(
                        [m.group(1), self.domain, m.group(2), m.group(3)])
                    return rtn
                else:
                    return "".join([m.group(1), m.group(2), m.group(3)])

            html = re.compile(pattern).sub(func, html)
            html = config.HTML_TEMPLATE.format(content=html)
            html = html.encode("utf-8")
            return html
        except Exception as e:
            logging.error("解析错误", exc_info=True)


class laomasaycodesCrawler(Crawler):
    """
    老马说编程 博客园文章
    http://www.cnblogs.com/swiftma/p/5631311.html
    """

    def parse_menu(self, response):
        """
        解析目录结构,获取所有URL目录列表
        :param response 爬虫返回的response对象
        :return: url生成器
        """
        soup = BeautifulSoup(response.content, "html.parser")
        post_body = soup.select('#cnblogs_post_body')[0]
        alist = post_body.find_all("a")
        for li in alist:
            url = li.get("href")
            yield url

    def parse_body(self, response):
        """
          解析正文
          :param response: 爬虫返回的response对象
          :return: 返回处理后的html文本
          """
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            body = soup.select('#cnblogs_post_body')[0]
            # print(body)
            # print(type(body))
            # 加入标题, 居中显示
            title = soup.select('.postTitle2')[0].get_text()
            center_tag = soup.new_tag("center")
            title_tag = soup.new_tag('h1')
            title_tag.string = title
            center_tag.insert(1, title_tag)
            body.insert(0, center_tag)
            body = str(body)
            # 去除文章末尾的微信公众号 二维码
            startdelflag = body.find("-------")
            html = body[0:startdelflag]
            html = html +"</p></div>"
            html = config.HTML_TEMPLATE.format(content=html)
            html = html.encode("utf-8")
            return html

        except Exception as e:
            logging.error("解析错误", exc_info=True)


class tushareCrawler(Crawler):
    '''
    tushare doc
    http://tushare.waditu.com/index.html
    '''
    def parse_menu(self, response):
        """
        解析目录结构,获取所有URL目录列表
        :param response 爬虫返回的response对象
        :return: url生成器
        """
        soup = BeautifulSoup(response.content, "html.parser")
        menu_tag = soup.find("ul", "current").find_all("a")
        for li in menu_tag:
            if str(li).find("#") < 0:
                print(li)
                url = "/" + str(li).split('"')[3]
                url = "".join([self.domain, url])  # 补全为全路径
                yield url

    def parse_body(self, response):
        """
        解析正文
        :param response: 爬虫返回的response对象
        :return: 返回处理后的html文本
        """
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            body = soup.select('.body')[0]
            html = str(body)
            # body中的img标签的src相对路径的改成绝对路径
            html = html.replace('src="', 'src="http://tushare.org/')
            html = config.HTML_TEMPLATE.format(content=html)
            html = html.encode("utf-8")
            return html
        except Exception as e:
            logging.error("解析错误", exc_info=True)

if __name__ == '__main__':
    # start_url = "http://tushare.org/index.html"
    # crawler = tushareCrawler("tushare", start_url)
    # crawler.run()

    start_url = "http://www.cnblogs.com/swiftma/p/5631311.html"
    crawler = laomasaycodesCrawler("laomacodes",start_url)
    crawler.run()
