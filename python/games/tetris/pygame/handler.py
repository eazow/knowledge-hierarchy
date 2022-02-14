import sys

import pygame

from grid import valid_space


def handle_key_down(current_block, grid):
    current_block.y += 1
    if not valid_space(current_block, grid):
        current_block.y -= 1


def handle_key_space(current_block, grid):
    while valid_space(current_block, grid):
        current_block.y += 1
    current_block.y -= 1


def handle_key_up(current_block, grid): # rotate shape
    current_block.rotation = current_block.rotation + 1 % len(
        current_block.shape
    )
    if not valid_space(current_block, grid):
        current_block.rotation = current_block.rotation - 1 % len(
            current_block.shape
        )


def handle_key_right(current_block, grid):
    current_block.x += 1
    if not valid_space(current_block, grid):
        current_block.x -= 1


def handle_key_left(current_block, grid):
    current_block.x -= 1
    if not valid_space(current_block, grid):
        current_block.x += 1


def handle_event(event, grid, block):
    if event.type == pygame.QUIT:
        pygame.display.quit()
        quit()
        sys.exit(0)
    if event.type == pygame.KEYDOWN:
        handler_registry.get(event.key)(block, grid)


handler_registry = {
    pygame.K_LEFT: handle_key_left,
    pygame.K_RIGHT: handle_key_right,
    pygame.K_UP: handle_key_up,
    pygame.K_DOWN: handle_key_down,
    pygame.K_SPACE: handle_key_space
}
