# coding: utf-8
from __future__ import unicode_literals, print_function

import sys
import argparse
from random import seed, sample

from razdel.compat import (
    decode,
    encode,
    BrokenPipeError
)
from razdel.eval.tests import (
    generate_partition_precision_tests,
    generate_partition_recall_tests
)
from razdel.eval.zoo import (
    dot_sentenize,
    deepmipt_sentenize,
    nltk_sentenize,
    segtok_sentenize,
    moses_sentenize,

    space_tokenize,
    re_tokenize,
    nltk_tokenize,
    spacy_tokenize,
    spacy_tokenize2,
    mystem_tokenize,
    moses_tokenize,
)
from razdel import (
    sentenize,
    tokenize
)
from .partition import (
    parse_partitions,
    format_partitions,
    update_partitions
)


ZOO = {
    'dot_sentenize': dot_sentenize,
    'deepmipt_sentenize': deepmipt_sentenize,
    'nltk_sentenize': nltk_sentenize,
    'segtok_sentenize': segtok_sentenize,
    'moses_sentenize': moses_sentenize,
    'sentenize': sentenize,

    'space_tokenize': space_tokenize,
    're_tokenize': re_tokenize,
    'nltk_tokenize': nltk_tokenize,
    'spacy_tokenize': spacy_tokenize,
    'spacy_tokenize2': spacy_tokenize2,
    'mystem_tokenize': mystem_tokenize,
    'moses_tokenize': moses_tokenize,
    'tokenize': tokenize,
}


def stdin_lines():
    for line in sys.stdin:
        yield decode(line).rstrip('\n')


def stdout_lines(lines):
    for line in lines:
        print(encode(line), file=sys.stdout)


def generate_(partitions, precision, recall):
    for partition in partitions:
        if precision:
            for test in generate_partition_precision_tests(partition):
                yield test
        if recall:
            for test in generate_partition_recall_tests(partition):
                yield test


def generate_command(args):
    precision = args.precision
    recall = args.recall
    if not precision and not recall:
        precision = True
        recall = True
    lines = stdin_lines()
    partitions = parse_partitions(lines)
    tests = generate_(partitions, precision, recall)
    lines = format_partitions(tests)
    stdout_lines(lines)


def sample_command(args):
    seed(args.seed)
    lines = list(stdin_lines())
    lines = sample(lines, args.size)
    stdout_lines(lines)


def show_(guess, etalon):
    print('---etalon')
    for _ in etalon:
        print('>', encode(_.text))
    print('---guess')
    for _ in guess:
        print('>', encode(_.text))
    print()


def diff_(tests, segment, show):
    for test in tests:
        guess = list(segment(test.as_text))
        etalon = list(test.as_substrings)
        if guess != etalon:
            if show:
                show_(guess, etalon)
            else:
                yield test


def diff_command(args):
    segment = ZOO[args.segment]
    lines = stdin_lines()
    partitions = parse_partitions(lines)
    tests = diff_(partitions, segment, args.show)
    lines = format_partitions(tests)
    stdout_lines(lines)


def update_command(args):
    segment = ZOO[args.segment]
    lines = stdin_lines()
    partitions = parse_partitions(lines)
    partitions = update_partitions(partitions, segment)
    lines = format_partitions(partitions)
    stdout_lines(lines)


def main():
    parser = argparse.ArgumentParser(prog='ctl')
    parser.set_defaults(function=None)

    sub = parser.add_subparsers()

    generate = sub.add_parser('gen')
    generate.set_defaults(function=generate_command)
    generate.add_argument('--precision', action='store_true')
    generate.add_argument('--recall', action='store_true')

    sample = sub.add_parser('sample')
    sample.set_defaults(function=sample_command)
    sample.add_argument('size', type=int)
    sample.add_argument('--seed', type=int, default=1)

    diff = sub.add_parser('diff')
    diff.set_defaults(function=diff_command)
    diff.add_argument('segment', choices=ZOO)
    diff.add_argument('--show', action='store_true')

    run = sub.add_parser('up')
    run.set_defaults(function=update_command)
    run.add_argument('segment', choices=ZOO)

    args = sys.argv[1:]
    args = parser.parse_args(args)
    if not args.function:
        parser.print_help()
        parser.exit()
    try:
        args.function(args)
    except BrokenPipeError:
        pass


if __name__ == '__main__':
    main()
