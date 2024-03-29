import pygame
from conf import fall_interval, caption


class ScoreMixin:
    score = 0

    def add_score(self, score):
        self.score += score
        if score != 0:
            print(f"Score: {self.score}")


class ClockMixin(object):
    clock = pygame.time.Clock()
    time_passed = 0

    def can_fall(self):
        self.clock.tick()
        self.time_passed += self.clock.get_rawtime()
        if self.time_passed >= fall_interval:
            self.time_passed = 0
            return True

        return False


class PygameMixin(object):
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(caption)
