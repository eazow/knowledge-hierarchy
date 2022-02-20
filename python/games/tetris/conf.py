from enum import Enum

window_width = 600
window_height = 600

grid_width = 300
grid_height = 600

rows = 20
cols = 10

cell_size = 30

shape_colors = [
    (0, 255, 0),
    (255, 0, 0),
    (0, 255, 255),
    (255, 255, 0),
    (255, 165, 0),
    (0, 0, 255),
    (128, 0, 128),
]

fall_interval = 300  # milliseconds


class Color(Enum):
    YELLOW = (244, 197, 36)
    TEAL = (70, 194, 255)
    BLUE = (54, 99, 246)
    ORANGE = (237, 130, 33)
    GREEN = (124, 227, 22)
    RED = (245, 61, 102)
    PURPLE = (227, 72, 192)
    ASH = (100, 100, 100)
    CHARCOAL = (40, 40, 40)
    JET = (43, 43, 43)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
