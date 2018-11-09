# coding: utf-8
from __future__ import unicode_literals

from razdel.utils import filter_xml

from razdel.substring import find_substrings
from razdel.tests.partition import substrings_partition
from .common import (
    is_sent,
    group_partitions
)


def parse_sents_(stream):
    stream = filter_xml(stream, tags={'text', 'source'})
    for event, node in stream:
        tag = node.tag
        if event == 'start' and tag == 'text':
            doc = node.get('id')
        elif event == 'end':
            if tag == 'source':
                text = node.text.strip()
                if is_sent(text):
                    yield doc, text
            node.clear()


def parse_sents(lines):
    records = parse_sents_(lines)
    return group_partitions(records)


def parse_tokens(stream):
    stream = filter_xml(stream, tags={'source', 'tokens', 'token'})
    buffer = []
    for event, node in stream:
        if event == 'end':
            tag = node.tag
            if tag == 'source':
                sent = node.text.strip()
            elif tag == 'token':
                word = node.get('text')
                buffer.append(word)
            elif tag == 'tokens':
                substrings = find_substrings(buffer, sent)
                yield substrings_partition(substrings)
                buffer = []
            node.clear()
