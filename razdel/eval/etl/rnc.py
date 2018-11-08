# coding: utf-8
from __future__ import unicode_literals

from .common import is_sent


def parse_sents(lines):
    index = 0
    buffer = []
    for line in lines:
        if line.startswith('==>'):
            continue
        elif line == '==newfile==':
            index += 1
        else:
            if line:
                parts = line.split('\t')
                word = parts[1]
                buffer.append(word)
            else:
                text = ' '.join(buffer)
                if not is_sent(text):
                    continue
                doc = str(index)
                yield doc, text
                buffer = []
