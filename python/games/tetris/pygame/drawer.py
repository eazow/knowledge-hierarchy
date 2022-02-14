import pygame
from conf import play_width, play_height


class Drawer:
    def __init__(self, window):
        self.window = window

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
        font = pygame.font.SysFont("comicsans", size, bold=True)
        label = font.render(text, 1, color)

        self.window.blit(
            label,
            (
                x - (label.get_width() / 2),
                y - label.get_height() / 2,
            ),
        )

    def draw_next_block(self, shape, surface):
        font = pygame.font.SysFont("comicsans", 30)

        label = font.render("Next Shape", True, (255, 255, 255))

        sx = play_width + 50
        sy = 50
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == "0":
                    pygame.draw.rect(
                        surface, shape.color, (sx + j * 30, sy + i * 30, 30, 30), 0
                    )

        surface.blit(label, (sx + 10, sy - 30))

    def draw_grid(self):
        pygame.draw.rect(
            self.window, (255, 0, 0), (0, 0, play_width, play_height), 1
        )
