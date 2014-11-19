from bottle import Bottle, run, response, request, abort
import json, uuid

app = Bottle()

talks = [
    {
      "id": 1,
      "name": "AngularJS and Flask sitting in a tree",
      "speaker": "Andrew Lombardi",
      "technology": "JavaScript, Python",
      "description": "An awesome talk about the JavaScript framework AngularJS and using it with Flask to build a RESTful service",
      "time": {
        "begin_time": "14:25",
        "end_time": "15:10"
      },
      "date": "2014-11-18"
    },
    {
      "id": 2,
      "name": "Simple API's with bottle.py",
      "speaker": "Andrew Lombardi",
      "technology": "Python",
      "description": "An awesome talk",
      "time": {
        "begin_time": "14:25",
        "end_time": "15:10"
      },
      "date": "2014-11-19"
    }
]

# the decorator
def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors

def _get_talk(id):
    for talk in talks:
        if str(talk['id']) == str(id):
            return talk
    return None

def _get_talk_index(id):
    for idx, talk in enumerate(talks):
        if str(talk['id']) == str(id):
            return idx
    return -1

@app.route('/api/talks/<id>', method='GET')
@enable_cors
def get_talk(id):
    response.content_type = 'application/json'
    referenced_talk = _get_talk(id)
    if not referenced_talk:
        abort(404)
        return
    else:
        return referenced_talk

@app.route('/api/talks/<id>', method='PUT')
@enable_cors
def updateTalk(id):
    response.content_type = 'application/json'
    referenced_talk_idx = _get_talk_index(id)
    if referenced_talk_idx == -1:
        abort(404)
        return

    json_data = json.loads(request.data)
    json_data['id'] = id                # just to ensure we have the right stuff
    talks[referenced_talk_idx] = json_data
    return json_data

@app.route('/api/talks/<id>', method='POST')
@app.route('/api/talks/<id>', method='PATCH')
def not_implemented():
    abort(405, "Method Not Allowed")

@app.route('/api/talks/<id>', method='DELETE')
@enable_cors
def delete_talk(id):
    referenced_talk_idx = _get_talk_index(id)
    if referenced_talk_idx == -1:
        abort(404)
        return
    else:
        del talks[referenced_talk_idx]
        return ""


@app.route('/api/talks', method='GET')
@enable_cors
def get_talk():
    response.content_type = 'application/json'
    return {"data": talks}

@app.route('/api/talks', method='POST')
@enable_cors
def add_talk():
    response.content_type = 'application/json'
    json_data = json.loads(request.data)
    new_id = uuid.uuid4()
    json_data['id'] = new_id
    talks.append(json_data)
    return {"id": json_data['id']}


if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)