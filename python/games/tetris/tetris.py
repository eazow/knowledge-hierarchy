import pygame

from python.games.tetris.grid import Grid
from python.games.tetris.conf import grid_width, grid_height
from python.games.tetris.handler import handle_event
from python.games.tetris.mixins import ScoreRecorder, ClockMixin, PygameMixin
from python.games.tetris.drawer import Drawer


class Game(PygameMixin, ClockMixin, ScoreRecorder):
    def __init__(self):
        super(Game, self).__init__()
        ClockMixin.__init__(self)
        ScoreRecorder.__init__(self)

        self.grid = Grid()

        self.drawer = Drawer()

    def start(self):
        while not self.grid.is_game_over():
            self.grid.update_colors()

            if self.can_fall():
                self.grid.fall_block()

            [handle_event(event, self.grid) for event in pygame.event.get()]

            self.grid.check_rows()

            self.drawer.draw_grid(self.grid.colors_by_row_col)
            self.drawer.draw_next_block(self.grid.next_block)
            pygame.display.update()

        self.lost()

    def lost(self):
        self.drawer.draw_text(
            "You Lost",
            40,
            grid_width / 2,
            grid_height / 2,
        )
        pygame.display.update()
        # pygame.time.delay(2000)


if __name__ == "__main__":
    Game().start()
