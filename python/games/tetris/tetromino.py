"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
"""
import random
from abc import ABC

from colors import Color


class Block(ABC):
    shapes = None
    color = None
    rotation = 0

    def __init__(self, col, row):
        self.col = col
        self.row = row

    @property
    def coordinates(self):
        shape = self.shapes[self.rotation]

        return [
            (self.col + j, self.row + i)
            for i, row in enumerate(shape)
            for j, col in enumerate(row)
            if col != "."
        ]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shapes)
        return self

    def fall(self):
        self.row += 1

    def rise(self):
        self.row -= 1

    @classmethod
    def create(cls, row, col):
        return random.choice(cls.__subclasses__())(row, col)


class BlockS(Block):
    shapes = [
        [
            "....",
            "..00",
            ".00.",
            "....",
        ],
        [
            ".0..",
            ".00.",
            "..0.",
            "....",
        ],
    ]
    color = Color.YELLOW


class BlockZ(Block):
    shapes = [
        [
            "....",
            ".00.",
            "..00",
            "....",
        ],
        [
            "..0.",
            ".00.",
            ".0..",
            "....",
        ],
    ]
    color = Color.TEAL


class BlockI(Block):
    shapes = [
        [
            ".0..",
            ".0..",
            ".0..",
            ".0..",
        ],
        [
            "....",
            "0000",
            "....",
            "....",
        ],
    ]
    color = Color.BLUE


class BlockO(Block):
    shapes = [
        [
            "....",
            ".00.",
            ".00.",
            "....",
        ]
    ]
    color = Color.ORANGE


class BlockJ(Block):
    shapes = [
        [
            "....",
            ".0..",
            ".000",
            "....",
        ],
        [
            ".00.",
            ".0..",
            ".0..",
            "....",
        ],
        [
            "....",
            ".000",
            "...0",
            "....",
        ],
        [
            "..0.",
            "..0.",
            ".00.",
            "....",
        ],
    ]
    color = Color.GREEN


class BlockL(Block):
    shapes = [
        [
            "....",
            "..0.",
            "000.",
            "....",
        ],
        [
            ".0..",
            ".0..",
            ".00.",
            "....",
        ],
        [
            "....",
            ".000",
            ".0..",
            "....",
        ],
        [
            ".00.",
            "..0.",
            "..0.",
            "....",
        ],
    ]
    color = Color.RED


class BlockT(Block):
    shapes = [
        [
            "....",
            "..0.",
            ".000",
            "....",
        ],
        [
            "....",
            ".0..",
            ".00.",
            ".0..",
        ],
        [
            "....",
            ".000",
            "..0.",
            "....",
        ],
        [
            "....",
            "..0.",
            ".00.",
            "..0.",
        ],
    ]
    color = Color.PURPLE
