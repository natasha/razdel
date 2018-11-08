# coding: utf-8
from __future__ import unicode_literals

from .utils import Record


SPLIT = 'split'
JOIN = 'join'


class Rule(Record):
    __attributes__ = ['name']

    def __init__(self, name):
        self.name = name

    def __call__(self, split):
        raise NotImplementedError


class FunctionRule(Rule):
    def __init__(self, function):
        super(FunctionRule, self).__init__(function.__name__)
        self.function = function

    def __call__(self, split):
        return self.function(split)
