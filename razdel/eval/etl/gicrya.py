# coding: utf-8
from __future__ import unicode_literals, division

from .common import is_sent


# 1	Жуткий	жуткий	ADJ	Case=Nom|Degree=Pos|Gender=Masc|Number=Sing
# 2	холод	холод	NOUN	Animacy=Inan|Case=Nom|Gender=Masc|Number=Sing
# 3	,	,	PUNCT	_


def parse_sents(lines):
    index = 0
    buffer = []
    for line in lines:
        if line:
            parts = line.split('\t')
            word = parts[1]
            buffer.append(word)
        else:
            text = ' '.join(buffer)
            if not is_sent(text):
                continue
            # group sents by 191 size chunks
            doc = str(index // 191)
            yield doc, text
            index += 1
            buffer = []
