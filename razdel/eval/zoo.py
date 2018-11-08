# coding: utf-8
from __future__ import unicode_literals

import re
import logging
from contextlib import contextmanager

from razdel.substring import find_substrings


def dot_sentenize_(text):
    previous = 0
    for match in re.finditer(r'([.?!…])\s+', text):
        delimiter = match.group(1)
        start = match.start()
        yield text[previous:start] + delimiter
        previous = match.end()
    if previous < len(text):
        yield text[previous:]


def dot_sentenize(text):
    chunks = dot_sentenize_(text)
    return find_substrings(chunks, text)


@contextmanager
def no_logger(logger):
    logger.disabled = True
    try:
        yield
    finally:
        logger.disabled = False


LOGGER = logging.getLogger()


def deepmipt_sentenize(text):
    from rusenttokenize import ru_sent_tokenize

    with no_logger(LOGGER):
        chunks = ru_sent_tokenize(text)
    return find_substrings(chunks, text)


def nltk_sentenize(text):
    from nltk import sent_tokenize

    chunks = sent_tokenize(text, 'russian')
    return find_substrings(chunks, text)


def segtok_sentenize(text):
    from segtok.segmenter import split_single

    chunks = split_single(text)
    return find_substrings(chunks, text)
