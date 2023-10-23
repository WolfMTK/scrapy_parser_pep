import scrapy


class PepParseItem(scrapy.Item):
    status = scrapy.Field()
    number = scrapy.Field()
    name = scrapy.Field()
