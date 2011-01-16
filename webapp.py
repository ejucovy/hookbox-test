import json
from webob import Request, Response
from paste.httpserver import serve
from pymongo import Connection
from tempita import Template

data = dict()

letters = "abcdefghijklmnopqrstuvwxyz"
import random

def pick_name():
    name = []
    length = random.randint(5, 10)
    for i in range(length):
        name.append(random.choice(letters))
    return ''.join(name)

class App(object):

    def __call__(self, environ, start_response):
        req = Request(environ)
        path_info = req.path_info.strip('/')
        print path_info
        if path_info == '':
            return Response(self.index(req))(
                environ, start_response)
        try:
            method = getattr(self, path_info)
        except AttributeError:
            return Response('404', status=404)(environ, start_response)
        resp = Response(json.dumps(method(req)), content_type="application/json")
        return resp(environ, start_response)

    def index(self, req):
        _index = Template.from_filename('index.html')
        conn = Connection()
        db = conn.comet
        coll = db.points
        data = coll.find()
        _index = _index.substitute(data=data)
        return _index

    def connect(self, req):
        return [True, {"name": pick_name()}]
    

    def disconnect(self, req):
        return [True, {}]

    def create_channel(self, req):
        return [True, {'history_size': 0, "reflective": False, "presenceful": True}]

    def subscribe(self, req):
        return [True, {}]

    def unsubscribe(self, req):
        return [True, {}]

    def publish(self, req):
        # some stupid mangling is required
        data = req.POST['payload'].replace("'", '"').replace('u"', '"')
        data = json.loads(data)
        id_ = data['id']
        conn = Connection()
        db = conn.comet
        coll = db.points
        coll.update({u"id": id_}, {"$set": data}, upsert=True)
        return [True, {}]

<<<<<<< HEAD
serve(App(), port="8000")
=======
    def getpoints(self, req):
        conn = Connection()
        db = conn.comet
        coll = db.points
        x = []
        for i in coll:
            del i['_id']
            x.append(i)
        return x

serve(App(), host="0.0.0.0", port="4444")
>>>>>>> 0f60e8dcfd74c25a05feaa2f37253c51f4e504b4
