from webtest import TestApp
import api
import json

def test_functional_stocks_get():
    app = TestApp(api.app)

    resp = app.get('/stocks')
    assert resp.status == '200 OK'

    json_text = json.loads(resp.text)
    print json_text
    assert false == true

    # assert resp.text == 'Hello, World!'