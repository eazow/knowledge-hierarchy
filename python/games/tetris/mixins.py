import pygame
from conf import fall_interval


class ScoreRecorder:
    def __init__(self):
        self.score = 0

    def add_score(self):
        self.score += 10


class ClockMixin:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.time_passed = 0

    def can_fall(self):
        self.clock.tick(30)
        self.time_passed += self.clock.get_rawtime()
        if self.time_passed >= fall_interval:
            self.time_passed = 0
            return True

        return False


class PygameMixin:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Tetris")
