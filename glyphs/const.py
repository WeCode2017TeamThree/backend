"""
"""
import os

# mongo connect strings
GLYPHS_DB = 'glyphs'
DB_ALIAS_DEFAULT = 'default'
_DB_CONNECT_STRING = 'mongodb://localhost/' + GLYPHS_DB
GLYPHS_DB_CONNECT = os.environ.get('MONGODB_URI', _DB_CONNECT_STRING)
