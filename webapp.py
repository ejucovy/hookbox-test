import json
from webob import Request, Response
from paste.httpserver import serve

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
        print resp.body
        return resp(environ, start_response)

    def index(self, req):
        _index = open('index.html').read()
        return _index

    def connect(self, req):
        return [True, {"name": "guest"}]

    def disconnect(self, req):
        return [True, {}]

    def create_channel(self, req):
        return [True, {'history_size': 0, "reflective": True, "presenceful": True}]

    def subscribe(self, req):
        return [True, {}]

    def unsubscribe(self, req):
        return [True, {}]

    def publish(self, req):
        return [True, {}]

serve(App(), port="8080")
