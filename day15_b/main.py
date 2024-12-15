MOVES = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1)
}


def parse_grid(raw):
    """
    Parses and expands the raw grid into the actual grid
    :param raw:
    :return:
    """
    grid = [[]]

    for char in raw:
        if char == "\n":
            grid.append(list())

        if char == "@":
            grid[-1] += ["@", "."]

        if char == "O":
            grid[-1] += ["[", "]"]

        if char == ".":
            grid[-1] += [".", "."]

        if char == "#":
            grid[-1] += ["#", "#"]

    return grid


def get_grid_and_moves():
    """
    Parse the puzzle into a grid and a list of directions we need to go in
    :return:
    """
    with open("puzzle.txt") as file:
        puzzle = file.read()

    [grid, moves] = puzzle.split("\n\n")

    grid = parse_grid(grid)
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


def can_move(position, direction, grid):
    """
    Whether the item at the given position can move
    Takes pushable boxes into account
    :param position:
    :param direction:
    :param grid:
    :return:
    """
    item = grid[position[0]][position[1]]

    x = position[0] + direction[0]
    y = position[1] + direction[1]
    y_start = y - 1 if item == "]" else y
    y_end = y + 1 if item == "[" else y

    chars = grid[x][y_start:(y_end + 1)]

    # It's just empty space so we can move
    if all(char == "." for char in chars):
        return True

    # If a wall is present it's not possible to move
    if any(char == "#" for char in chars):
        return False

    # A box is in the way, check if the box can be moved
    if len(chars) == 1 and chars[0] in ("[", "]"):
        return can_move((x, y), direction, grid)

    # A box is in the way on the left or right side of the current box
    if len(chars) == 2 and direction[1] != 0:
        if direction[1] == -1 and chars[0] == "]":
            return can_move((x, y_start), direction, grid)

        if direction[1] == 1 and chars[1] == "[":
            return can_move((x, y_end), direction, grid)

        return True

    # If there are 2 boxes below or above, check if both can be moved
    if chars[0] == "]" and chars[1] == "[":
        return can_move((x, y_start), direction, grid) and can_move((x, y_end), direction, grid)

    # If there is a single box below on the most left side
    if chars[0] in ("[", "]"):
        return can_move((x, y_start), direction, grid)

    # Finally if there is a single box on the most right side
    return can_move((x, y_end), direction, grid)


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

    # Only if item is @, otherwise we call can_move a lot of unneeded times
    if item == "@" and not can_move(position, direction, grid):
        return position, grid

    # The position of the current item
    # Range is used for boxes
    px = position[0]
    py = position[1]
    py_start = py - 1 if item == "]" else py
    py_end = py + 1 if item == "[" else py

    x = px + direction[0]
    y = py + direction[1]
    y_start = py_start + direction[1]
    y_end = py_end + direction[1]

    chars = grid[x][y_start:(y_end + 1)]

    # Move boxes in the way
    # We already know they can be moved
    if len(chars) == 1 and chars[0] in ("[", "]"):
        _, grid = move((x, y), direction, grid)

    if len(chars) == 2 and direction[1] != 0:
        if direction[1] == -1 and chars[0] == "]":
            _, grid = move((x, y_start), direction, grid)

        if direction[1] == 1 and chars[1] == "[":
            _, grid = move((x, y_end), direction, grid)

    if len(chars) == 2 and direction[0] != 0:
        if chars[0] == "]" and chars[1] == "[":
            _, grid = move((x, y_start), direction, grid)
            _, grid = move((x, y_end), direction, grid)
        elif chars[0] in ("[", "]"):
            _, grid = move((x, y_start), direction, grid)
        elif chars[1] in ("[", "]"):
            _, grid = move((x, y_end), direction, grid)

    # Move the current item
    grid[px][py_start:(py_end + 1)] = ["."] * (abs(py_end - py_start) + 1)

    if y_start == y_end:
        grid[x][y] = "@"

    if y_start != y_end:
        grid[x][y_start:(y_end + 1)] = ["[", "]"]

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
            if char != "[":
                continue

            total += x * 100 + y

    return total


def main():
    grid, moves = get_grid_and_moves()

    total = find_sum_of_gps_coordinates_after_moves(grid, moves)

    print(total)


if __name__ == "__main__":
    main()
