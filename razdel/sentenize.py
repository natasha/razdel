# coding: utf-8
from __future__ import unicode_literals

import re

from .utils import cached_property
from .rule import (
    JOIN,
    FunctionRule
)
from .split import (
    Split,
    Splitter,
)
from .segmenter import (
    Segmenter,
    DebugSegmenter
)


SPACE_SUFFIX = re.compile(r'\s$', re.U)
SPACE_PREFIX = re.compile(r'^\s', re.U)

TOKEN = re.compile(r'([^\W\d]+|\d+|[^\w\s])', re.U)
FIRST_TOKEN = re.compile(r'^\s*([^\W\d]+|\d+|[^\w\s])', re.U)
LAST_TOKEN = re.compile(r'([^\W\d]+|\d+|[^\w\s])\s*$', re.U)
WORD = re.compile(r'([^\W\d]+|\d+)', re.U)
PAIR_SOKR = re.compile(r'(\w)\s*\.\s*(\w)\s*$', re.U)
INT_SOKR = re.compile(r'\d+\s*-?\s*(\w+)\s*$', re.U)

DOT = '.'
SEMICOLON = ';'
ENDINGS = '.?!…'
DASHES = '‑–—−-'

OPEN_QUOTES = '«“‘'
CLOSE_QUOTES = '»”’'
GENERIC_QUOTES = '"„'
QUOTES = OPEN_QUOTES + CLOSE_QUOTES + GENERIC_QUOTES

OPEN_BRACKETS = '([}'
CLOSE_BRACKETS = ')]}'
BRACKETS = OPEN_BRACKETS + CLOSE_BRACKETS

CLOSE_BOUNDS = CLOSE_QUOTES + CLOSE_BRACKETS

ROMAN = re.compile(r'^[IVXML]+$', re.U)
BULLET_CHARS = set('§абвгдеabcdef')
BULLET_BOUNDS = '.)'
BULLET_SIZE = 20

DELIMITERS = ENDINGS + SEMICOLON + GENERIC_QUOTES + CLOSE_QUOTES + CLOSE_BRACKETS
SMILES = r'[=:;]-?[)(]{1,3}'  # :-) ;) =(((
SMILE_PREFIX = re.compile(r'^\s*' + SMILES, re.U)


def parse_sokrs(lines):
    for line in lines:
        for word in line.split():
            yield word


def parse_pair_sokrs(lines):
    for line in lines:
        yield tuple(line.split())


TAIL_SOKRS = set(parse_sokrs([
    'дес тыс млн млрд',
    'дол долл',
    'коп руб р',
    'проц',  # 95 проц. акций,

    'га',
    'барр',  # 40 долларов за барр.
    'куб',  # 1000 куб. метр.
    'кв км',  # 700 тыс. кв. км.
    'см',  # 30 см

    'час мин сек',  # в 15 час. 13 мин. 53 сек.
    'в вв',  # XII в. XVIII—XIX вв.
    'г гг',  # 1996-1999гг

    'с стр',  # 287 стр.

    'co corp inc',

    'изд ed',  # 1-е изд. Arthur W. Hummel, ed. Eminent Chinese

    'др',  # и другие
    'al',  # North et al.
]))

