from colors import Color
from conf import rows
from grid import Grid
from handler import handle_key_space, handle_key_left
from tetromino import BlockO


def test_key_space():
    grid = Grid()
    grid.current_block = BlockO(5, 0)

    handle_key_space(grid)
    grid.update_colors()

    assert grid.colors_by_row_col[rows - 3][4] == Color.BLACK
    assert grid.colors_by_row_col[rows - 3][5] == Color.BLACK
    assert grid.colors_by_row_col[rows - 2][5] == BlockO.color
    assert grid.colors_by_row_col[rows - 2][5] == BlockO.color
    assert grid.colors_by_row_col[rows - 1][4] == BlockO.color
    assert grid.colors_by_row_col[rows - 1][5] == BlockO.color


def test_key_left():
    grid = Grid()
    grid.current_block = BlockO(5, 0)

    grid.fall_block()
    grid.fall_block()

    handle_key_left(grid)
    grid.update_colors()

    assert grid.colors_by_row_col[0][5] == Color.BLACK
    assert grid.colors_by_row_col[1][5] == Color.BLACK

    assert grid.colors_by_row_col[0][3] == BlockO.color
    assert grid.colors_by_row_col[0][4] == BlockO.color
    assert grid.colors_by_row_col[1][3] == BlockO.color
    assert grid.colors_by_row_col[1][4] == BlockO.color
