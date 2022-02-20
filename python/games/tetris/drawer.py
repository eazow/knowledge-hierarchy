import pygame

from conf import (
    grid_width,
    grid_height,
    window_height,
    window_width,
    rows,
    cols,
    cell_size,
    Color,
)


class Drawer:
    def __init__(self, grid):
        self.grid = grid
        self.window = pygame.display.set_mode((window_width, window_height))

    def draw_grid(self, colors_by_row_col):
        for row in range(rows):
            for col in range(cols):
                self.draw_rect(
                    colors_by_row_col[row][col].value,
                    (col * cell_size, row * cell_size, cell_size, cell_size),
                )

        pygame.draw.line(
            self.window,
            Color.CHARCOAL.value,
            (grid_width, 0),
            (grid_width, grid_height),
            1,
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

        label = font.render(text, True, (100, 255, 100))

        pos = (
            x - (label.get_width() / 2),
            y - label.get_height() / 2,
        )
        self.window.blit(label, pos)

    def draw_next_block(self, block):
        font = pygame.font.SysFont("comicsansms", 30)
        text = font.render("Next Shape", True, Color.WHITE.value, Color.BLACK.value)

        sx = grid_width + 50
        sy = 150

        for i, line in enumerate(block.coordinates):
            row = list(line)
            for j, column in enumerate(row):
                if column == "0":
                    self.draw_rect(
                        block.color.value,
                        (sx + j * 30, sy + i * 30, cell_size, cell_size),
                    )

        self.window.blit(text, (grid_width + 20, 20))

    def draw(self):
        self.draw_grid(self.grid.colors_by_row_col)
        self.draw_next_block(self.grid.next_block)
        pygame.display.update()
