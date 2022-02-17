"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""
import random
from abc import ABC, abstractproperty, abstractmethod
from enum import Enum

from conf import shape_colors, Color


class BlockShapes(Enum):
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

    @classmethod
    def list(cls):
        return [x.value for x in BlockShapes]


class Block(ABC):
    shapes = None
    color = None
    rotation = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def coordinates(self):
        positions = []
        shape = self.shapes[self.rotation % len(self.shapes)]

        for i, line in enumerate(shape):
            row = list(line)
            for j, column in enumerate(row):
                if column == "0":
                    positions.append((self.x + j, self.y + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shapes)
        return self

    @classmethod
    def create(cls, x, y):
        return random.choice(cls.__subclasses__())(x, y)


class BlockS(Block):
    shapes = [
        [".....", ".....", "..00.", ".00..", "....."],
        [".....", "..0..", "..00.", "...0.", "....."],
    ]
    color = Color.YELLOW


class BlockZ(Block):
    shapes = [
        [".....", ".....", ".00..", "..00.", "....."],
        [".....", "..0..", ".00..", ".0...", "....."],
    ]
    color = Color.TEAL



class BlockI(Block):
    shapes = [
        ["..0..", "..0..", "..0..", "..0..", "....."],
        [".....", "0000.", ".....", ".....", "....."],
    ]
    color = Color.BLUE


class BlockO(Block):
    shapes = [[".....", ".....", ".00..", ".00..", "....."]]
    color = Color.ORANGE


class BlockJ(Block):
    shapes = [
        [".....", ".0...", ".000.", ".....", "....."],
        [".....", "..00.", "..0..", "..0..", "....."],
        [".....", ".....", ".000.", "...0.", "....."],
        [".....", "..0..", "..0..", ".00..", "....."],
    ]
    color = Color.GREEN


class BlockL(Block):
    shapes = [
        [".....", "...0.", ".000.", ".....", "....."],
        [".....", "..0..", "..0..", "..00.", "....."],
        [".....", ".....", ".000.", ".0...", "....."],
        [".....", ".00..", "..0..", "..0..", "....."],
    ]
    color = Color.RED


class BlockT(Block):
    shapes = [
        [".....", "..0..", ".000.", ".....", "....."],
        [".....", "..0..", "..00.", "..0..", "....."],
        [".....", ".....", ".000.", "..0..", "....."],
        [".....", "..0..", ".00..", "..0..", "....."],
    ]
    color = Color.PURPLE
