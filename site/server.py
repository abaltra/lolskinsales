from flask import Flask
from flask import jsonify
from flask import render_template
import requests
import json

app = Flask(__name__)

@app.route('/riot.txt', methods=['GET'])
def rito():
        return 'dab449dc-e90e-4f12-846a-8a44bf284da1'

@app.route('/', methods=['GET'])
def index():
        data = requests.get('http://localhost:5000').content
        data = json.loads(data)
        return render_template('index.html',
                data=data)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
