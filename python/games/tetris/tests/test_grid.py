from conf import rows, cols
from colors import Color
from grid import Grid
from handler import handle_key_space
from tetromino import BlockO, BlockL, BlockI


def test_fall():
    grid = Grid()
    grid.current_block = BlockO(5, 0)

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
    grid.current_block = BlockO(5, 0)

    [grid.fall_block() for _ in range(rows + 1)]

    assert grid.colors[rows - 1][4] == BlockO.color
    assert grid.colors[rows - 1][5] == BlockO.color
    assert grid.colors[rows - 2][4] == BlockO.color
    assert grid.colors[rows - 2][5] == BlockO.color

    assert grid.locks[(4, rows - 1)]
    assert grid.locks[(5, rows - 1)]


def test_clear_rows():
    grid = Grid()
    grid.current_block = BlockO(1, 0)
    [grid.fall_block() for _ in range(rows + 1)]

    grid.current_block = BlockO(3, 0)
    [grid.fall_block() for _ in range(rows + 1)]

    grid.current_block = BlockO(5, 0)
    [grid.fall_block() for _ in range(rows + 1)]

    grid.current_block = BlockO(7, 0)
    [grid.fall_block() for _ in range(rows + 1)]

    grid.current_block = BlockL(5, 0)
    handle_key_space(grid)

    grid.current_block = BlockO(9, 0)
    [grid.fall_block() for _ in range(rows + 1)]

    assert grid.locks != {}
    assert grid.check_rows() == 2

    assert grid.locks.keys() == {(4, 19), (5, 19), (6, 19), (6, 18)}


def test_clear_alternate_rows():
    grid = Grid()
    for col in range(cols):
        grid.locks[(col, 16)] = Color.BLUE
        grid.locks[(col, 17)] = Color.BLUE
        grid.locks[(col, 18)] = Color.BLUE
        grid.locks[(col, 19)] = Color.BLUE

    del grid.locks[(8, 16)]
    del grid.locks[(8, 18)]

    grid.is_changing = True
    grid.update_colors()
    grid.check_rows()

    assert grid.locks[(0, 19)] == Color.BLUE
    assert grid.locks[(9, 19)] == Color.BLACK

