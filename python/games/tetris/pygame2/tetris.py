import sys

import pygame

from grid import Grid, create_grid
from piece import get_shape
from conf import window_width, window_height, play_width, play_height, fall_speed

top_left_x = (window_width - play_width) // 2
top_left_x = 0
top_left_y = window_height - play_height
top_left_y = 0


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_positions = [
        [(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)
    ]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def is_game_over(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(
        label,
        (
            top_left_x + play_width / 2 - (label.get_width() / 2),
            top_left_y + play_height / 2 - label.get_height() / 2,
        ),
    )


def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one

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


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Next Shape", 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    sy = top_left_y + 50
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == "0":
                pygame.draw.rect(
                    surface, shape.color, (sx + j * 30, sy + i * 30, 30, 30), 0
                )

    surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface):
    # surface.fill((0, 0, 0))
    # Tetris Title
    font = pygame.font.SysFont("comicsans", 60)
    # label = font.render("TETRIS", 1, (255, 255, 255))
    # surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(
                surface,
                grid[i][j],
                (top_left_x + j * 30, top_left_y + i * 30, 30, 30),
                0,
            )

    # draw grid and border
    Grid.draw(surface, 20, 10, top_left_x, top_left_y)
    pygame.draw.rect(
        surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 1
    )
    # pygame.display.update()


def start():
    global grid

    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)

    change_piece = False
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    score = 0

    while True:
        print(locked_positions)
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()

        clock.tick()

        # PIECE FALLING CODE
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        [handle_event(current_piece, event) for event in pygame.event.get()]

        shape_pos = convert_shape_format(current_piece)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # call four times to check for multiple clear rows
            if clear_rows(grid, locked_positions):
                score += 10
                print(score)

        draw_window(window)
        draw_next_shape(next_piece, window)
        pygame.display.update()

        # Check if user lost
        if is_game_over(locked_positions):
            break

    draw_text_middle("You Lost", 40, (255, 255, 255), window)
    pygame.display.update()
    pygame.time.delay(2000)


def handle_event(current_piece, event):
    if event.type == pygame.QUIT:
        pygame.display.quit()
        quit()
        sys.exit(0)
    if event.type == pygame.KEYDOWN:
        handle_keydown(current_piece, event)


def handle_keydown(current_piece, event):
    if event.key == pygame.K_LEFT:
        current_piece.x -= 1
        if not valid_space(current_piece, grid):
            current_piece.x += 1

    elif event.key == pygame.K_RIGHT:
        current_piece.x += 1
        if not valid_space(current_piece, grid):
            current_piece.x -= 1
    elif event.key == pygame.K_UP:
        # rotate shape
        current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
        if not valid_space(current_piece, grid):
            current_piece.rotation = current_piece.rotation - 1 % len(
                current_piece.shape
            )
    if event.key == pygame.K_DOWN:
        # move shape down
        current_piece.y += 1
        if not valid_space(current_piece, grid):
            current_piece.y -= 1
    """if event.key == pygame_.K_SPACE:
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1
                    print(convert_shape_format(current_piece))"""  # todo fix


def init():
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Tetris")
    return pygame.display.set_mode((window_width, window_height))


if __name__ == "__main__":
    window = init()
    start()
