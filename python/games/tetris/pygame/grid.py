class Grid:
    def __init__(self, ):
        self.colors_by_yx = [[(0, 0, 0) for y in range(10)] for x in range(20)]

    def update_locked(self, locked_positions):
        for i in range(len(self.colors_by_yx)):
            for j in range(len(self.colors_by_yx[i])):
                self.colors_by_yx[i][j] = locked_positions.get((j, i), self.colors_by_yx[i][j])

    def is_game_over(self, positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
        return False

    def update(self, shape_pos, block_color):
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                self.colors_by_yx[y][x] = block_color

    def clear_rows(self, locked):
        # need to see if row is clear the shift every other row above down one
        grid = self.colors_by_yx

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
    formatted = shape.convert_shape_format()

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True
