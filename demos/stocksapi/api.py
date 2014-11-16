from bottle import Bottle, run, response
import json

app = Bottle()

stocks = [
    {"symbol": "AAPL", "price": 114.18},
    {"symbol": "MSFT", "price": 49.58},
    {"symbol": "GOOG", "price": 544.40}
]

@app.route('/stocks', method='GET')
def list_stocks():
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


if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)