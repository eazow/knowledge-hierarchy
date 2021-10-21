from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QFrame
from utils import draw_cell


class SidePanel(QFrame):
    def __init__(self, parent, grid_size, inner_board):
        super(SidePanel, self).__init__(parent)
        self.grid_size = grid_size
        self.inner_board = inner_board
        self.setFixedSize(grid_size * 5, grid_size * inner_board.height)
        self.move(grid_size * inner_board.width, 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        x_min, x_max, y_min, y_max = self.inner_board.next_tetris.get_relative_boundary(
            0
        )
        dy = 3 * self.grid_size
        dx = (self.width() - (x_max - x_min) * self.grid_size) / 2
        shape = self.inner_board.next_tetris.shape
        for x, y in self.inner_board.next_tetris.get_absolute_coords(0, 0, -y_min):
            draw_cell(
                painter,
                x * self.grid_size + dx,
                y * self.grid_size + dy,
                shape,
                self.grid_size,
            )

    def updateData(self):
        self.update()