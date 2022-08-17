import scrapy


class ClothesSpider(scrapy.Spider):
    name = 'clothes'
    allowed_domains = ['scrapingclub.com']
    start_urls = ['http://scrapingclub.com/exercise/list_basic/']

    def parse(self, response):
        cards = response.xpath("//div[@class='card']")

        for card in cards:
            yield {
                'href': response.urljoin(card.xpath(".//a/@href").get()),
                'img': response.urljoin(card.xpath(".//a/img/@src").get()),
                'title': card.xpath(".//h4[@class='card-title']/a/text()").get(),
                'price': card.xpath(".//div[@class='card-body']/h5/text()").get()
            }

        next_page = response.xpath("//li[@class='page-item']/a[contains(text(), 'Next')]/@href").get()

        if next_page:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)


