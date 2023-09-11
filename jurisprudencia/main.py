from scrapy.crawler import CrawlerProcess
from jurisprudencia.spiders import BJNSpider, LocalSpider


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(LocalSpider)
    process.start()
