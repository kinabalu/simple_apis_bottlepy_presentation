from pymongo import MongoClient
from pymongo.errors import InvalidId
import json
import StringIO
from bson import BSON
from bson import json_util
from bson.objectid import ObjectId

client = MongoClient('mongodb://boot2docker:27017/')
db = client.stocks

def main():
    db.stocks.save({"symbol": "AAPL", "price": 114.18})
    db.stocks.save({"symbol": "MSFT", "price": 49.58})
    db.stocks.save({"symbol": "GOOG", "price": 544.40})

if __name__ == '__main__':
    main()
