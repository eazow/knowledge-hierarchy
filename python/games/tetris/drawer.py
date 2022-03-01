import pygame

from conf import (
    grid_width,
    grid_height,
    window_height,
    window_width,
    rows,
    cols,
    cell_size,
)
from colors import Color


class Drawer:
    def __init__(self, grid):
        self.grid = grid
        self.colors = str(grid.colors)
        self.window = pygame.display.set_mode((window_width, window_height))

    def draw_grid(self):
        for row in range(rows):
            for col in range(cols):
                self.draw_rect(
                    self.grid.colors[row][col].value,
                    (col * cell_size, row * cell_size, cell_size, cell_size),
                )

    def draw_rect(self, color, rect):
        pygame.draw.rect(
            self.window,
            color,
            rect,
            0,
        )

    def draw_text(self, text, size, x, y):  # deprecated
        font = pygame.font.SysFont("comicsansms", size, bold=True)

        label = font.render(text, True, Color.WHITE.value, Color.BLACK.value)

        x = x - label.get_width() / 2
        y = y - label.get_height() / 2
        self.window.blit(label, (x, y))

    def draw_side_panel(self):
        self.draw_text(
            "Next Shape", 25, grid_width + (window_width - grid_width) / 2, 10
        )

        x, y = grid_width + 20, 50
        self.draw_block(self.grid.next_block, x, y)

    def draw_block(self, block, x, y):
        for i, line in enumerate(block.shapes[block.rotation]):
            for j, col in enumerate(list(line)):
                rect = (x + j * cell_size, y + i * cell_size, cell_size, cell_size)
                color = block.color if col == "0" else Color.BLACK
                self.draw_rect(color.value, rect)

    def draw_split_line(self):
        pygame.draw.line(
            self.window,
            Color.CHARCOAL.value,
            (grid_width, 0),
            (grid_width, grid_height),
            1,
        )

    def draw(self):
        if self.colors != str(self.grid.colors):
            self.draw_grid()
            self.draw_split_line()
            self.draw_side_panel()

            self.colors = str(self.grid.colors)

            pygame.display.update()
