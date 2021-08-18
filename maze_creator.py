cell, wall = 'c', 'w'


def init_maze(width, height):
    line = ['u' for _ in range(width)]
    return [line for _ in range(height)]
