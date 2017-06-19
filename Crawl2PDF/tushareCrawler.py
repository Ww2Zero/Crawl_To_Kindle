#-*-coding=utf-8-*-
import logging

from bs4 import BeautifulSoup

from Crawl2PDF.config import HTML_TEMPLATE
from Crawl2PDF.pdfbaseCrawler import Crawler


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
            html = HTML_TEMPLATE.format(content=html)
            html = html.encode("utf-8")
            return html
        except Exception as e:
            logging.error("解析错误", exc_info=True)
