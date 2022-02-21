import sys

import pygame


def handle_key_down(grid):
    grid.current_block.row += 1
    if not grid.valid_space():
        grid.current_block.row -= 1


def handle_key_space(grid):
    while grid.valid_space():
        grid.current_block.row += 1
    grid.current_block.row -= 1


def handle_key_up(grid):  # rotate shape
    grid.current_block.rotation = (grid.current_block.rotation + 1) % len(grid.current_block.shapes)
    if not grid.valid_space():
        grid.current_block.rotation = grid.current_block.rotation - 1 % len(grid.current_block.shapes)


def handle_key_right(grid):
    grid.current_block.col += 1
    if not grid.valid_space():
        grid.current_block.col -= 1


def handle_key_left(grid):
    grid.current_block.col -= 1
    if not grid.valid_space():
        grid.current_block.col += 1


def handle_event(event, grid):
    if event.type == pygame.QUIT:
        pygame.display.quit()
        quit()
        sys.exit(0)
    if event.type == pygame.KEYDOWN:
        handler_registry.get(event.key)(grid)


def handle_events(grid):
    [handle_event(event, grid) for event in pygame.event.get()]


handler_registry = {
    pygame.K_LEFT: handle_key_left,
    pygame.K_RIGHT: handle_key_right,
    pygame.K_UP: handle_key_up,
    pygame.K_DOWN: handle_key_down,
    pygame.K_SPACE: handle_key_space,
}
