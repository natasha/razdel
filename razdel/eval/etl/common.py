# coding: utf-8
from __future__ import unicode_literals

import re
from itertools import groupby

from razdel.tests.partition import Partition


def is_bib(text):
    # Lot of these things in Corpora:
    # Astronomical Journal. — 1987. — С. 178—188.
    if re.search('— С. \d', text):
        return True

    # Калашниковой. – М.: Центрполиграф
    if re.search(r'[-—–]\s*(М|M|СПб)\.[:,]', text):
        return True

    # • Nelson Annandale, Francis Adam Marshall. Фарерские острова =
    # • The Faroes. — 1905. — 419 с.
    # ↑ Деррида Ж. Диссеминация (La Dissemination)
    if re.match('^\s*[•↑]', text):
        return True


def has_sent_ending(text):
    return re.search('[.?!…;)»"]\s*$', text)


def is_sent(text):
    return has_sent_ending(text) and not is_bib(text)


def partition_chunks(records):
    for index, (doc, text) in enumerate(records):
        if index > 0:
            yield ' '
        yield text


def group_partitions(records):
    for _, group in groupby(records, key=lambda _: _[0]):
        chunks = list(partition_chunks(group))
        yield Partition(chunks)
