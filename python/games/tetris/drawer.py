import pygame

from conf import grid_width, grid_height, window_height, window_width, rows, cols, cell_size


class Drawer:
    def __init__(self):
        self.window = pygame.display.set_mode((window_width, window_height))

    def draw_window(self, colors_by_row_col):
        for row in range(len(rows)):
            for col in range(len(cols)):
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
        font = pygame.font.SysFont("comicsans", 30)
        label = font.render("Next Shape", True, (255, 255, 255))

        sx = grid_width + 50
        sy = 50

        for i, line in enumerate(block.coordinates):
            row = list(line)
            for j, column in enumerate(row):
                if column == "0":
                    pygame.draw.rect(
                        self.window, block.color.value, (sx + j * 30, sy + i * 30, 30, 30), 0
                    )

        self.window.blit(label, (sx + 10, sy - 30))

    def draw_grid(self):
        pygame.draw.rect(self.window, (255, 0, 0), (0, 0, grid_width, grid_height), 1)
