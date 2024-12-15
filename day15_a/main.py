MOVES = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1)
}


def get_grid_and_moves():
    """
    Parse the puzzle into a grid and a list of directions we need to go in
    :return:
    """
    with open("puzzle.txt") as file:
        puzzle = file.read()

    [grid, moves] = puzzle.split("\n\n")

    grid = [[char for char in line] for line in grid.split("\n")]
    moves = [MOVES[move] for move in moves.replace("\n", "")]

    return grid, moves


def get_robot_position(grid):
    """
    Find the current position of the robot in the grid
    :param grid:
    :return:
    """
    for x, row in enumerate(grid):
        for y, char in enumerate(row):
            if char != "@":
                continue

            return x, y

    return None


def move(position, direction, grid):
    """
    Move the given item at position in a certain direction
    - Cannot move to walls.
    - Cannot move into boxes (but boxes can be pushed).
    :param position:
    :param direction:
    :param grid:
    :return:
    """
    item = grid[position[0]][position[1]]

    x = position[0] + direction[0]
    y = position[1] + direction[1]

    char = grid[x][y]

    # We hit a wall so do nothing
    if char == "#":
        return position, grid

    # We hit a box
    if char == "O":
        # Attempt to move the box
        box_position, grid = move((x, y), direction, grid)
        # If the box has not moved, don't move the current item
        if box_position == (x, y):
            return position, grid

    grid[position[0]][position[1]] = "."
    grid[x][y] = item

    return (x, y), grid


def move_robot(grid, moves):
    """
    Make the robot do all moves
    :param grid:
    :param moves:
    :return:
    """
    position = get_robot_position(grid)

    for direction in moves:
        position, grid = move(position, direction, grid)

    return grid


def find_sum_of_gps_coordinates_after_moves(grid, moves):
    """
    Finds the sum of gps coordinates after the robot has done it's moves
    :param grid:
    :param moves:
    :return:
    """
    grid = move_robot(grid, moves)

    return get_sum_of_gps_coordinates(grid)


def get_sum_of_gps_coordinates(grid):
    """
    Calculates the total sum of all gps coordinates
    gps coordinate: x * 100 + y
    :param grid:
    :return:
    """
    total = 0

    for x, row in enumerate(grid):
        for y, char in enumerate(row):
            if char != "O":
                continue

            total += x * 100 + y

    return total


def main():
    grid, moves = get_grid_and_moves()

    total = find_sum_of_gps_coordinates_after_moves(grid, moves)

    print(total)


if __name__ == "__main__":
    main()
