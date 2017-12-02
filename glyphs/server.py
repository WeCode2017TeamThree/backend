"""
"""
from functools import wraps
import json

from jinja2 import Environment, FileSystemLoader

from klein import Klein

from twisted.internet import defer

from glyphs.location import Location, Comment, Rating


ENV = Environment(loader=FileSystemLoader('public'))


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
        return ENV.get_template("index.html").render()

    @app.route("/api/v1/locations")
    @jsonAPI
    def listLocations(self, request):
        """
        """
        return [loc.toJSType() for loc in Location.objects()]

    @app.route('/api/v1/location/<string:id>/comment', methods=['POST'])
    @jsonAPI
    def addComment(self, request, id):
        """
        """
        data = request.payload['comment']
        c = Comment(**data)
        loc = Location.objects(id=id).first()
        loc.comments.append(c)
        loc.save()
        return {'status': 'ok'}

    @app.route('/api/v1/location/<string:id>/feature', methods=['POST'])
    @jsonAPI
    def addFeature(self, request, id):
        """
        """
        import pdb; pdb.set_trace()
        data = request.payload['feature']
        c = Comment(**data)
        loc = Location.objects(id=id).first()
        loc.comments.append(c)
        loc.save()
        return {'status': 'ok'}

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
        features = data.pop('feature_set', None)
        loc = Location(**data)
        for f in features:
            loc.feature_set[f] = Rating(upvotes=1)
        loc.feature_set.save()
        loc.save()
        return {'status': 'ok'}
