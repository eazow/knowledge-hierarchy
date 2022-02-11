"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
import random
from enum import Enum

from conf import shape_colors


class ShapeType(Enum):
    pass


S = [
    [".....", ".....", "..00.", ".00..", "....."],
    [".....", "..0..", "..00.", "...0.", "....."],
]
Z = [
    [".....", ".....", ".00..", "..00.", "....."],
    [".....", "..0..", ".00..", ".0...", "....."],
]
I = [
    ["..0..", "..0..", "..0..", "..0..", "....."],
    [".....", "0000.", ".....", ".....", "....."],
]
O = [[".....", ".....", ".00..", ".00..", "....."]]
J = [
    [".....", ".0...", ".000.", ".....", "....."],
    [".....", "..00.", "..0..", "..0..", "....."],
    [".....", ".....", ".000.", "...0.", "....."],
    [".....", "..0..", "..0..", ".00..", "....."],
]
L = [
    [".....", "...0.", ".000.", ".....", "....."],
    [".....", "..0..", "..0..", "..00.", "....."],
    [".....", ".....", ".000.", ".0...", "....."],
    [".....", ".00..", "..0..", "..0..", "....."],
]
T = [
    [".....", "..0..", ".000.", ".....", "....."],
    [".....", "..0..", "..00.", "..0..", "....."],
    [".....", ".....", ".000.", "..0..", "....."],
    [".....", "..0..", ".00..", "..0..", "....."],
]

shapes = [S, Z, I, O, J, L, T]


class Block(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

    def convert_shape_format(self, shape):
        positions = []
        format = shape.shape[shape.rotation % len(shape.shape)]
        print(format)

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == "0":
                    positions.append((shape.x + j, shape.y + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions

    @classmethod
    def create(cls):
        return Block(5, 0, random.choice(shapes))
