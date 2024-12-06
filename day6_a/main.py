def get_grid():
    """
    Returns the grid from the puzzle file
    :return:
    """
    with open("puzzle.txt") as file:
        lines = file.readlines()

    return lines


def find_positions(grid):
    """
    Finds all positions the guard will visit before leaving
    :param grid:
    :return:
    """
    position = get_start(grid)
    direction = (-1, 0)
    visited = set()

    while position is not None:
        position, direction = step(grid, position, direction)

        if position is not None:
            visited.add(position)

    return visited


def step(grid, position, direction):
    """
    Does a single step
    Returns None, None if the position is out of bounds
    :param grid:
    :param position:
    :param direction:
    :return:
    """
    px = position[0] + direction[0]
    py = position[1] + direction[1]

    if not is_in_bounds(px, py, grid):
        return None, None

    if grid[px][py] == "#":
        return step(grid, position, (direction[1], -direction[0]))

    return (px, py), direction


def is_in_bounds(x, y, grid):
    """
    Whether the given x,y is in bounds
    :param x:
    :param y:
    :param grid:
    :return:
    """
    x_in_bounds = 0 <= x < len(grid)
    y_in_bounds = 0 <= y < len(grid[0])

    return x_in_bounds and y_in_bounds


def get_start(grid):
    """
    Finds the starting position
    :param grid:
    :return:
    """
    for x, row in enumerate(grid):
        for y, char in enumerate(row):
            if char != "^":
                continue

            return x, y


def main():
    grid = get_grid()

    positions = find_positions(grid)

    print(len(positions))


if __name__ == "__main__":
    main()
