from grid import valid_space


def handle_key_down(current_piece, grid):
    current_piece.y += 1
    if not valid_space(current_piece, grid):
        current_piece.y -= 1


def handle_key_space(current_piece, grid):
    while valid_space(current_piece, grid):
        current_piece.y += 1
    current_piece.y -= 1


def handle_key_up(current_piece, grid):
    # rotate shape
    current_piece.rotation = current_piece.rotation + 1 % len(
        current_piece.shape
    )
    if not valid_space(current_piece, grid):
        current_piece.rotation = current_piece.rotation - 1 % len(
            current_piece.shape
        )


def handle_key_right(current_piece, grid):
    current_piece.x += 1
    if not valid_space(current_piece, grid):
        current_piece.x -= 1


def handle_key_left(current_piece, grid):
    current_piece.x -= 1
    if not valid_space(current_piece, grid):
        current_piece.x += 1
