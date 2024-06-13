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
    assert extra in [2, 4], "actual should contain one and only one extra 2 or 4"
    for i in range(16):
        rowid = i // 4
        colid = i % 4
        if alike[rowid][colid] is not None:
            assert alike[rowid][colid] == actual[rowid][colid], f"at ({rowid}, {colid}), expect {alike[rowid][colid]}, actual {actual[rowid][colid]}"
        elif actual[rowid][colid] is not None:
            assert actual[rowid][colid] == extra, "actual should contain one and only one extra 2 or 4"


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