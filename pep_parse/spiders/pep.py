import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        pattern = (
            '//section[@id="numerical-index"]'
            '//a[@class="pep reference internal"]/@href'
        )
        for pep in response.xpath(pattern).getall():
            yield response.follow(pep, callback=self.parse_pep)

    def parse_pep(self, response):
        title = response.css('h1.page-title::text').get().split()
        data = {
            'status': response.css('abbr::text').get(),
            'number': title[1],
            'name': ' '.join(title[3:])
        }
        yield PepParseItem(data)
