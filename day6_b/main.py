def get_grid():
    """
    Returns the grid from the puzzle file
    :return:
    """
    with open("puzzle.txt") as file:
        lines = file.readlines()

    return lines


def find_obstructions(grid):
    """
    Finds the positions an obstruction can be placed so the guard goes in a loop
    :param grid:
    :return:
    """
    obstructions = set()

    for x, row in enumerate(grid):
        for y, char in enumerate(row):
            if char != ".":
                continue

            # Replace x, y with a #
            temp_grid = grid[:x] + [f"{row[:y]}#{row[y + 1:]}"] + grid[x + 1:]
            is_looping = find_possible_loop(temp_grid)

            if is_looping:
                obstructions.add((x, y))

    return obstructions


def find_possible_loop(grid):
    """
    Simulates the guards movement until:
    - The guard goes out of bounds, so there is no loop
    - The guard visits the same position in the same direction, there is a loop
    :param grid:
    :return:
    """
    position = get_start(grid)
    direction = (-1, 0)
    visited = {(position, direction)}

    while True:
        position, direction = step(grid, position, direction)

        if position is None:
            break

        if (position, direction) in visited:
            return True

        visited.add((position, direction))

    return False


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

    obstructions = find_obstructions(grid)

    print(len(obstructions))


if __name__ == "__main__":
    main()
