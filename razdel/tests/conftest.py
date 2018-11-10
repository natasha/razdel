# coding: utf-8
from __future__ import unicode_literals


def pytest_assertrepr_compare(op, left, right):
    # add one more line for "assert ..."
    return (
        ['']
        + ['---']
        + ['> ' + _.text for _ in left]
        + ['---']
        + ['> ' + _.text for _ in right]
    )


def pytest_addoption(parser):
    parser.addoption('--int', action='store_true')


def pytest_generate_tests(metafunc):
    if 'int_test' in metafunc.fixturenames:
        tests = []
        if metafunc.config.getoption('int'):
            tests = metafunc.module.int_tests()
        metafunc.parametrize('int_test', tests)
