from bottle import Bottle, run

app = Bottle()

@app.route('/hello')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    run(app, host='localhost', port=8081, debug=True)