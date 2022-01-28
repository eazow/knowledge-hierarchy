import sys

import pygame

from grid import Grid, valid_space
from piece import get_shape, convert_shape_format
from conf import window_width, window_height, play_width, play_height, fall_speed

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


def draw_next_shape(shape, surface):
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


def handle_event(current_piece, event):
    if event.type == pygame.QUIT:
        pygame.display.quit()
        quit()
        sys.exit(0)
    if event.type == pygame.KEYDOWN:
        handle_keydown(current_piece, event)


def handle_keydown(current_piece, event):
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
        current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
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


class ScoreRecorder:
    def __init__(self):
        self.score = 0

    def add_score(self):
        self.score += 10


class Game(ScoreRecorder):
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Tetris")
        self.window = pygame.display.set_mode((window_width, window_height))

        self.current_piece = get_shape()
        self.next_piece = get_shape()
        self.change_piece = False
        self.grid = None
        self.fall_time = 0
        self.locked_positions = {}  # (x,y):(255,0,0)

    def start(self):
        clock = pygame.time.Clock()

        while True:
            self.grid = Grid.create(self.locked_positions)
            self.fall_time += clock.get_rawtime()

            clock.tick()

            self.fall_piece()

            [handle_event(self.current_piece, event) for event in pygame.event.get()]

            shape_pos = convert_shape_format(self.current_piece)

            # add piece to the grid for drawing
            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    self.grid[y][x] = self.current_piece.color

            # IF PIECE HIT GROUND
            if self.change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    self.locked_positions[p] = self.current_piece.color
                self.current_piece = self.next_piece
                self.next_piece = get_shape()
                self.change_piece = False

                # call four times to check for multiple clear rows
                if clear_rows(self.grid, self.locked_positions):
                    self.add_score()

            self.draw_window()
            draw_next_shape(self.next_piece, self.window)
            pygame.display.update()

            if is_game_over(self.locked_positions):
                break

        self.draw_text_middle("You Lost", 40, (255, 255, 255))
        pygame.display.update()
        pygame.time.delay(2000)

    def fall_piece(self):
        if self.fall_time >= 1000 * fall_speed:
            self.fall_time = 0

            self.current_piece.y += 1
            if (
                not (valid_space(self.current_piece, self.grid))
                and self.current_piece.y > 0
            ):
                self.current_piece.y -= 1
                self.change_piece = True

    def draw_window(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                pygame.draw.rect(
                    self.window,
                    self.grid[i][j],
                    (top_left_x + j * 30, top_left_y + i * 30, 30, 30),
                    0,
                )

        # draw grid and border
        Grid.draw(self.window, 20, 10, top_left_x, top_left_y)
        pygame.draw.rect(
            self.window, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 1
        )
        # pygame.display.update()

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


if __name__ == "__main__":
    Game().start()
