# coding: utf-8
from __future__ import unicode_literals

from razdel.utils import Record


class Split(Record):
    __attributes__ = ['left', 'delimiter', 'right', 'buffer']

    def __init__(self, left, delimiter, right, buffer=None):
        self.left = left
        self.delimiter = delimiter
        self.right = right
        self.buffer = buffer


class Splitter(Record):
    pass
