import pygame
from conf import play_width, play_height


class Grid:
    @classmethod
    def draw(cls, surface, row, col, top_left_x, top_left_y):
        for i in range(row):
            pygame.draw.line(
                surface,
                (128, 128, 128),
                (top_left_x, top_left_y + i * 30),
                (top_left_x + play_width, top_left_y + i * 30),
            )  # horizontal lines
            for j in range(col):
                pygame.draw.line(
                    surface,
                    (128, 128, 128),
                    (top_left_x + j * 30, top_left_y),
                    (top_left_x + j * 30, top_left_y + play_height),
                )  # vertical lines


def create_grid(locked_positions={}):
    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] = locked_positions.get((j, i), grid[i][j])

    return grid