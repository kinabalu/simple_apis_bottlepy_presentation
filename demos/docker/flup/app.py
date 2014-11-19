from bottle import Bottle, run, request, response, abort
import json
import urllib
import requests


app = Bottle()


"""
# Modify this example so it uses mongo to save stocks data
import mongoengine as db

db.connect('stocks', host='192.168.59.103')

class Stock(db.Document):
    symbol = db.StringField(required=True)
    price = db.DecimalField(required=True, precision=2)

stock = Stock(symbol='AAPL', price=114.18)
stock.save()
"""
stocks = [
    {"symbol": "AAPL", "price": 114.18},
    {"symbol": "MSFT", "price": 49.58},
    {"symbol": "GOOG", "price": 544.40}
]

def _get_stocks_from_yql(stock_list):
    csv_stocks = '"' + ",".join(stock_list) + '"'

    url = 'https://query.yahooapis.com/v1/public/yql'
    data = urllib.quote_plus('select * from yahoo.finance.quotes where symbol in (' + csv_stocks + ')')
    data_url = url + '?q=' + data + '&env=http%3A%2F%2Fdatatables.org%2Falltables.env&format=json'

    r = requests.get(data_url)

    stocks_result = []
    if r.status_code == 200:
        j = r.json()
        total_returned = j['query']['count']
        for entry in j['query']['results']['quote']:
            stocks_result.append({
                'symbol': entry['symbol'],
                'price': entry['Ask']
            })

    return stocks_result


@app.route('/stocks', method='GET')
def list_stocks():
    for stock in Stock.objects:
        print stock

    result = dict()
    result['num_results'] = len(stocks)
    result['total_pages'] = 1
    result['page'] = 1
    result['objects'] = stocks

    response.content_type = 'application/json'    
    return json.dumps(result)

@app.route('/stocks', method='POST')
def add_stock():
    try:
        postdata = request.body.read()
        symbol_request = json.loads(postdata)
        stocks.append({"symbol": symbol_request['symbol'], "price": 75.42})
    except TypeError:
        abort(500, "Invalid content passed")

@app.route("/stocks", method="PUT")
@app.route("/stocks", method="PATCH")
@app.route("/stocks", method="DELETE")
def not_implemented():
  abort(405, "Method Not Allowed")

@app.route('/stocks/<symbol>', method='GET')
def get_stock(symbol='AAPL'):
    response.content_type = 'application/json'    

    for stock in stocks:
        if stock['symbol'] == symbol:
            return json.dumps(stock)
    abort(404, 'Stock not found')

@app.route('/stocks/<symbol>', method='DELETE')
def delete_stock(symbol='AAPL'):
    response.content_type = 'application/json'

    for idx, stock in enumerate(stocks):
        if stock['symbol'] == symbol:
            del stocks[idx]
            response.status = 200
            return ''
    abort(404, 'Stock not found')


if __name__ == '__main__':
    # expand this out with args so we can swap between flup and not, and init the mongo with initial data
    run(app, host='0.0.0.0', port=8000, server='flup')