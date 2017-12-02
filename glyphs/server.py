"""
"""
from functools import wraps
import json

from klein import Klein

from twisted.internet import defer
from twisted.web.resource import Resource
from twisted.web.static import File

from glyphs.location import Location


def jsonAPI(f):
    """
    """
    @wraps(f)
    def jsonWrapper(self, request, *a, **kw):
        request.setHeader("Content-Type", "application/json")
        content = request.content.read()
        if content:
            request.payload = json.loads(content)
        d = defer.maybeDeferred(f, self, request, *a, **kw)
        d.addCallback(json.dumps)
        return d
    return jsonWrapper


class Server(object):
    """
    The web server for wayfarer-glyphs
    """
    app = Klein()

    @app.route('/')
    def home(self, request):
        """
        """
        f = File("public/index.html")
        f.type, f.encoding = 'text/plain', None
        r = Resource()
        r.putChild(b"", f)
        return r

    @app.route("/api/v1/locations")
    @jsonAPI
    def listLocations(self, request):
        """
        """
        return [loc.toJSType() for loc in Location.objects()]

    @app.route('/api/v1/location/<string:id>')
    @jsonAPI
    def getLocation(self, request, id):
        """
        """
        return Location.objects(id=id).first().toJSType()

    @app.route('/api/v1/location', methods=['POST'])
    @jsonAPI
    def createLocation(self, request):
        """
        """
        data = request.payload['location']
        loc = Location(**data)
        loc.save()
        return {'status': 'ok'}
