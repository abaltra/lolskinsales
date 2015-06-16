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
        data = re.findall("<h4>(.+?)</h4>\\n<strike .+?>([0-9]+)</strike> ([0-9]+)", response.body)
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

        current_saved_sales = list(self.sales_collection.find({}))

        found_counter = 0
        for i in xrange(0, len(current_saved_sales)):
            for j in xrange(0, len(items)):
                if items[j - 1]['champion_id'] == current_saved_sales[i]['champion_id'] and items[j]['start_date'] == current_saved_sales[i]['start_date'] and items[j]['end_date'] == current_saved_sales[i]['end_date']:
                    found_counter += 1

        print "Found counter: %i, items: %i" % (found_counter, len(items))

        if found_counter == len(items):
            #Sales are the same as before, do nothing
            print "DOing nothing"
            pass
        else:
            print "updating"
            [self.sales_history_collection.insert_one(item) for item in current_saved_sales] #Move sales to history
            self.sales_collection.delete_many({}) #Clear current sales
            [self.sales_collection.insert_one(item) for item in items] #Save current sales
