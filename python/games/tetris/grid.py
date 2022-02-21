from tetromino import Block
from conf import cols, rows
from colors import Color


class Grid:
    def __init__(self):
        self.fall_time = 0
        self.locked_positions = {}
        self.is_changing = False

        self.current_block = Block.create(4, 0)
        self.next_block = Block.create(4, 0)

        self.colors_by_row_col = {}
        self.init_colors()

    def init_colors(self):
        self.colors_by_row_col = [[Color.BLACK for _ in range(cols)] for _ in range(rows)]

    def update_colors(self):
        self.init_colors()
        for row in range(rows):
            for col in range(cols):
                self.colors_by_row_col[row][col] = self.locked_positions.get(
                    (col, row), self.colors_by_row_col[row][col]
                )

        for col, row in self.current_block.coordinates:
            if row > -1:
                self.colors_by_row_col[row][col] = self.current_block.color

    def is_game_over(self):
        for col, row in self.locked_positions:
            if row < 1:
                return True
        return False

    def check_rows(self):
        if self.is_changing:
            self.is_changing = False
            # call four times to check for multiple clear rows
            return self.clear_rows()

        return False

    def fall_block(self):
        self.current_block.fall()
        if not self.is_valid() and self.current_block.row > 0:
            self.current_block.rise()
            self.is_changing = True

            for col, row in self.current_block.coordinates:
                self.locked_positions[(col, row)] = self.current_block.color

        self.update_colors()

    def clear_rows(self):
        # need to see if row is clear the shift every other row above down one
        locked = self.locked_positions

        cleared_rows = 0
        for i in range(rows - 1, -1, -1):
            if Color.BLACK not in self.colors_by_row_col[i]:
                cleared_rows += 1
                # add positions to remove from locked
                ind = i
                for j in range(cols):
                    if (j, i) in locked:
                        del locked[(j, i)]
        if cleared_rows > 0:
            for col, row in sorted(list(locked), key=lambda x: x[1])[::-1]:
                if row < ind:
                    locked[(col, row + cleared_rows)] = locked.pop((col, row))

        return cleared_rows

    def is_valid(self):
        empty_positions = set([
            (col, row)
            for row in range(rows)
            for col in range(cols)
            if (col, row) not in self.locked_positions
        ])

        for col, row in self.current_block.coordinates:
            if (col, row) not in empty_positions and row >= 0:
                return False

        return True
