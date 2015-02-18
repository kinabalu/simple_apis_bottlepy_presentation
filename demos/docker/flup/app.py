from bottle import Bottle, run, request, response, abort
import json
import urllib
import requests
from pymongo import MongoClient
from pymongo.errors import InvalidId
from bson import BSON
from bson import json_util
from bson.objectid import ObjectId

app = Bottle()
client = MongoClient('mongodb://mongo:27017')
db = client.stocks

@app.route('/stocks', method='GET')
def list_stocks():
    stocks = []
    for stock in db.stocks.find():
        stocks.append({
            "symbol": stock['symbol'],
            "price": stock['price']
        })

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
        db.stocks.save({"symbol": symbol_request['symbol'], "price": 0.00})
    except TypeError:
        abort(500, "Invalid content passed")

"""
@app.route("/stocks", method="PUT")
@app.route("/stocks", method="PATCH")
@app.route("/stocks", method="DELETE")
def not_implemented():
  abort(405, "Method Not Allowed")
"""

@app.route('/stocks/<symbol>', method='GET')
def get_stock(symbol):
    response.content_type = 'application/json'    

    stock = db.stocks.find_one({"symbol": symbol})

    if stock is None:
        abort(404, 'Stock not found')

    return json.dumps({"symbol": symbol, "price": stock['price']})

@app.route('/stocks/<symbol>', method='DELETE')
def delete_stock(symbol):
    response.content_type = 'application/json'

    ref_stock = db.stocks.find_one({"symbol": symbol})

    if ref_stock is None:
        abort(404)
        return

    db.stocks.remove({"symbol": symbol});
    return ''


if __name__ == '__main__':
    # expand this out with args so we can swap between flup and not, and init the mongo with initial data
    run(app, host='0.0.0.0', port=8000, server='flup')