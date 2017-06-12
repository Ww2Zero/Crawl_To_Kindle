#-*-coding=utf-8-*-
import logging
from bs4 import BeautifulSoup
from config import HTML_TEMPLATE
from pdfCrawler import Crawler


class laomacodesCrawler(Crawler):
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
            html = HTML_TEMPLATE.format(content=html)
            html = html.encode("utf-8")
            return html

        except Exception as e:
            logging.error("解析错误", exc_info=True)
