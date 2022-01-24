import random

import shape
from conf import shape_colors
from shape import shapes


class Piece(object):
    # rows = 20  # y
    # columns = 10  # x

    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def get_shape():
    return Piece(5, 0, random.choice(shape.shapes))