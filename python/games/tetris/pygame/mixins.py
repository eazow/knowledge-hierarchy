import pygame


class ScoreRecorder:
    def __init__(self):
        self.score = 0

    def add_score(self):
        self.score += 10


class ClockMixin:
    def __init__(self):
        self.clock = pygame.time.Clock()


class PygameMixin:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Tetris")
