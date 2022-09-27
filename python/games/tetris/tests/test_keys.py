from colors import Color
from conf import rows
from grid import Grid
from handler import handle_key_space, handle_key_left, handle_key_up
from tetromino import BlockO


def test_key_space():
    grid = Grid()
    grid.current_block = BlockO(3, -4)

    handle_key_space(grid)

    assert grid.colors[rows - 3][4] == Color.BLACK
    assert grid.colors[rows - 3][5] == Color.BLACK
    assert grid.colors[rows - 2][4] == BlockO.color
    assert grid.colors[rows - 2][5] == BlockO.color
    assert grid.colors[rows - 1][4] == BlockO.color
    assert grid.colors[rows - 1][5] == BlockO.color


def test_key_left():
    grid = Grid()
    grid.current_block = BlockO(5, 0)

    grid.fall_block()
    grid.fall_block()

    handle_key_left(grid)
    grid.update_colors()

    assert grid.colors[0][5] == Color.BLACK
    assert grid.colors[1][5] == Color.BLACK

    assert grid.colors[0][3] == BlockO.color
    assert grid.colors[0][4] == BlockO.color
    assert grid.colors[1][3] == BlockO.color
    assert grid.colors[1][4] == BlockO.color


def test_key_up():
    grid = Grid()
    grid.current_block = BlockO(3, -3)

    grid.fall_block()
    grid.fall_block()

    handle_key_up(grid)
    grid.update_colors()

    assert grid.colors[0][4] == BlockO.color
    assert grid.colors[0][5] == BlockO.color
    assert grid.colors[1][4] == BlockO.color
    assert grid.colors[1][5] == BlockO.color


def test_key_left():
    grid = Grid()
    grid.current_block = BlockO(0, 0)
    grid.fall_block()

    handle_key_left(grid)
    handle_key_left(grid)

    assert grid.current_block.col == -1

