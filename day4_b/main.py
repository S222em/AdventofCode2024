def get_puzzle():
    """
    Returns the puzzle input in lines with newline chars stripped
    :return:
    """
    with open("puzzle.txt") as file:
        lines = file.readlines()

    return [line.strip() for line in lines]


DIRECTIONS = [(1, 1), (1, -1)]


def find_x_occurrences(puzzle: list[str]) -> int:
    """
    Finds all occurrences of the x-mas
    :param puzzle:
    :return:
    """
    occurrences = 0

    for x, row in enumerate(puzzle):
        for y, char in enumerate(row):
            # A is always the middle, so look from there
            if char != "A":
                continue

            occurrences += is_x_from(x, y, puzzle)

    return occurrences


def is_x_from(x: int, y: int, puzzle: list[str]) -> bool:
    """
    Check whether an x-mas is present from the given x, y
    :param x:
    :param y:
    :param puzzle:
    :return:
    """
    for dx, dy in DIRECTIONS:
        # Coordinates of opposite sides of A
        px = x + dx
        py = y + dy
        qx = x - dx
        qy = y - dy

        if not is_in_bounds(px, py, puzzle) or puzzle[px][py] not in "MS":
            return False

        if not is_in_bounds(qx, qy, puzzle) or puzzle[qx][qy] not in "MS":
            return False

        # If it's the same char MAS can not be formed so invalid
        # For example:
        # M S
        #  A
        # S M
        # This forms the words MAM and SAS which is not valid
        if puzzle[px][py] == puzzle[qx][qy]:
            return False

    return True


def is_in_bounds(x: int, y: int, puzzle: list[str]) -> bool:
    """
    Whether the given x, y is in bounds of the puzzle
    :param x:
    :param y:
    :param puzzle:
    :return:
    """
    x_in_bounds = 0 <= x < len(puzzle)
    y_in_bounds = 0 <= y < len(puzzle[0])

    return x_in_bounds and y_in_bounds


def main():
    puzzle = get_puzzle()

    occurrences = find_x_occurrences(puzzle)

    print(occurrences)


if __name__ == "__main__":
    main()
