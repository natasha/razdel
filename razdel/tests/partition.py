# coding: utf-8
from __future__ import unicode_literals

import re

from razdel.utils import Record
from razdel.substring import Substring


class Partition(Record):
    __attributes__ = ['chunks']

    is_fill = re.compile('^\s*$').match

    def __init__(self, chunks):
        self.chunks = chunks

    @property
    def as_text(self):
        return ''.join(self.chunks)

    @property
    def as_substrings(self):
        start = 0
        for chunk in self.chunks:
            stop = start + len(chunk)
            if not self.is_fill(chunk):
                yield Substring(start, stop, chunk)
            start = stop


ESCAPE = [
    ('|', r'\|'),
    ('\n', r'\n')
]


def escape_chunk(chunk):
    for source, target in ESCAPE:
        chunk = chunk.replace(source, target)
    return chunk


def unescape_chunk(chunk):
    for source, target in ESCAPE:
        chunk = chunk.replace(target, source)
    return chunk


def parse_partition(line):
    # re negative lookbehind assertion
    chunks = re.split(r'(?<!\\)\|', line)
    return Partition([unescape_chunk(_) for _ in chunks])


def parse_partitions(lines):
    for line in lines:
        yield parse_partition(line)


def format_partition(partition):
    return '|'.join(escape_chunk(_) for _ in partition.chunks)


def format_partitions(partitions):
    for partition in partitions:
        yield format_partition(partition)


def substring_bounds(substrings):
    for substring in substrings:
        yield substring.start
        yield substring.stop


def split_text(text, bounds):
    previous = 0
    for index in bounds:
        if previous < index:
            yield text[previous:index]
        previous = index
    if previous < len(text):
        yield text[previous:]


def update_partition(partition, segment):
    text = partition.as_text
    substrings = segment(text)
    bounds = substring_bounds(substrings)
    chunks = list(split_text(text, bounds))
    return Partition(chunks)


def update_partitions(partitions, segment):
    for partition in partitions:
        yield update_partition(partition, segment)


def substrings_partition_(substrings, fill):
    previous = 0
    for index, substring in enumerate(substrings):
        if index > 0:
            size = substring.start - previous
            yield fill * size
        yield substring.text
        previous = substring.stop


def substrings_partition(substrings, fill=' '):
    chunks = list(substrings_partition_(substrings, fill))
    return Partition(chunks)


def chunks_partition_(chunks, fill):
    for index, chunk in enumerate(chunks):
        if index > 0:
            yield fill
        yield chunk


def chunks_partition(chunks, fill=' '):
    chunks = list(chunks_partition_(chunks, fill))
    return Partition(chunks)
