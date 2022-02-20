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
    def __init__(self):
        self.window = pygame.display.set_mode((window_width, window_height))

    def draw_window(self, colors_by_row_col):
        for row in range(rows):
            for col in range(cols):
                pygame.draw.rect(
                    self.window,
                    colors_by_row_col[row][col].value,
                    (col * cell_size, row * cell_size, cell_size, cell_size),
                    0,
                )

        self.draw_grid()

    def draw_text(self, text, size, x, y):
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
        sy = 50

        for i, line in enumerate(block.coordinates):
            row = list(line)
            for j, column in enumerate(row):
                if column == "0":
                    pygame.draw.rect(
                        self.window,
                        block.color.value,
                        (sx + j * 30, sy + i * 30, cell_size, cell_size),
                        0,
                    )

        self.window.blit(text, (grid_width + 20, 20))

    def draw_grid(self):
        # pygame.draw.rect(self.window, (255, 0, 0), (0, 0, grid_width, grid_height), 1)
        pygame.draw.line(self.window, Color.JET.value, (300, 0), (300, 600), 1)
