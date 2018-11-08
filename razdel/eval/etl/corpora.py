# coding: utf-8
from __future__ import unicode_literals

from razdel.utils import filter_xml

from .common import is_sent


def parse_sents(stream):
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
