import time 
import requests
import urllib
from pymongo import MongoClient
from pymongo.errors import InvalidId
from bson import BSON
from bson import json_util
from bson.objectid import ObjectId

client = MongoClient('mongodb://boot2docker:27017')
db = client.stocks

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
                'price': float(entry['Ask'])
            })

    return stocks_result

def _get_list_of_stocks():
    stocks = []
    for stock in db.stocks.find():
        stocks.append(stock['symbol'])

    return stocks

def update_stocks():
    stocks = _get_list_of_stocks()
    updated_result = _get_stocks_from_yql(stocks)

    for stock in updated_result:
        referenced_stock = db.stocks.find_one({"symbol": stock['symbol']})
        old_price = referenced_stock['price']
        referenced_stock['price'] = float(stock['price'])
        db.stocks.save(referenced_stock)
        print 'Symbol: %s [old: %.2f, new: %.2f]' % (stock['symbol'], old_price, stock['price'])
    print '---'

def main():
    while True:
        update_stocks()
        time.sleep(60)

if __name__ == '__main__':
    main()
