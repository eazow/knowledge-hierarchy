from conf import rows, cols
from colors import Color
from grid import Grid
from handler import handle_key_space
from tetromino import BlockO, BlockL, BlockI


def test_fall():
    grid = Grid()
    grid.current_block = BlockO(3, -3)

    grid.fall_block()

    assert grid.colors[0][4] == BlockO.color
    assert grid.colors[0][5] == BlockO.color

    grid.fall_block()
    grid.fall_block()

    assert grid.colors[0][4] == Color.BLACK
    assert grid.colors[0][5] == Color.BLACK
    assert grid.colors[1][4] == BlockO.color
    assert grid.colors[1][5] == BlockO.color


def test_hit_bottom():
    grid = Grid()
    grid.current_block = BlockO(3, -4)

    [grid.fall_block() for _ in range(rows + 2)]

    assert grid.colors[rows - 1][4] == BlockO.color
    assert grid.colors[rows - 1][5] == BlockO.color
    assert grid.colors[rows - 2][4] == BlockO.color
    assert grid.colors[rows - 2][5] == BlockO.color

    assert grid.locks[(4, rows - 1)]
    assert grid.locks[(5, rows - 1)]


def test_clear_rows():
    grid = Grid()
    grid.current_block = BlockO(-1, 0)
    [grid.fall_block() for _ in range(rows + 1)]

    grid.current_block = BlockO(1, 0)
    [grid.fall_block() for _ in range(rows + 1)]

    grid.current_block = BlockO(3, 0)
    [grid.fall_block() for _ in range(rows + 1)]

    grid.current_block = BlockO(5, 0)
    [grid.fall_block() for _ in range(rows + 1)]

    grid.current_block = BlockL(4, 0)
    handle_key_space(grid)

    grid.current_block = BlockO(7, 0)
    [grid.fall_block() for _ in range(rows + 1)]

    assert grid.locks != {}
    assert grid.check_rows() == 2

    assert grid.locks.keys() == {
        (4, rows - 1),
        (5, rows - 1),
        (6, rows - 1),
        (6, rows - 2),
    }


def test_clear_alternate_rows():
    grid = Grid()
    for col in range(cols):
        for row in range(rows-4, rows):
            grid.locks[(col, row)] = Color.BLUE
    del grid.locks[(9, rows-4)]
    del grid.locks[(9, rows-2)]

    grid.is_changing = True
    cleared_rows = grid.check_rows()

    for col in range(cols - 1):
        assert grid.locks[(col, rows-2)] == Color.BLUE
        assert grid.locks[(col, rows-1)] == Color.BLUE
    assert (7, rows-3) not in grid.locks
    assert (9, rows-2) not in grid.locks
    assert (9, rows-1) not in grid.locks
    assert 2 == cleared_rows
