

def pytest_assertrepr_compare(op, left, right):
    # add one more line for "assert ..."
    return (
        ['']
        + ['---']
        + ['> ' + _.text for _ in left]
        + ['---']
        + ['> ' + _.text for _ in right]
    )
