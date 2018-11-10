# coding: utf-8
from __future__ import unicode_literals

import pytest

from razdel import tokenize

from .partition import parse_partitions
from .common import (
    run,
    data_path,
    data_lines
)


UNIT = parse_partitions([
    '1',
    'что-то',
    'К_тому_же',
    '...',
    '1,5',
    '1/2',

    '»||.',
    ')||.',
    '(||«',
    ':)))',
    ':)||,',

    'mβж',
    'Δσ',
])


@pytest.mark.parametrize('test', UNIT)
def test_unit(test):
    run(tokenize, test)


def int_tests():
    path = data_path('tokens.txt')
    lines = data_lines(path, 1000)
    return parse_partitions(lines)


def test_int(int_test):
    run(tokenize, int_test)
