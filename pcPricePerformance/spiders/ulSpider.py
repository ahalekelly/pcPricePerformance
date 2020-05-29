import scrapy
from pcPricePerformance.items import ulItem

class ulCPUSpider(scrapy.Spider):
    name = "ulCPU"

    def start_requests(self):
        urls = ['https://benchmarks.ul.com/compare/best-cpus?amount=0&sortBy=SCORE&reverseOrder=true&types=DESKTOP&minRating=0']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for selector in response.xpath("//tbody/tr"):
            print(selector)
            item = ulItem()
            item["model"] = selector.xpath("td/a/node()").extract_first()
            item["performance"] = int(selector.xpath("td/div[@class='bar-holder performance']/div/span/node()").extract_first())
            item["popularity"] = float(selector.xpath("td/div[@class='bar-holder secondary']/div/span/node()").extract_first())
            yield item

class ulGPUSpider(scrapy.Spider):
    name = "ulGPU"

    def start_requests(self):
        urls = ['https://benchmarks.ul.com/compare/best-gpus?amount=0&sortBy=SCORE&reverseOrder=true&types=DESKTOP&minRating=1']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for selector in response.xpath("//tbody/tr"):
            print(selector)
            item = ulItem()
            item["model"] = selector.xpath("td/a/node()").extract_first()
            item["performance"] = int(selector.xpath("td/div[@class='bar-holder performance']/div/span/node()").extract_first())
            item["popularity"] = float(selector.xpath("td/div[@class='bar-holder secondary']/div/span/node()").extract_first())
            yield item
