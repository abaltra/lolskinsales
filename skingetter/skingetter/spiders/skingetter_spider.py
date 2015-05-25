import scrapy
import re
from skingetter.items import SkinGetterItem
import json
from pymongo import MongoClient
import time

class SkinGetterSpider(scrapy.Spider):
    name = "skingetter"
    allowed_domains = ["leagueoflegends.com"]
    client = MongoClient('localhost', 27017)
    db = client['skinsales']
    champions_collection = db['champions']
    sales_collection = db['sales']
    SPLASH_URL = 'http://ddragon.leagueoflegends.com/cdn/img/champion/splash/'
    LOADING_URL = 'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/'
    sales_data = None

    def __init__(self, file_path=''):
        with open(file_path) as data:
            d = json.load(data)[0]
            self.start_urls = ["http://na.leagueoflegends.com/%s" % d['url']]
            self.sales_data = d

    def parse(self, response):
        data = re.findall("<h4>(.+?)</h4>\\n<strike .+?>([0-9]+)</strike> ([0-9]+)", response.body)
        items = []
        final_items = []
        self.sales_collection.delete_many({})
        for datum in data:
            item = {}
            item['skin_name'] = datum[0]
            item['old_price'] = datum[1]
            item['new_price'] = datum[2]
            champion_data = self.champions_collection.find_one({"skins.name": {"$in": [item['skin_name']]}})
            for skin in champion_data['skins']:
                if skin['name'] == item['skin_name']:
                    item['skin_splash_url'] = "%s%s_%s.jpg" % (self.SPLASH_URL, champion_data['index'], skin['num'])
                    item['skin_loading_url'] = "%s%s_%s.jpg" % (self.LOADING_URL, champion_data['index'], skin['num'])
                    item['champion_name'] = champion_data['name']
                    item['champion_id'] = champion_data['id']
                    item['start_date'] = self.sales_data['start_date']
                    item['end_date'] = self.sales_data['end_date']
                    self.sales_collection.insert_one(item) 
            items.append(item)     
