# coding: utf-8
from __future__ import unicode_literals

import re

from razdel.substring import find_substrings
from razdel.tests.partition import substrings_partition
from .common import (
    is_sent,
    group_partitions
)


def parse_sents_(lines):
    lines = iter(lines)
    for line in lines:
        match = re.match(r'^# sent_id = (.+)$', line)
        if match:
            id = match.group(1)
            match = re.match(r'^([^.]+).xml_\d+$', id)
            doc = match.group(1)
            line = next(lines)
            match = re.match(r'# text = (.+)$', line)
            text = match.group(1).strip()
            if is_sent(text):
                yield doc, text


def parse_sents(lines):
    records = parse_sents_(lines)
    return group_partitions(records)


def parse_tokens(lines):
    lines = iter(lines)
    sent = None
    buffer = []
    for line in lines:
        if not line:
            substrings = find_substrings(buffer, sent)
            yield substrings_partition(substrings)
            buffer = []
        else:
            match = re.match(r'# text = (.+)$', line)
            if match:
                sent = match.group(1)
            if re.match(r'^\d', line):
                parts = line.split('\t')
                word = parts[1]
                buffer.append(word)
