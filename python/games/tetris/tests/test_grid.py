from conf import rows
from grid import Grid
from tetromino import BlockO


def test_grid():
    grid = Grid()
    grid.current_block = BlockO(5, 0)

    grid.current_block.fall()
    grid.update()

    assert grid.colors_by_row_col[0][4] == BlockO.color
    assert grid.colors_by_row_col[0][5] == BlockO.color


def test_hit_bottom():
    grid = Grid()
    grid.current_block = BlockO(5, 0)

    [grid.current_block.fall() for _ in range(rows)]
    grid.update()

