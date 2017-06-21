'''
#pdfbaseCrawler pdf爬虫的基类
主要方法：
    crawl
    parse_menu
    parse_body
    download
    htmls2pdf
    control

'''
#-*-coding=utf-8-*-
import os
import shutil
import time
import pdfkit
import requests
from Crawl2PDF.config import OPTIONS

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
        self.path = name+"_files"
        self.pdfname = name+".pdf"
        self.htmls = []

    def crawl(self, url):
        """
        抓取器
        抓取url  (代理的切换,request.header,请求头等切换)
        :return:response 爬虫返回的response对象
        """
        response = requests.get(url)
        return response

    def parse_menu(self, response):
        """
        url管理
        解析目录结构,获取所有URL目录列表:由子类实现
        :param response 爬虫返回的response对象
        :return: url 可迭代对象(iterable) 列表,生成器,元组都可以
        """
        raise NotImplementedError

    def parse_body(self, response):
        """
        解析器
        解析正文,由子类实现
        :param response: 爬虫返回的response对象
        :return: 返回经过处理的html文本
        """
        raise NotImplementedError

    def download(self, htmlname, htmlcontent):
        """
        下载器
        下载到指定的目录下 self.path
        :param htmlname: html文本保存的名字
        :param htmlcontent: 爬虫返回的html文本
        """
        # 切换到文件夹中
        os.chdir(self.path)
        # 拼接 html文件名
        f_name = ".".join([htmlname, "html"])
        self.htmls.append(f_name)
        # 写入 文件中
        with open(f_name, 'wb') as f:
            f.write(htmlcontent)
        os.chdir("..")

    def htmls2pdf(self):
        """
        合成器
        将htmlpath中的html合并为pdf
        """
        pdfkit.from_file(self.htmls, self.pdfname, options=OPTIONS)

    def htmls2pdf2(self):
        """
        合成器 自定义htmlname比较方式
        将htmlpath中的html合并为pdf
        """
        htmls = os.listdir(self.path)
        shtmls = sorted(htmls, key=lambda x: int(x.split('.')[0]))
        print(os.getcwd())
        os.chdir(self.path)
        print(os.getcwd())
        pdfkit.from_file(shtmls, self.pdfname, options=OPTIONS)

    def run(self):
        '''
        1.抓取页面保存为html
        2.把html合并为pdf
        '''
        # 文件夹是否存在 文件夹存在就删除
        if os.path.exists(self.path):
            shutil.rmtree(self.path)
        # 创建下载目录文件夹
        os.mkdir(self.path)
        start = time.time()
        for index, url in enumerate(self.parse_menu(self.crawl(self.start_url))):
            html = self.parse_body(self.crawl(url))
            f_name = str(index)
            self.download(f_name, html)
        self.htmls2pdf2()
        total_time = time.time() - start
        print(u"总共耗时：%f 秒" % total_time)

    def run2(self):
        '''
        1.抓取页面保存为html
        2.把html合并为pdf
        '''
        # 文件夹是否存在 文件夹存在就删除
        if os.path.exists(self.path):
            shutil.rmtree(self.path)
        # 创建下载目录文件夹
        os.mkdir(self.path)
        start = time.time()
        for index,url in enumerate(self.parse_menu(self.crawl(self.start_url))):
            f_name,html = self.parse_body(self.crawl(url))
            self.download(f_name, html)
        self.htmls2pdf2()
        total_time = time.time() - start
        print(u"总共耗时：%f 秒" % total_time)
