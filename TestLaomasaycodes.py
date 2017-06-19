#-*-coding=utf-8-*-
from Crawl2PDF.laomasaycodesCrawler import laomacodesCrawler
if __name__ == '__main__':
    start_url = "http://www.cnblogs.com/swiftma/p/5631311.html"
    crawler = laomacodesCrawler("laomacodes",start_url)
    crawler.run()