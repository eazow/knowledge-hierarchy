import pygame
from python.games.tetris.conf import grid_width, grid_height, window_height, window_width


class Drawer:
    def __init__(self):
        self.window = pygame.display.set_mode((window_width, window_height))

    def draw_window(self, grid):
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(
                    self.window,
                    grid[i][j],
                    (j * 30, i * 30, 30, 30),
                    0,
                )

        self.draw_grid(20, 10)

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.SysFont("comicsansms", size, bold=True)
        # font = pygame.font.SysFont("arial", 16)
        print(pygame.font.get_fonts())

        label = font.render(text, True, (100, 255, 100))

        pos = (
            x - (label.get_width() / 2),
            y - label.get_height() / 2,
        )
        self.window.blit(label, pos)

    def draw_next_block(self, shape, surface):
        font = pygame.font.SysFont("comicsans", 30)
        label = font.render("Next Shape", True, (255, 255, 255))

        sx = grid_width + 50
        sy = 50
        format = shape.shapes[shape.rotation % len(shape.shapes)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == "0":
                    pygame.draw.rect(
                        surface, shape.color, (sx + j * 30, sy + i * 30, 30, 30), 0
                    )

        surface.blit(label, (sx + 10, sy - 30))

    def draw_grid(self):
        pygame.draw.rect(self.window, (255, 0, 0), (0, 0, grid_width, grid_height), 1)
