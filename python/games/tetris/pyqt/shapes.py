class TetrisShape:
    def __init__(self, shape=0):
        # 空块
        self.shape_empty = 0
        # 一
        self.shape_I = 1
        # L
        self.shape_L = 2
        # 向左的L型块
        self.shape_J = 3
        # T型块
        self.shape_T = 4
        # 田字型块
        self.shape_O = 5
        # 反向Z型块
        self.shape_S = 6
        # Z型块
        self.shape_Z = 7
        # 每种块包含的四个小方块相对坐标分布
        self.shapes_relative_coords = [
            [[0, 0], [0, 0], [0, 0], [0, 0]],
            [[0, -1], [0, 0], [0, 1], [0, 2]],
            [[0, -1], [0, 0], [0, 1], [1, 1]],
            [[0, -1], [0, 0], [0, 1], [-1, 1]],
            [[0, -1], [0, 0], [0, 1], [1, 0]],
            [[0, 0], [0, -1], [1, 0], [1, -1]],
            [[0, 0], [0, -1], [-1, 0], [1, -1]],
            [[0, 0], [0, -1], [1, 0], [-1, -1]],
        ]
        self.shape = shape
        self.relative_coords = self.shapes_relative_coords[self.shape]

    def get_rotated_relative_coords(self, direction):
        """获得该形状当前旋转状态的四个小方块的相对坐标分布"""
        # 初始分布
        if direction == 0 or self.shape == self.shape_O:
            return self.relative_coords
        # 逆时针旋转90度
        if direction == 1:
            return [[-y, x] for x, y in self.relative_coords]
        # 逆时针旋转180度
        if direction == 2:
            if self.shape in [self.shape_I, self.shape_Z, self.shape_S]:
                return self.relative_coords
            else:
                return [[-x, -y] for x, y in self.relative_coords]
        # 逆时针旋转270度
        if direction == 3:
            if self.shape in [self.shape_I, self.shape_Z, self.shape_S]:
                return [[-y, x] for x, y in self.relative_coords]
            else:
                return [[y, -x] for x, y in self.relative_coords]

    def get_absolute_coords(self, direction, x, y):
        """获得该俄罗斯方块的各个小块绝对坐标"""
        return [[x + i, y + j] for i, j in self.get_rotated_relative_coords(direction)]

    def get_relative_boundary(self, direction):
        """获得相对坐标的边界"""
        relative_coords_now = self.get_rotated_relative_coords(direction)
        xs = [i[0] for i in relative_coords_now]
        ys = [i[1] for i in relative_coords_now]
        return min(xs), max(xs), min(ys), max(ys)
