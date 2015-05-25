# -*- coding: utf-8 -*-

# Scrapy settings for skinsales project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'urlgetter'

SPIDER_MODULES = ['urlgetter.spiders']
NEWSPIDER_MODULE = 'urlgetter.spiders'

ITEM_PIPELINES = {
    'urlgetter.pipelines.URLGetterPipeline': 300
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'skinsales (+http://www.yourdomain.com)'
