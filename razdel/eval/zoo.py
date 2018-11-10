# coding: utf-8
from __future__ import unicode_literals

import re
import logging
from contextlib import contextmanager

from razdel.substring import find_substrings


def dot_sentenize_(text):
    previous = 0
    for match in re.finditer(r'([.?!…])\s+', text, re.U):
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


TOKEN = re.compile(r'([^\W\d]+|\d+|[^\w\s])', re.U)


def space_tokenize(text):
    chunks = re.split(r'\s+', text)
    return find_substrings(chunks, text)


def re_tokenize(text):
    chunks = TOKEN.findall(text)
    return find_substrings(chunks, text)


def nltk_tokenize(text):
    from nltk.tokenize import word_tokenize

    chunks = word_tokenize(text, 'russian')
    return find_substrings(chunks, text)


NLP = None


def spacy_tokenize(text):
    from spacy.lang.ru import Russian

    global NLP
    if not NLP:
        NLP = Russian()

    doc = NLP(text)
    chunks = [token.text for token in doc]
    return find_substrings(chunks, text)


NLP2 = None


def spacy_tokenize2(text):
    from spacy.lang.ru import Russian
    from spacy_russian_tokenizer import (
        RussianTokenizer,
        MERGE_PATTERNS,
        SYNTAGRUS_RARE_CASES
    )

    global NLP2
    if not NLP2:
        NLP2 = Russian()
        NLP2.add_pipe(
            RussianTokenizer(NLP2, MERGE_PATTERNS + SYNTAGRUS_RARE_CASES),
            name='russian_tokenizer'
        )

    doc = NLP2(text)
    chunks = [token.text for token in doc]
    return find_substrings(chunks, text)
