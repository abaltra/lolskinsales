from flask import Flask
from flask import jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client['skinsales']
sales_collection = db['sales']

@app.route('/skins', methods=['GET'])
def allSkins():
	sales = list(sales_collection.find())
	for sale in sales:
		del sale['_id']
	return json.dumps(sales)

@app.route('/skins/championName/<string:champ_name>', methods=['GET'])
def skinsByName(champ_name):
	sale = sales_collection.find_one({'champion_name': champ_name})
	if sale is None:
		return json.dumps({'error': 'Champion not found'}), 404
	del sale['_id']
	return json.dumps(sale)

@app.route('/skins/championId/<int:champ_id>', methods=['GET'])
def skinsById(champ_id):
	sale = sales_collection.find_one({'champion_id': champ_id})
	if sale is None:
		return json.dumps({'error': 'Champion not found'}), 404
	del sale['_id']
	return json.dumps(sale)

if __name__ == '__main__':
    app.run(debug=True)