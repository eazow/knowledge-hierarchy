import sys

import pygame

from grid import Grid, valid_space
from conf import window_width, window_height, play_width, play_height, fall_speed
from block import Block

top_left_x = 0
top_left_y = 0


def is_game_over(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one

    inc = 0
    for i in range(len(grid) - 1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except BaseException:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)


def draw_next_block(shape, surface):
    font = pygame.font.SysFont("comicsans", 30)
    # font = pygame.font.Font(None, 30)

    label = font.render("Next Shape", True, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    sy = top_left_y + 50
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                pygame.draw.rect(
                    surface, shape.color, (sx + j * 30, sy + i * 30, 30, 30), 0
                )

    surface.blit(label, (sx + 10, sy - 30))


class ScoreRecorder:
    def __init__(self):
        self.score = 0

    def add_score(self):
        self.score += 10


class ClockMixin:
    def __init__(self):
        self.clock = pygame.time.Clock()


class Game(ClockMixin, ScoreRecorder):
    def __init__(self):
        super(Game, self).__init__()

        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Tetris")
        self.window = pygame.display.set_mode((window_width, window_height))

        self.current_block = Block.create()
        self.next_block = Block.create()
        self.is_changing = False
        self.grid = None
        self.fall_time = 0
        self.locked_positions = {}

    def start(self):
        while True:
            self.grid = Grid.create(self.locked_positions)
            self.fall_time += self.clock.get_rawtime()

            self.clock.tick()

            self.fall_piece()

            [self.handle_event(event) for event in pygame.event.get()]

            shape_pos = self.current_block.convert_shape_format()

            self.update_grid(shape_pos)

            self.check_rows(shape_pos)

            self.draw_window()
            draw_next_block(self.next_block, self.window)
            pygame.display.update()

            if is_game_over(self.locked_positions):
                break

        self.draw_text_middle("You Lost", 40, (255, 255, 255))
        pygame.display.update()
        # pygame.time.delay(2000)

    def update_grid(self, shape_pos):
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                self.grid[y][x] = self.current_block.color

    def check_rows(self, shape_pos):
        if self.is_changing:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                self.locked_positions[p] = self.current_block.color
            self.current_block = self.next_block
            self.next_block = Block.create()
            self.is_changing = False

            # call four times to check for multiple clear rows
            if clear_rows(self.grid, self.locked_positions):
                self.add_score()

    def fall_piece(self):
        if self.fall_time >= 1000 * fall_speed:
            self.fall_time = 0

            self.current_block.y += 1
            if (
                not (valid_space(self.current_block, self.grid))
                and self.current_block.y > 0
            ):
                self.current_block.y -= 1
                self.is_changing = True

    def draw_window(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                pygame.draw.rect(
                    self.window,
                    self.grid[i][j],
                    (top_left_x + j * 30, top_left_y + i * 30, 30, 30),
                    0,
                )

        Grid.draw(self.window, 20, 10, top_left_x, top_left_y)

    def draw_text_middle(self, text, size, color):
        font = pygame.font.SysFont("comicsans", size, bold=True)
        label = font.render(text, 1, color)

        self.window.blit(
            label,
            (
                top_left_x + play_width / 2 - (label.get_width() / 2),
                top_left_y + play_height / 2 - label.get_height() / 2,
            ),
        )

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.display.quit()
            quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)

    def handle_keydown(self, event):
        current_piece = self.current_block
        grid = self.grid

        if event.key == pygame.K_LEFT:
            current_piece.x -= 1
            if not valid_space(current_piece, grid):
                current_piece.x += 1

        elif event.key == pygame.K_RIGHT:
            current_piece.x += 1
            if not valid_space(current_piece, grid):
                current_piece.x -= 1
        elif event.key == pygame.K_UP:
            # rotate shape
            current_piece.rotation = current_piece.rotation + 1 % len(
                current_piece.shape
            )
            if not valid_space(current_piece, grid):
                current_piece.rotation = current_piece.rotation - 1 % len(
                    current_piece.shape
                )
        if event.key == pygame.K_DOWN:
            # move shape down
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
        """if event.key == pygame_.K_SPACE:
                        while valid_space(current_piece, grid):
                            current_piece.y += 1
                        current_piece.y -= 1
                        print(convert_shape_format(current_piece))"""  # todo fix


if __name__ == "__main__":
    Game().start()