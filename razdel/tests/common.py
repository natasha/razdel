
import os
from random import seed, sample


def run(segment, test):
    guess = list(segment.debug(test.as_text))
    etalon = list(test.as_substrings)
    assert guess == etalon


def data_path(filename):
    return os.path.join(
        os.path.dirname(__file__),
        'data',
        filename
    )


def data_lines(path, size):
    lines = load_lines(path)
    seed(1)
    return sample(list(lines), size)
