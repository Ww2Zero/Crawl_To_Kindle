#-*-coding=utf-8-*-
import logging
import re
from bs4 import BeautifulSoup
from Crawl_TO_PDF.config import HTML_TEMPLATE
from Crawl_TO_PDF.pdfbaseCrawler import Crawler


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
            html = HTML_TEMPLATE.format(content=html)
            html = html.encode("utf-8")
            return html
        except Exception as e:
            logging.error("解析错误", exc_info=True)
