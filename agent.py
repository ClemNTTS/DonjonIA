import random

moves = [
    (0, 1),  # right
    (1, 0),  # down
    (0, -1), # left
    (-1, 0)  # up
]

def move(position, maze):
    x, y = position
    direction = choose_direction()
    print(direction)
    dx, dy = moves[direction]
    nx, ny = x + dx, y + dy
    if maze[nx][ny] == 3:
        return (nx, ny), True
    if maze[nx][ny] != 1:
        return (nx, ny), False
    return position, False

def choose_direction():
    return random.randint(0, 3)

