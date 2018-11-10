# coding: utf-8
from __future__ import unicode_literals

from os.path import join as join_path  # noqa
from glob import iglob as list_paths  # noqa
from xml.etree import ElementTree as ET

from razdel.compat import (
    decode,
    encode,
)


class cached_property(object):
    def __init__(self, function):
        self.function = function
        self.name = function.__name__

    def __get__(self, instance, type=None):
        if self.name not in instance.__dict__:
            result = instance.__dict__[self.name] = self.function(instance)
            return result
        return instance.__dict__[self.name]


class Record(object):
    __attributes__ = []

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and all(
                (getattr(self, _) == getattr(other, _))
                for _ in self.__attributes__
            )
        )

    def __ne__(self, other):
        return not self == other

    def __iter__(self):
        return (getattr(self, _) for _ in self.__attributes__)

    def __hash__(self):
        return hash(tuple(self))

    def __repr__(self):
        name = self.__class__.__name__
        args = ', '.join(
            repr(getattr(self, _))
            for _ in self.__attributes__
        )
        return '{name}({args})'.format(
            name=name,
            args=args
        )

    def _repr_pretty_(self, printer, cycle):
        name = self.__class__.__name__
        if cycle:
            printer.text('{name}(...)'.format(name=name))
        else:
            with printer.group(len(name) + 1, '{name}('.format(name=name), ')'):
                for index, key in enumerate(self.__attributes__):
                    if index > 0:
                        printer.text(',')
                        printer.breakable()
                    value = getattr(self, key)
                    printer.pretty(value)


def assert_type(item, types):
    if not isinstance(item, types):
        if not isinstance(types, tuple):
            types = [types]
        raise TypeError('expected {types}, got {type}'.format(
            types=' or '.join(_.__name__ for _ in types),
            type=type(item).__name__
        ))


def load_lines(path):
    with open(path) as file:
        for line in file:
            yield decode(line).rstrip('\n')


def dump_lines(lines, path):
    with open(path, 'w') as file:
        for line in lines:
            file.write(encode(line) + '\n')


def load_xml(path):
    return ET.iterparse(path, events=('start', 'end'))


def filter_xml(stream, tags):
    for event, node in stream:
        if node.tag in tags:
            yield event, node
