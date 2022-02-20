from tetromino import Block
from conf import cols, rows, Color


class Grid:
    def __init__(self):
        self.colors_by_row_col = [
            [Color.BLACK for y in range(cols)] for x in range(rows)
        ]

        self.fall_time = 0
        self.locked_positions = {}
        self.is_changing = False

        self.current_block = Block.create(4, 0)
        self.next_block = Block.create(4, 0)

    def update_colors(self):
        self.colors_by_row_col = [
            [Color.BLACK for y in range(cols)] for x in range(rows)
        ]
        for row in range(len(self.colors_by_row_col)):
            for col in range(len(self.colors_by_row_col[row])):
                self.colors_by_row_col[row][col] = self.locked_positions.get(
                    (col, row), self.colors_by_row_col[row][col]
                )

    def is_game_over(self):
        for col, row in self.locked_positions:
            if row < 1:
                return True
        return False

    def check_rows(self):
        if self.is_changing:
            # call four times to check for multiple clear rows
            if self.clear_rows(self.locked_positions):
                self.add_score()

            self.is_changing = False

    def fall_block(self):
        self.current_block.fall()
        if not self.valid_space() and self.current_block.row > 0:
            self.current_block.rise()
            self.is_changing = True

            for col, row in self.current_block.coordinates:
                self.locked_positions[(col, row)] = self.current_block.color

        self.update_colors()
        coordinates = self.current_block.coordinates
        for col, row in coordinates:
            if row > -1:
                self.colors_by_row_col[row][col] = self.current_block.color

    def clear_rows(self, locked):
        # need to see if row is clear the shift every other row above down one
        grid = self.colors_by_row_col

        inc = 0
        for i in range(len(grid) - 1, -1, -1):
            row = grid[i]
            if (0, 0, 0) not in row:
                inc += 1
                # add positions to remove from locked
                ind = i
                for j in range(len(row)):
                    try:
                        del locked[(j, i)]
                    except BaseException:
                        continue
        if inc > 0:
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked[newKey] = locked.pop(key)

    def valid_space(self):
        accepted_positions = [
            [
                (col, row)
                for col in range(cols)
                if (col, row) not in self.locked_positions
            ]
            for row in range(rows)
        ]
        accepted_positions = [j for sub in accepted_positions for j in sub]

        for pos in self.current_block.coordinates:
            if pos not in accepted_positions and pos[1] > -1:
                return False

        return True
