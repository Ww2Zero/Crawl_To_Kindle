#-*-coding=utf-8-*-
from Crawl2PDF.javaquestion import javaquestionCrawler
if __name__ == '__main__':
    start_url = "http://blog.csdn.net/ooppookid/article/category/6211626"
    crawler = javaquestionCrawler("javaq",start_url)
    crawler.run2()