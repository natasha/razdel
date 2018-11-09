# coding: utf-8
from __future__ import unicode_literals

from razdel.tests.partition import chunks_partition
from .common import (
    is_sent,
    group_partitions
)


def parse_sents_(lines):
    doc = 0
    buffer = []
    for line in lines:
        if line.startswith('==>'):
            continue
        elif line == '==newfile==':
            doc += 1
        else:
            if line:
                parts = line.split('\t')
                word = parts[1]
                buffer.append(word)
            else:
                text = ' '.join(buffer)
                if not is_sent(text):
                    continue
                yield doc, text
                buffer = []


def parse_sents(lines):
    records = parse_sents_(lines)
    return group_partitions(records)


def parse_tokens(lines):
    buffer = []
    for line in lines:
        if line.startswith('=='):
            continue
        else:
            if line:
                parts = line.split('\t')
                word = parts[1]
                buffer.append(word)
            else:
                yield chunks_partition(buffer)
                buffer = []
