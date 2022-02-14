import sys

import pygame

from grid import Grid, valid_space
from conf import window_width, window_height, play_width, play_height, fall_speed
from block import Block
from handler import handler_registry
from mixins import ScoreRecorder, ClockMixin, PygameMixin
from drawer import Drawer


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


class Game(ClockMixin, ScoreRecorder, PygameMixin):
    def __init__(self):
        super(Game, self).__init__()

        self.current_block = Block.create()
        self.next_block = Block.create()
        self.is_changing = False
        self.grid = None
        self.fall_time = 0
        self.locked_positions = {}

        self.drawer = Drawer(pygame.display.set_mode((window_width, window_height)))

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

            self.drawer.draw_window(self.grid)
            self.drawer.draw_next_block(self.next_block)
            pygame.display.update()

            if Grid.is_game_over(self.locked_positions):
                break

        self.lost()

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

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.display.quit()
            quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            handler_registry.get(event.key)(self.current_block, self.grid)

    def lost(self):
        self.drawer.draw_text(
            "You Lost",
            40,
            (255, 255, 255),
            play_width / 2,
            play_height / 2,
        )
        pygame.display.update()
        # pygame.time.delay(2000)


if __name__ == "__main__":
    Game().start()
