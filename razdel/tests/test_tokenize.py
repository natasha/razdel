# coding: utf-8
from __future__ import unicode_literals

import pytest

from razdel import tokenize

from .partition import parse_partitions


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
    guess = list(tokenize.debug(test.as_text))
    etalon = list(test.as_substrings)
    assert guess == etalon
