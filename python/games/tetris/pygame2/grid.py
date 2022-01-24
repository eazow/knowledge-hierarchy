import pygame
from conf import play_width, play_height
from tetris import top_left_x, top_left_y


class Grid:
    @classmethod
    def draw(surface, row, col):
        sx = top_left_x
        sy = top_left_y
        for i in range(row):
            pygame.draw.line(
                surface,
                (128, 128, 128),
                (sx, sy + i * 30),
                (sx + play_width, sy + i * 30),
            )  # horizontal lines
            for j in range(col):
                pygame.draw.line(
                    surface,
                    (128, 128, 128),
                    (sx + j * 30, sy),
                    (sx + j * 30, sy + play_height),
                )  # vertical lines
