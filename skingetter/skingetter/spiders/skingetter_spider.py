import scrapy
import re
from skingetter.items import SkinGetterItem
import json
from pymongo import MongoClient
import time
from datetime import date

class SkinGetterSpider(scrapy.Spider):
    name = "skingetter"
    allowed_domains = ["leagueoflegends.com"]
    client = MongoClient('localhost', 27017)
    db = client['skinsales']
    champions_collection = db['champions']
    sales_collection = db['sales']
    sales_history_collection = db['sales_history']
    SPLASH_URL = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/'
    LOADING_URL = 'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/'
    sales_data = None

    def __init__(self, file_path=''):
        with open(file_path) as data:
            d = json.load(data)[0]
            self.start_urls = ["http://na.leagueoflegends.com/%s" % d['url']]
            self.sales_data = d

    def parse(self, response):
        data = re.findall("<h4>(.+?)</h4>\\n<p><strike style=\"color: #777777\">([0-9]+)</strike>\s+([0-9]+)\s+RP</p>", response.body)
        items = []
        final_items = []
        for datum in data:
            item = {}
            champion_data = self.champions_collection.find_one({"skins.name": {"$in": [datum[0]]}})
            item['skin_name'] = datum[0]
            item['old_price'] = datum[1]
            item['new_price'] = datum[2]
            item['champion_name'] = champion_data['name']
            item['champion_id'] = champion_data['id']
            item['start_date'] = str(self.sales_data['start_date']) + '.' + str(date.today().year + 1)
            item['end_date'] = str(self.sales_data['end_date']) + '.' + str(date.today().year + 1)
            for skin in champion_data['skins']:
                if skin['name'] == item['skin_name']:
                    item['skin_splash_url'] = "%s%s_%s.jpg" % (self.SPLASH_URL, champion_data['index'], skin['num'])
                    item['skin_loading_url'] = "%s%s_%s.jpg" % (self.LOADING_URL, champion_data['index'], skin['num'])
            items.append(item)

        self.sales_collection.delete_many({}) #Clear current sales
        [self.sales_collection.insert_one(item) for item in items] #Save current sales
