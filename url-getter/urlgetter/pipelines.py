# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem
import re

class URLGetterPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""

    # put all words in lowercase
    f = re.compile('Champion and skin sale: .+')
    found = False

    def process_item(self, item, spider):
        if self.found:
            raise DropItem('Latest URL already found')
        elif not self.f.match(item['title']):
            raise DropItem("Not useful URL: %s" % item['url'])
        else:
            self.found = True
            item['start_date'], _, item['end_date'] = item['title'][-13:].split(' ')
            return item
