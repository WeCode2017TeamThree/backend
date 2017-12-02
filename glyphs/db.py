"""
"""
from contextlib import contextmanager
import os
import sys

from mongoengine import register_connection
from mongoengine.connection import get_connection

from twisted.logger import Logger

from glyphs.const import GLYPHS_DB, DB_ALIAS_DEFAULT


log = Logger()
CONNECTION_GLYPHS = None


@contextmanager
def connection(connectString, *a, **kw):
    """
    Code that needs a db connection should live inside a with block managed here.
    """
    global CONNECTION_GLYPHS

    register_connection(GLYPHS_DB, host=connectString, *a, **kw)
    register_connection(DB_ALIAS_DEFAULT, host=connectString, *a, **kw)

    conn = get_connection(GLYPHS_DB, reconnect=False)
    if not CONNECTION_GLYPHS:
        CONNECTION_GLYPHS = conn
        log.info("mongoengine: Connected to database {name!r}", name=connectString, out_=sys.stderr)

    yield conn
