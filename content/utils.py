import copy
import unittest

class FreezedParam():
    def __init__(self, value):
        self.value = value

    def __enter__(self):
        self.passed_reference = copy.deepcopy(self.value)
        return self.passed_reference

    def __exit__(self, *args):
        assert self.passed_reference == self.value, "Should not mutate function parameter"


def grade_test(test_class, returns=False):
    test = unittest.main(argv=[''],defaultTest=test_class.__name__, verbosity=0, exit=False)
    total = test.result.testsRun
    fails = len(test.result.failures)
    score = total - fails
    percentage = int(float(score)/float(total) * 100)
    result = (total, score, fails, percentage)
    if returns:
        return result
    else:
        print("==========")
        print(f"Score of {test_class.__name__}: {score}/{total} ({percentage}%)")
        print("==========")

def grade_tests(test_classes):
    results = [grade_test(test_class, returns=True) for test_class in test_classes]
    print("==========")
    for test_class, (total, score, fails, percentage) in zip(test_classes, results):
        print(f"Score of {test_class.__name__}: {score}/{total} ({percentage}%)")
    print("==========")


def assert_eq(actual, expected):
    assert actual == expected, f"expect:\n{expected}\n\nactual:\n{actual}"


def assert_next_grid(actual, alike):
    """
    For testing grid after putting a new number in random location.

    for each item in alike:
        if the item is not None:
            corresponding item in actual grid should have the same value

    and there exists one and only one item in alike that is None, and its corresponding item in actual grid is either 2 or 4
    """
    extra = (sum(filterna(flatten(actual))) - sum(filterna(flatten(alike))))
    assert extra in [2, 4], f"actual should contain one and only one extra 2 or 4, but got {extra}"
    for i in range(16):
        rowid = i // 4
        colid = i % 4
        if alike[rowid][colid] is not None:
            assert alike[rowid][colid] == actual[rowid][colid], f"at ({rowid}, {colid}), expect {alike[rowid][colid]}, actual {actual[rowid][colid]}"
        elif actual[rowid][colid] is not None:
            assert actual[rowid][colid] == extra, f"extra digit should be {extra}, but got {actual[rowid][colid]}"


def assert_next_state(actual, expected):
    assert_eq(actual['result'], expected['result'])
    assert_next_grid(actual['grid'], expected['grid'])


def create_empty_row():
    return [None, None, None, None]


def create_empty_grid():
    return [
        create_empty_row(),
        create_empty_row(),
        create_empty_row(),
        create_empty_row()
    ]

def flatten(grid):
    """
    Convert 2d array to 1d

    example input:
    grid = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10,11,12],
        [13,14,15,16]
    ]

    output:
    [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    """
    return [it for row in grid for it in row]

assert_eq(flatten([
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10,11,12],
        [13,14,15,16]
    ]), [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])

def filterna(array):
    """
    Drop the `None`s in the array

    example input:
    array = [1, 2, None, 3, 4, None, 5]

    output:
    [1,2,3,4,5]
    """
    return [it for it in array if it is not None]

assert_eq(filterna([1, 2, None, 3, 4, None, 5]), [1,2,3,4,5])