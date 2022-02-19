import pygame


class Level:
    def get_level_time(self):
        clock = pygame.time.Clock()
        level_time = clock.get_rawtime()

        if level_time / 1000 > 4:
            level_time = 0
            # if fall_speed > 0.15:
            #     fall_speed -= 0.005
