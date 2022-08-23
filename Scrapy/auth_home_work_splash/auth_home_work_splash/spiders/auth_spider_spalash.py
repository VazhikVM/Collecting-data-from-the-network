import scrapy
from scrapy_splash import SplashRequest, SplashFormRequest


class AuthSpiderSpalashSpider(scrapy.Spider):
    name = 'auth_spider_spalash'
    allowed_domains = ['scrapingclub.com']
    # start_urls = ['https://scrapingclub.com/']

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
            url='https://scrapingclub.com/exercise/basic_login',
            callback=self.parse,
            endpoint='execute',
            args={'lua_source': self.script}
        )

    def parse(self, response):
        csrf_token = response.xpath("//input[@name='csrfmiddlewaretoken']/@value").get()

        yield SplashFormRequest.from_response(
            response,
            formxpath="//form",
            formdata={
                'name': 'scrapingclub',
                'password': 'scrapingclub',
                'csrfmiddlewaretoken': csrf_token
            },
            callback=self.after_login,

        )

    def after_login(self, response):
        yield {
            'text': response.xpath("//div[contains(@class, 'mt-4')]/p/text()").get()
        }

