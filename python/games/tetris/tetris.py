import pygame

from python.games.tetris.grid import Grid
from python.games.tetris.conf import grid_width, grid_height
from python.games.tetris.handler import handle_events
from python.games.tetris.mixins import ScoreRecorder, ClockMixin, PygameMixin
from python.games.tetris.drawer import Drawer


class Game(PygameMixin, ClockMixin, ScoreRecorder):
    def __init__(self):
        super(Game, self).__init__()
        ClockMixin.__init__(self)
        ScoreRecorder.__init__(self)

        self.grid = Grid()

        self.drawer = Drawer(self.grid)

    def start(self):
        while not self.grid.is_game_over():
            if self.can_fall():
                self.grid.fall_block()

            handle_events(self.grid)

            self.grid.check_rows()

            self.drawer.draw()

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
