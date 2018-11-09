# coding: utf-8
from __future__ import unicode_literals

import re

from .utils import (
    Record,
    cached_property
)
from .rule import (
    JOIN, SPLIT,
    Rule,
    FunctionRule
)
from .split import (
    Split,
    Splitter,
)
from .segmenter import (
    Segmenter,
    DebugSegmenter
)


RU = 'RU'
LAT = 'LAT'
INT = 'INT'
PUNCT = 'PUNCT'
OTHER = 'OTHER'

ATOM = re.compile(
    r'''
    (?P<RU>[а-яё]+)
    |(?P<LAT>[a-z]+)
    |(?P<INT>\d+)
    |(?P<PUNCT>[-\\/!#$%&()\[\]\*\+,\.:;<=>?@^_`{|}~№…"\'«»„“ʼʻ”])
    |(?P<OTHER>\S)
    ''',
    re.I | re.U | re.X
)

DASHES = '‑–—−-'
UNDERSCORE = '_'
DOT = '.'
COMMA = ','


##########
#
#  TRIVIAL
#
######


def split_space(split):
    if split.delimiter:
        return SPLIT


##########
#
#   2112
#
##########


class Rule2112(Rule):
    def __call__(self, split):
        if self.delimiter(split.left):
            # что-|то
            left, right = split.left_2, split.right_1
        elif self.delimiter(split.right):
            # что|-то
            left, right = split.left_1, split.right_2
        else:
            return

        if not left or not right:
            return

        return self.rule(left, right)


class DashRule(Rule2112):
    name = 'dash'

    def delimiter(self, delimiter):
        return delimiter in DASHES

    def rule(self, left, right):
        if left.type == PUNCT or right.type == PUNCT:
            return
        return JOIN


class UnderscoreRule(Rule2112):
    name = 'dash'

    def delimiter(self, delimiter):
        return delimiter == UNDERSCORE

    def rule(self, left, right):
        if left.type == PUNCT or right.type == PUNCT:
            return
        return JOIN


class FloatRule(Rule2112):
    name = 'float'

    def delimiter(self, delimiter):
        return delimiter in (DOT, COMMA)

    def rule(self, left, right):
        if left.type == INT and right.type == INT:
            return JOIN


########
#
#   11
#
##########


def punct(split):
    if split.left_1.type == PUNCT and split.right_1.type == PUNCT:
        return JOIN


#########
#
#   l1
#
##########


def initials(split):
    if split.right_1.text != DOT:
        return

    left = split.left_1.text
    if len(left) == 1 and left.isupper():
        return JOIN


########
#
#   SPLIT
#
########


class Atom(Record):
    __attributes__ = ['start', 'stop', 'type', 'text']

    def __init__(self, start, stop, type, text):
        self.start = start
        self.stop = stop
        self.type = type
        self.text = text
        self.normal = text.lower()


class TokenSplit(Split):
    def __init__(self, left, delimiter, right):
        self.left_atoms = left
        self.right_atoms = right
        super(TokenSplit, self).__init__(
            self.left_1.text,
            delimiter,
            self.right_1.text
        )

    @cached_property
    def left_1(self):
        return self.left_atoms[-1]

    @cached_property
    def left_2(self):
        if len(self.left_atoms) > 1:
            return self.left_atoms[-2]

    @cached_property
    def right_1(self):
        return self.right_atoms[0]

    @cached_property
    def right_2(self):
        if len(self.right_atoms) > 1:
            return self.right_atoms[1]


class TokenSplitter(Splitter):
    def __init__(self, window=2):
        self.window = window

    def atoms(self, text):
        matches = ATOM.finditer(text)
        for match in matches:
            start = match.start()
            stop = match.end()
            type = match.lastgroup
            text = match.group(0)
            yield Atom(
                start, stop,
                type, text
            )

    def __call__(self, text):
        atoms = list(self.atoms(text))
        for index in range(len(atoms)):
            atom = atoms[index]
            if index > 0:
                previous = atoms[index - 1]
                delimiter = text[previous.stop:atom.start]
                left = atoms[max(0, index - self.window):index]
                right = atoms[index:index + self.window]
                yield TokenSplit(left, delimiter, right)
            yield atom.text


########
#
#   SEGMENT
#
########


RULES = [
    DashRule(),
    UnderscoreRule(),
    FloatRule(),

    FunctionRule(punct),
    FunctionRule(initials)
]


class TokenSegmenter(Segmenter):
    def __init__(self):
        super(TokenSegmenter, self).__init__(TokenSplitter(), RULES)

    def segment(self, parts):
        buffer = next(parts)
        for split in parts:
            right = next(parts)
            split.buffer = buffer
            if not split.delimiter and self.join(split):
                buffer += right
            else:
                yield buffer
                buffer = right
        yield buffer

    @property
    def debug(self):
        return DebugTokenSegmenter()


class DebugTokenSegmenter(TokenSegmenter, DebugSegmenter):
    pass


tokenize = TokenSegmenter()