HEAD_SOKRS = set(parse_sokrs([
    'букв',  # яп. 18禁, букв. «запрещено
    'ст',  # ст.-слав.
    'трад',  # кит. трад
    'лат венг исп кат укр нем англ фр итал греч',
    'евр араб яп слав кит рус русск латв',
    'словацк хорв',

    'mr mrs ms dr vs',
    'св',  # св.Иоанна
    'арх зав зам проф акад',
    'кн',  # кандидат наук
    'корр',  # сообщил корр. ИТАР-ТАСС
    'ред',  # Под ред. Линды Уильямс
    'гр',  # гр. Валевской
    'ср',  # Ср. L. Ross
    'чл корр',  # является чл.-корр. АН СССР
    'им',  # им. Вс. Мейерхольда
    'тов',  # тюремном подвале тов. Берия

    'нач пол',  # нач. XX века

    'chap',
    'п пп ст ч чч гл стр абз пт',  # ст. 129 ч. 2 п. 8 Гл. VI
    'no',  # No. 6

    'просп ул ш г гор д стр корп пер корп обл эт пом ауд',
    'т',  # т. 1 л.д. 85-89
    'х',  # х. Ново-Максимовский
    'пл',  # площадь
    'bd',  # Bd. 16, Berlin
    'о оз',  # Вблизи оз. Селяха
    'р',  # р. Иордан

    'обр',  # обр. 1936 г.
    'ум',  # ум. 1064
    'ок',  # "родилась ок. 1211", "работают ок. 150 специалистов"
    'откр',  # Откр. 20:40

    'пс ps',
    'upd',
    'см',
    'напр',  # UNIX-семейства, напр. Linux, FreeBSD

    'тел',
    'сб',  # Сб. «Киноварь»
    'внутр',  # к внутр. миру героев
    'дифф',  # мне по дифф. зачёту «5» поставил
    'гос',  # гос. экзамены
    'отм',  # от отм. 0.000
]))

OTHER_SOKRS = set(parse_sokrs([
    'сокр рис искл прим',

    'яз',
    'устар',  # пометкой "устар."
    'шутл',  # "в стиле шутл.", "bones — шутл. человек"
]))

SOKRS = TAIL_SOKRS | HEAD_SOKRS | OTHER_SOKRS

TAIL_PAIR_SOKRS = set(parse_pair_sokrs([
    'т п',
    'т д',
    'у е',
    'н э',
    'p m',
    'a m',
    'с г',  # от 18 мая с. г.
    'р х',  # 250 года до Р. Х.
    'с г',  # 18 мая с. г.
    'с ш',  # 50°13′ с. ш.
    'з д',  # 12°48′ з. д.
    'ч т', 'т д',  # ч.т.д
]))

HEAD_PAIR_SOKRS = set(parse_pair_sokrs([
    'т е',
    'т н',
    'и о',
    'к н',
    'к п', 'п н',  # к.п.н
    'к т', 'т н',  # к.т.н
    'л д',  # т. 1 л.д. 85-89
]))

OTHER_PAIR_SOKRS = set(parse_pair_sokrs([
    'ед ч',
    'мн ч',
    'повел накл',  # в 1 лице мн. ч. повел. накл.
    'жен р'
    'муж р',
]))

PAIR_SOKRS = TAIL_PAIR_SOKRS | HEAD_PAIR_SOKRS | OTHER_PAIR_SOKRS

INITIALS = {
    'дж',
    'ed',
    'вс',  # Вс. Мейерхольда
}


def is_lower_alpha(token):
    return token.isalpha() and token.islower()


def is_title(token):
    return token[0].isupper()


def is_punkt(token):
    return not token.isalnum()


#######
#
#   TRIVIAL
#
######


def empty_side(split):
    if not split.left_token or not split.right_token:
        return JOIN


def no_space_prefix(split):
    if not split.right_space_prefix:
        return JOIN


def lower_right(split):
    if is_lower_alpha(split.right_token):
        return JOIN


def delimiter_right(split):
    right = split.right_token
    if right in GENERIC_QUOTES:
        return

    if right in DELIMITERS:
        return JOIN

    if SMILE_PREFIX.match(split.right):
        return JOIN


########
#
#   SOKR
#
#########


def is_sokr(token):
    if token.isdigit():
        return True
    if not token.isalpha():
        return True  # punct
    return token.islower()  # lower alpha


def sokr_left(split):
    if split.delimiter != DOT:
        return

    right = split.right_token
    match = split.left_pair_sokr
    if match:
        a, b = match
        left = a.lower(), b.lower()

        if left in HEAD_PAIR_SOKRS:
            return JOIN

        if left in PAIR_SOKRS:
            if is_sokr(right):
                return JOIN
            return

    left = split.left_token.lower()
    if left in HEAD_SOKRS:
        return JOIN

    if left in SOKRS and is_sokr(right):
            return JOIN


