#-*-coding=utf-8-*-
from laomasaycodesCrawler import laomasaycodesCrawler

if __name__ == '__main__':
    # start_url = "http://tushare.org/index.html"
    # crawler = tushareCrawler("tushare", start_url)
    # crawler.run()

    start_url = "http://www.cnblogs.com/swiftma/p/5631311.html"
    crawler = laomasaycodesCrawler("laomacodes",start_url)
    crawler.run()