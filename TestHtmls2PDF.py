from Crawl2PDF.pdfbaseCrawler import Crawler
if __name__ == '__main__':
    start_url = "http://www.cnblogs.com/swiftma/p/5631311.html"
    crawl = Crawler("laomacodes",start_url)
    crawl.htmls2pdf2()