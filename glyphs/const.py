"""
"""
import os

# mongo connect strings
GLYPHS_DB = 'glyphs'
DB_ALIAS_DEFAULT = 'default'
MONGO_HOST = os.environ.get('glyphs_mongo_host', 'localhost')
_DB_CONNECT_STRING = 'mongodb://%s/' % MONGO_HOST
GLYPHS_DB_CONNECT = _DB_CONNECT_STRING + GLYPHS_DB