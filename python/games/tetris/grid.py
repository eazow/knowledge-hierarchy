from tetromino import Block
from conf import cols, rows
from colors import Color


class Grid:
    def __init__(self):
        self.fall_time = 0
        self.is_changing = False

        self.current_block = Block.create(3, -4)
        self.next_block = Block.create(3, -4)

        self.locks = {}
        self.colors = {}
        self.init_colors()

    def init_colors(self):
        self.colors = [[Color.BLACK] * cols for _ in range(rows)]

    def update_colors(self):
        self.init_colors()
        for col, row in self.locks.keys():
            self.colors[row][col] = self.locks.get((col, row))

        for col, row in self.current_block.coordinates:
            if row >= 0:
                self.colors[row][col] = self.current_block.color

    def is_game_over(self):
        for col, row in self.locks:
            if row < 1:
                return True
        return False

    def check_rows(self):
        if self.is_changing:
            self.change_block()

            self.is_changing = False

            return self.clear_rows()

        return 0

    def change_block(self):
        self.current_block = self.next_block
        self.next_block = Block.create(4, 0)

    def update_locked(self):
        for col, row in self.current_block.coordinates:
            self.locks[(col, row)] = self.current_block.color

    def fall_block(self):
        self.current_block.fall()
        if not self.is_valid() and self.current_block.row > 0:
            self.current_block.rise()
            self.is_changing = True

            self.update_locked()

        self.update_colors()

    def is_full_row(self, row):
        for col in range(cols):
            if (col, row) not in self.locks:
                return False

        return True

    def clear_rows(self):
        cleared_rows = 0

        for _ in range(4):
            for i in range(rows - 1, -1, -1):
                if self.is_full_row(i):
                    cleared_rows += 1
                    [
                        self.locks.pop((j, i))
                        for j in range(cols)
                        if (j, i) in self.locks
                    ]

                    for col, row in sorted(
                        list(self.locks), key=lambda x: x[1], reverse=True
                    ):
                        if row < i:
                            self.locks[(col, row + 1)] = self.locks.pop((col, row))

        return cleared_rows

    def is_valid(self):
        empty_positions = set(
            [
                (col, row)
                for row in range(rows)
                for col in range(cols)
                if (col, row) not in self.locks
            ]
        )

        for col, row in self.current_block.coordinates:
            if (col, row) not in empty_positions and row >= 0:
                return False

        return True

    def left(self):
        self.current_block.col -= 1
        if not self.is_valid():
            self.current_block.col += 1

    def right(self):
        self.current_block.col += 1
        if not self.is_valid():
            self.current_block.col -= 1
