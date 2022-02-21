from conf import rows
from colors import Color
from grid import Grid
from handler import handle_key_space
from tetromino import BlockO, BlockL


def test_fall():
    grid = Grid()
    grid.current_block = BlockO(5, 0)

    grid.fall_block()

    assert grid.colors_by_row_col[0][4] == BlockO.color
    assert grid.colors_by_row_col[0][5] == BlockO.color

    grid.fall_block()
    grid.fall_block()

    assert grid.colors_by_row_col[0][4] == Color.BLACK
    assert grid.colors_by_row_col[0][5] == Color.BLACK
    assert grid.colors_by_row_col[1][4] == BlockO.color
    assert grid.colors_by_row_col[1][5] == BlockO.color


def test_hit_bottom():
    grid = Grid()
    grid.current_block = BlockO(5, 0)

    [grid.fall_block() for _ in range(rows + 1)]

    assert grid.colors_by_row_col[rows - 1][4] == BlockO.color
    assert grid.colors_by_row_col[rows - 1][5] == BlockO.color
    assert grid.colors_by_row_col[rows - 2][4] == BlockO.color
    assert grid.colors_by_row_col[rows - 2][5] == BlockO.color

    assert grid.locked_positions[(4, rows - 1)]
    assert grid.locked_positions[(5, rows - 1)]


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

    print(grid.locked_positions)
    assert grid.locked_positions != {}
    assert grid.check_rows() == 2

    print(grid.locked_positions)
    assert grid.locked_positions.keys() == {(4, 19), (5, 19), (6, 19), (6, 18)}
