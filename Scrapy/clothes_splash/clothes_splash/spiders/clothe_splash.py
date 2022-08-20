import scrapy
from scrapy_splash import SplashRequest


class ClotheSplashSpider(scrapy.Spider):
    name = 'clothe_splash'
    allowed_domains = ['scrapingclub.com']
    # start_urls = ['https://scrapingclub.com/exercise/detail_sign/']

    script = '''
        function main(splash, args)
          assert(splash:go(args.url))
          assert(splash:wait(0.5))
          return {
            html = splash:html(),
          }
        end
    '''

    def start_requests(self):
        yield SplashRequest(
            url='https://scrapingclub.com/exercise/detail_sign/',
            callback=self.parse,
            endpoint='execute',
            args={'lua_source': self.script}
        )

    def parse(self, response):
        yield {
            'title': response.xpath("//h4[@class='card-title']/text()").get(),
            'img': response.urljoin(response.xpath('//img[contains(@class, "card-img-top")]/@src').get()),
            'price': response.xpath("//h4[@class='card-price']/text()").get(),
            'desc': response.xpath("//p[@class='card-description']/text()").get(),
        }
