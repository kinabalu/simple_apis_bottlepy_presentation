from bottle import Bottle, run, request, response, abort
import mongoengine as db
import json
import urllib
import requests
import argparse

app = Bottle()


class Stock(db.Document):
    symbol = db.StringField(required=True)
    price = db.DecimalField(required=True, precision=2)


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
    objects = []
    for stock in Stock.objects:
        objects.append({"symbol": stock.symbol, "price": float(stock.price)})

    result = dict()
    # example metadata to send along with dataset
    result['num_results'] = len(objects)
    result['total_pages'] = 1
    result['page'] = 1
    result['objects'] = objects

    return result

@app.route('/stocks', method='POST')
def add_stock():
    try:
        postdata = request.body.read()
        symbol_request = json.loads(postdata)

        stock_qs = Stock.objects(symbol=symbol_request['symbol'])

        if stock_qs:
            abort(404, "Find a better way of saying this, but you failed dude")
            return

        # TODO grab stock price with YQL here?
        stock = Stock(symbol=symbol_request['symbol'], price=114.18)
        stock.save()
    except TypeError:
        abort(500, "Invalid content passed")

@app.route("/stocks", method="PUT")
@app.route("/stocks", method="PATCH")
@app.route("/stocks", method="DELETE")
def not_implemented():
  abort(405, "Method Not Allowed")

# Member REST methods
@app.route('/stocks/<symbol>', method='GET')
def get_stock(symbol):

    stock_qs = Stock.objects(symbol=symbol)

    if stock_qs:
        stock = stock_qs.get()
        return {"symbol": stock.symbol, "price": float(stock.price)}

    abort(404, 'Stock not found')

@app.route('/stocks/<symbol>', method='DELETE')
def delete_stock(symbol):

    for stock in Stock.objects:
        if stock.symbol == symbol:
            stock.delete()
            response.status = 200
            return ''
    abort(404, 'Stock not found')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='stocksapi')

    parser.add_argument(
        "--fcgi",
        dest="use_fcgi",
        action="store_true",
        help="Use fcgi rather than wsgi"
    )
    parser.add_argument(
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="Debug mode"
    )
    parser.add_argument(
        "-p",
        dest="port",
        type=int,
        default=8080,
        help="http port"
    )

    parser.add_argument(
        "--mongo-host",
        dest="mongo_host",
        type=str,
        default="mongo",
        help="mongo server"
    )

    parser.add_argument(
        "--host",
        dest="host",
        type=str,
        default="localhost",
        help="http server"
    )


    args = parser.parse_args()

    db.connect('stocks', host=args.mongo_host)

    if args.use_fcgi:
        run(app, host=args.host, port=args.port, debug=args.debug, server='flup')
    else:
        run(app, host=args.host, port=args.port, debug=args.debug)
    