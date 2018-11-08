# coding: utf-8
from __future__ import unicode_literals, print_function

import sys
import argparse
from random import (
    sample,
    seed as set_seed
)

from razdel.eval.tests import (
    generate_partition_precision_tests,
    generate_partition_recall_tests
)
from razdel.eval.zoo import (
    dot_sentenize,
    deepmipt_sentenize,
    nltk_sentenize,
    segtok_sentenize
)
from razdel import sentenize
from ..partition import (
    parse_partitions,
    format_partitions,
    update_partitions
)


ZOO = {
    'dot_sentenize': dot_sentenize,
    'deepmipt_sentenize': deepmipt_sentenize,
    'nltk_sentenize': nltk_sentenize,
    'segtok_sentenize': segtok_sentenize,
    'sentenize': sentenize
}


def stdin_lines():
    for line in sys.stdin:
        yield line.rstrip('\n')


def stdout_lines(lines):
    for line in lines:
        print(line, file=sys.stdout)


def generate_(partitions):
    for partition in partitions:
        for test in generate_partition_precision_tests(partition):
            yield test
        for test in generate_partition_recall_tests(partition):
            yield test


def generate_command(_):
    lines = stdin_lines()
    partitions = parse_partitions(lines)
    tests = generate_(partitions)
    lines = format_partitions(tests)
    stdout_lines(lines)


def sample_command(args):
    set_seed(args.seed)
    lines = list(stdin_lines())
    lines = sample(lines, args.size)
    stdout_lines(lines)


def error_(tests, segment):
    for test in tests:
        guess = list(segment(test.as_text))
        etalon = list(test.as_substrings)
        if guess != etalon:
            yield test


def error_command(args):
    segment = ZOO[args.segment]
    lines = stdin_lines()
    partitions = parse_partitions(lines)
    tests = error_(partitions, segment)
    lines = format_partitions(tests)
    stdout_lines(lines)


def run_command(args):
    segment = ZOO[args.segment]
    lines = stdin_lines()
    partitions = parse_partitions(lines)
    partitions = update_partitions(partitions, segment)
    lines = format_partitions(partitions)
    stdout_lines(lines)


def show_guess(guess, etalon):
    print('---etalon')
    for _ in etalon:
        print('>', _.text)
    print('---guess')
    for _ in guess:
        print('>', _.text)
    print()


def show_command(args):
    segment = ZOO[args.segment]
    lines = stdin_lines()
    tests = parse_partitions(lines)
    for test in tests:
        guess = list(segment(test.as_text))
        etalon = list(test.as_substrings)
        show_guess(guess, etalon)


def main():
    parser = argparse.ArgumentParser(prog='ctl')
    parser.set_defaults(function=None)

    sub = parser.add_subparsers()

    generate = sub.add_parser('gen')
    generate.set_defaults(function=generate_command)

    sample = sub.add_parser('sample')
    sample.set_defaults(function=sample_command)
    sample.add_argument('size', type=int)
    sample.add_argument('--seed', type=int, default=1)

    error = sub.add_parser('err')
    error.set_defaults(function=error_command)
    error.add_argument('segment', choices=ZOO)

    run = sub.add_parser('run')
    run.set_defaults(function=run_command)
    run.add_argument('segment', choices=ZOO)

    show = sub.add_parser('show')
    show.set_defaults(function=show_command)
    show.add_argument('segment', choices=ZOO)

    args = sys.argv[1:]
    args = parser.parse_args(args)
    if not args.function:
        parser.print_help()
        parser.exit()
    try:
        args.function(args)
    except (BrokenPipeError, IOError):
        pass


if __name__ == '__main__':
    main()
