# coding: utf-8
from __future__ import unicode_literals, print_function

from razdel.utils import (
    Record,
    assert_type
)
from razdel.rule import (
    JOIN,
    Rule
)
from razdel.split import Splitter
from razdel.substring import find_substrings


class Segmenter(Record):
    __attributes__ = ['split', 'rules']

    def __init__(self, split, rules):
        assert_type(split, Splitter)
        self.split = split
        for rule in rules:
            assert_type(rule, Rule)
        self.rules = rules

    def join(self, split):
        for rule in self.rules:
            action = rule(split)
            if action:
                return action == JOIN

    def segment(self, parts):
        buffer = next(parts)
        for split in parts:
            right = next(parts)
            split.buffer = buffer
            if self.join(split):
                buffer = buffer + split.delimiter + right
            else:
                yield buffer + split.delimiter
                buffer = right
        yield buffer

    post = None

    def __call__(self, text):
        parts = self.split(text)
        chunks = self.segment(parts)
        if self.post:
            chunks = self.post(chunks)
        return find_substrings(chunks, text)


class DebugSegmenter(Segmenter):
    def join(self, split):
        print(split.left, '|', split.delimiter, '|', split.right)
        for rule in self.rules:
            action = rule(split)
            if action:
                print('\t', action, rule.name)
                return action == JOIN
