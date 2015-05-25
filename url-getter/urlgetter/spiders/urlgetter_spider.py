import scrapy
import re
from urlgetter.items import URLGetterItem

class URLGetterSpider(scrapy.Spider):
    name = "urlgetter"
    allowed_domains = ["leagueoflegends.com"]
    start_urls = [
        "http://na.leagueoflegends.com/en/news/store/sales",
    ]

    def parse(self, response):
        selectors = response.xpath('//a')
        items = []
        for selector in selectors:
            text = selector.xpath('text()').extract()
            if len(text) > 0:
                item = URLGetterItem()
                item['title'] = text[0]
                item['url'] = selector.xpath('@href').extract()[0]
                items.append(item)
        return items
