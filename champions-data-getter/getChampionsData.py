from pymongo import MongoClient
import requests
import json
import sys

APITOKEN = ''
CHAMPIONS_ENDPOINT = 'https://na1.api.riotgames.com/lol/static-data/v3/champions?champData=image,skins&api_key=%s' % APITOKEN
client = MongoClient('localhost', 27017)
db = client['skinsales']
champions_collection = db['champions']

def retrieveChampData():
	print 'Retrieving data from Riot'
	data = requests.get(CHAMPIONS_ENDPOINT).content
	data = json.loads(data)
	version = data['version']
	old = champions_collection.find_one()
	if old and old['version'] == version:
		print 'Data already at latest version, exiting'
		sys.exit(0)
	champ_data = data['data']
	print 'There are %i champions' % len(champ_data)
	for champ in champ_data:
		parsed_data = {}
		parsed_data['name'] = champ_data[champ]['name']
		parsed_data['skins'] = champ_data[champ]['skins']
		parsed_data['index'] = champ
		parsed_data['version'] = version
		parsed_data['id'] = champ_data[champ]['id']
		champions_collection.update({'name': parsed_data['name']}, parsed_data, upsert=True)
	print 'Done'

if __name__ == '__main__':
	retrieveChampData()