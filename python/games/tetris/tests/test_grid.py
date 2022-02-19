from conf import rows, Color
from grid import Grid
from tetromino import BlockO


def test_grid():
    grid = Grid()
    grid.current_block = BlockO(5, 0)

    grid.current_block.fall()

    assert grid.colors_by_row_col[0][4] == BlockO.color
    assert grid.colors_by_row_col[0][5] == BlockO.color


def test_hit_bottom():
    grid = Grid()
    grid.current_block = BlockO(5, 0)

    [grid.fall_block() for _ in range(rows)]


def test_fall():
    grid = Grid()
    grid.current_block = BlockO(5, 0)

    grid.fall_block()
    grid.fall_block()
    grid.fall_block()

    assert grid.colors_by_row_col[0][4] == Color.BLACK
    assert grid.colors_by_row_col[0][5] == Color.BLACK
    assert grid.colors_by_row_col[1][4] == BlockO.color
    assert grid.colors_by_row_col[1][5] == BlockO.color


