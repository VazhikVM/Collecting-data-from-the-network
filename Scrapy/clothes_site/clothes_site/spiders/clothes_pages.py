import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ClothesPagesSpider(CrawlSpider):
    name = 'clothes_pages'
    allowed_domains = ['scrapingclub.com']
    start_urls = ['http://scrapingclub.com/exercise/list_basic/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=r"//h4[@class='card-title']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=r"//li[@class='page-item']/a[contains(text(), 'Next')]"), follow=True),
    )

    def parse_item(self, response):
        item = {}
        item['title'] = response.xpath('//div[@class="card-body"]/h3/text()').get()
        item['price'] = response.xpath('//div[@class="card-body"]/h4/text()').get()
        item['description'] = response.xpath('//div[@class="card-body"]/p/text()').get()
        item['img'] = response.urljoin(response.xpath('//img[contains(@class, "card-img-top")]/@src').get())
        return item
