import pygame

from python.games.tetris.grid import Grid
from python.games.tetris.conf import grid_width, grid_height
from python.games.tetris.handler import handle_event
from python.games.tetris.mixins import ScoreRecorder, ClockMixin, PygameMixin
from python.games.tetris.drawer import Drawer


class Game(PygameMixin, ClockMixin, ScoreRecorder):
    def __init__(self):
        super(Game, self).__init__()

        self.grid = Grid()

        self.drawer = Drawer()

    def start(self):
        while self.grid.is_game_over():
            self.grid.update_locked(self.locked_positions)
            self.grid.fall_time += self.clock.get_rawtime()

            self.clock.tick()

            self.grid.fall_piece()

            [handle_event(event, self.grid, self.grid.current_block) for event in pygame.event.get()]

            shape_pos = self.current_block.coordinates()
            self.grid.update(shape_pos)
            self.grid.check_rows(shape_pos)

            self.drawer.draw_window(self.grid)
            self.drawer.draw_next_block(self.grid.next_block)
            pygame.display.update()

        self.lost()

    def lost(self):
        self.drawer.draw_text(
            "You Lost",
            40,
            (255, 255, 255),
            grid_width / 2,
            grid_height / 2,
        )
        pygame.display.update()
        pygame.time.delay(2000)


if __name__ == "__main__":
    Game().start()
