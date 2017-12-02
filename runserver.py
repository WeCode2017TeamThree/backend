"""
Runs the glyphs server
"""
from contextlib import contextmanager
import os
import sys

from codado.tx import Main

from twisted.internet import reactor, endpoints, defer
from twisted.python import log as tlog
from twisted.web.server import Site

from glyphs import db
from glyphs.const import GLYPHS_DB_CONNECT
from glyphs.server import Server


LOG_DIR = './http'
LOG_PATH = '%s/http-requests.log' % LOG_DIR
DEFAULT_PORT = int(os.environ["PORT"]) or 8080


class Run(Main):
    """
    Command that runs the glyphs server
    """
    synopsis = "run"

    callLater = reactor.callLater

    def postOptions(self):
        """
        Start logging and run the webserver
        """
        tlog.startLogging(sys.stdout)

        with createWeb() as webFactory:
            epWeb = endpoints.serverFromString(reactor, 'tcp:%s' % DEFAULT_PORT)
            dWeb = epWeb.listen(webFactory)

            def giveUp(f):
                f.printTraceback()
                self.callLater(0, reactor.stop)

            dl = defer.DeferredList([dWeb,], fireOnOneErrback=True).addErrback(giveUp)
            reactor.run()
            return dl


@contextmanager
def createWeb():
    """
    Create a factory for starting the website
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    with db.connection(GLYPHS_DB_CONNECT):
        yield Site(Server().app.resource(), logPath=LOG_PATH)


Run.main()
