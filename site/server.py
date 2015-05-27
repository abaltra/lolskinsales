from flask import Flask
from flask import jsonify
from flask import render_template
import requests
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	data = requests.get('http://localhost:5000/skins').content
	data = json.loads(data)
	return render_template('index.html',
		data=data)


if __name__ == '__main__':
    app.run(debug=True, port=5001)