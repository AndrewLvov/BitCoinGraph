import sys
import json
import requests

from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    ctx = {

    }
    return render_template("index.html", **ctx)

@app.route('/data/')
def data_view():
    response = requests.get('http://api.bitcoincharts.com/v1/markets.json')
    if response.status_code != 200:
        sys.exit(1)

    try:
        data = json.loads(response.content.decode('utf-8'))

        currency_data = []
        index = 0
        for d in data:
            if d['currency'] == 'USD' and \
                    d['bid'] is not None and \
                    d['ask'] is not None:
                currency_data.append({
                    'index': index,
                    'bid': d['bid'],
                    'ask': d['ask'],
                })
                index += 1

    except ValueError:
        print('Failed parsing response')
        currency_data = []

    return jsonify(data=currency_data, my=[])

    # "{ 'data': [{'value': 0, 'close': 300}, {'value': 1, 'close': 335}], 'my': [] }"


if __name__ == '__main__':
    app.debug = True
    app.run()
