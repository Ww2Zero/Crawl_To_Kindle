#-*-coding=utf-8-*-
import logging
from bs4 import BeautifulSoup
from Crawl2PDF.config import HTML_TEMPLATE
from Crawl2PDF.pdfbaseCrawler import Crawler


class javaquestionCrawler(Crawler):
    """
    java千百问
    http://blog.csdn.net/ooppookid/article/category/6211626
    """

    def parse_menu(self, response):
        """
        解析目录结构,获取所有URL目录列表
        :param response 爬虫返回的response对象
        :return: url生成器
        """
        soup = BeautifulSoup(response.content, "html.parser")
        post_list = soup.find(class_="list")
        post_body = post_list.find_all(class_='link_title')
        for li in post_body:
            turl = li.find('a').get("href")
            url = 'http://blog.csdn.net'+turl
            print(url)
            yield url

    def parse_body(self, response):
        """
          解析正文
          :param response: 爬虫返回的response对象
          :return: 返回处理后的html文本
          """
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            body = soup.select("#article_content")
            # print(body)
            # print(type(body))
            # 加入标题, 居中显示
            title = soup.find(class_='link_title').get_text()
            center_tag = soup.new_tag("center")
            title_tag = soup.new_tag('h1')
            title_tag.string = title
            center_tag.insert(0, title_tag)
            body.insert(0, center_tag)
            html = str(body)
            html = HTML_TEMPLATE.format(content=html)
            html = html.encode("utf-8")
            # 文件为：         Java千百问_01基本概念（003）_J2EE里面的2是什么意思            
            # 文件名提取为    3
            htmlname = str(int(str(title).strip().split('（')[1].split('）')[0]))
            return htmlname,html

        except Exception as e:
            logging.error("解析错误", exc_info=True)
