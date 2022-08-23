import scrapy
from scrapy import FormRequest


class AuthSpiderSpider(scrapy.Spider):
    name = 'auth_spider'
    allowed_domains = ['scrapingclub.com']
    start_urls = ['https://scrapingclub.com/exercise/basic_login']

    def parse(self, response):
        csrf_token = response.xpath("//input[@name='csrfmiddlewaretoken']/@value").get()
        yield FormRequest.from_response(
            response,
            formxpath="//form",
            formdata={
                'name': 'scrapingclub',
                'password': 'scrapingclub',
                'csrfmiddlewaretoken': csrf_token
            },
            callback=self.after_login
        )

    def after_login(self, response):

        yield {
            'text': response.xpath("//div[contains(@class, 'mt-4')]/p/text()").get()
        }
