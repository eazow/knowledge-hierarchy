from tetromino import Block
from conf import fall_interval, cols, rows


class Grid:
    def __init__(self):
        self.colors_by_row_col = [[(0, 0, 0) for y in range(cols)] for x in range(rows)]

        self.fall_time = 0
        self.locked_positions = {}
        self.is_changing = False

        self.current_block = Block.create(5, 0)
        self.next_block = Block.create(5, 0)

    def update_locked(self, locked_positions):
        for i in range(len(self.colors_by_row_col)):
            for j in range(len(self.colors_by_row_col[i])):
                self.colors_by_row_col[i][j] = locked_positions.get((j, i), self.colors_by_row_col[i][j])

    def is_game_over(self):
        for x, y in self.locked_positions:
            if y < 1:
                return True
        return False

    def check_rows(self, shape_pos):
        if self.is_changing:

            self.is_changing = False

            # call four times to check for multiple clear rows
            if self.grid.clear_rows(self.locked_positions):
                self.add_score()

    def fall_block(self):
        if self.fall_time >= fall_interval:
            self.fall_time = 0

            self.current_block.fall()
            if (
                not (valid_space(self.current_block, self.grid))
                and self.current_block.row > 0
            ):
                self.current_block.row -= 1
                self.is_changing = True

                for pos in self.current_block.coordinates():
                    p = (pos[0], pos[1])
                    self.locked_positions[p] = self.current_block.color

    def update(self):
        coordinates = self.current_block.coordinates
        for x, y in coordinates:
            if y > -1:
                self.colors_by_row_col[y][x] = self.current_block.color

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


def valid_space(shape, grid):
    accepted_positions = [
        [(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)
    ]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = shape.coordinates()

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True
