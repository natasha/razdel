# coding: utf-8
from __future__ import unicode_literals

try:
    # Python 2
    str = unicode
    string_type = basestring
    decode = lambda _: _.decode('utf8')
    encode = lambda _: _.encode('utf8')
    BrokenPipeError = IOError
except NameError:
    # Python 3
    str = str
    string_type = str
    decode = lambda _: _
    encode = lambda _: _
    BrokenPipeError = BrokenPipeError
