# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class URLGetterItem(scrapy.Item):
	url = scrapy.Field()
	title = scrapy.Field()
	start_date = scrapy.Field()
	end_date = scrapy.Field()