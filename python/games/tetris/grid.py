from tetromino import Block
from conf import cols, rows
from colors import Color


class Grid:
    def __init__(self):
        self.fall_time = 0
        self.is_changing = False

        self.current_block = Block.create(4, 0)
        self.next_block = Block.create(4, 0)

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
            if row > -1:
                self.colors[row][col] = self.current_block.color

    def is_game_over(self):
        for col, row in self.locks:
            if row < 1:
                return True
        return False

    def check_rows(self):
        if self.is_changing:
            self.is_changing = False
            # call four times to check for multiple clear rows
            return self.clear_rows()

        return False

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

    def clear_rows(self):
        cleared_rows = 0
        for i in range(rows - 1, -1, -1):
            if Color.BLACK not in self.colors[i]:
                cleared_rows += 1
                # add positions to remove from locked
                min_row = i
                for j in range(cols):
                    if (j, i) in self.locks:
                        del self.locks[(j, i)]
        if cleared_rows > 0:
            for col, row in sorted(list(self.locks), key=lambda x: x[1], reverse=True):
                if row < min_row:
                    self.locks[(col, row + cleared_rows)] = self.locks.pop((col, row))

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
