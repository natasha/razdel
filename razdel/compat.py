# coding: utf-8
from __future__ import unicode_literals

try:
    # Python 2
    str = unicode
    string_type = basestring
except NameError:
    # Python 3
    str = str
    string_type = str
