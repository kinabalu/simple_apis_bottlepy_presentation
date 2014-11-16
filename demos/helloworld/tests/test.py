from webtest import TestApp
import helloworld

def test_functional_helloworld():
    app = TestApp(helloworld.app)

    resp = app.get('/hello')
    assert resp.status == '200 OK'
    assert resp.text == 'Hello, World!'