def inside_pair_sokr(split):
    if split.delimiter != DOT:
        return

    left = split.left_token.lower()
    right = split.right_token.lower()
    if (left, right) in PAIR_SOKRS:
        return JOIN


def initials_left(split):
    if split.delimiter != DOT:
        return

    left = split.left_token
    if left.isupper() and len(left) == 1:
        return JOIN
    if left.lower() in INITIALS:
        return JOIN


##########
#
#  BOUND
#
########


def close_bound(split):
    left = split.left_token
    if left in ENDINGS:
        return
    return JOIN


def close_quote(split):
    delimiter = split.delimiter
    if delimiter not in QUOTES:
        return

    if delimiter in CLOSE_QUOTES:
        return close_bound(split)

    if delimiter in GENERIC_QUOTES:
        if not split.left_space_suffix:
            return close_bound(split)
        return JOIN


def close_bracket(split):
    if split.delimiter in CLOSE_BRACKETS:
        return close_bound(split)


#######
#
#   BULLET
#
########


def is_bullet(token):
    if token.isdigit():
        return True
    if token in BULLET_BOUNDS:
        # "8.1." "2)."
        return True
    if token.lower() in BULLET_CHARS:
        return True
    if ROMAN.match(token):
        return True


def list_item(split):
    if split.delimiter not in BULLET_BOUNDS:
        return

    if len(split.buffer) > BULLET_SIZE:
        return

    if all(is_bullet(_) for _ in split.buffer_tokens):
        return JOIN


##########
#
#   SPLIT
#
##########


class SentSplit(Split):
    @cached_property
    def right_space_prefix(self):
        return bool(SPACE_PREFIX.match(self.right))

    @cached_property
    def left_space_suffix(self):
        return bool(SPACE_SUFFIX.search(self.left))

    @cached_property
    def right_token(self):
        match = FIRST_TOKEN.match(self.right)
        if match:
            return match.group(1)

    @cached_property
    def left_token(self):
        match = LAST_TOKEN.search(self.left)
        if match:
            return match.group(1)

    @cached_property
    def left_pair_sokr(self):
        match = PAIR_SOKR.search(self.left)
        if match:
            return match.groups()

    @cached_property
    def left_int_sokr(self):
        match = INT_SOKR.search(self.left)
        if match:
            return match.group(1)

    @cached_property
    def right_word(self):
        match = WORD.search(self.right)
        if match:
            return match.group(1)

    @cached_property
    def buffer_tokens(self):
        return TOKEN.findall(self.buffer)

    @cached_property
    def buffer_first_token(self):
        match = FIRST_TOKEN.match(self.buffer)
        if match:
            return match.group(1)


class SentSplitter(Splitter):
    __attributes__ = ['pattern']

    def __init__(self, window=10):
        self.pattern = '({smiles}|[{delimiters}])'.format(
            delimiters=re.escape(DELIMITERS),
            smiles=SMILES
        )
        self.window = window
        self.re = re.compile(self.pattern, re.U)

    def __call__(self, text):
        matches = self.re.finditer(text)
        previous = 0
        for match in matches:
            start = match.start()
            stop = match.end()
            delimiter = match.group(1)
            yield text[previous:start]
            left = text[max(0, start - self.window):start]
            right = text[stop:stop + self.window]
            yield SentSplit(left, delimiter, right)
            previous = stop
        yield text[previous:]


########
#
#   SEGMENT
#
########


RULES = [FunctionRule(_) for _ in [
    empty_side,
    no_space_prefix,
    lower_right,
    delimiter_right,

    sokr_left,
    inside_pair_sokr,
    initials_left,

    list_item,

    close_quote,
    close_bracket,
]]


class SentSegmenter(Segmenter):
    def __init__(self):
        super(SentSegmenter, self).__init__(SentSplitter(), RULES)

    @property
    def debug(self):
        return DebugSentSegmenter()

    def post(self, chunks):
        for chunk in chunks:
            yield chunk.strip()


class DebugSentSegmenter(SentSegmenter, DebugSegmenter):
    pass


sentenize = SentSegmenter()
