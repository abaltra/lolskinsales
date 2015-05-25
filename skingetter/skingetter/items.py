# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SkinGetterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    skin_name = scrapy.Field()
    old_price = scrapy.Field()
    new_price = scrapy.Field()
    skin_splash_url = scrapy.Field()
    skin_loading_url = scrapy.Field()
