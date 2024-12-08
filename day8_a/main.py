def get_grid():
    """
    Returns the puzzle grid
    :return:
    """
    with open("puzzle.txt") as file:
        lines = file.readlines()

    return [line.strip() for line in lines]


def get_antennas_from_grid(grid):
    """
    Parses the positions of all antennas and their frequencies into a dict
    :param grid:
    :return:
    """
    antennas = dict()

    for x, row in enumerate(grid):
        for y, char in enumerate(row):
            if char == ".":
                continue

            antennas[(x, y)] = char

    return antennas


def find_antinodes(grid):
    """
    Finds all the antinodes in a grid
    :param grid:
    :return:
    """
    antennas = get_antennas_from_grid(grid)
    frequencies = set(antennas.values())

    antinodes = set()

    for frequency in frequencies:
        antinodes.update(find_frequency_antinodes(frequency, antennas, grid))

    return antinodes


def find_frequency_antinodes(frequency, antennas, grid):
    """
    Finds all the antinodes of a specific frequency in a grid
    :param frequency:
    :param antennas:
    :param grid:
    :return:
    """
    frequency_antennas = [p for p, f in antennas.items() if f == frequency]

    antinodes = set()

    for i, a in enumerate(frequency_antennas):
        for j, b in enumerate(frequency_antennas):
            if i == j:
                continue

            dx = b[0] - a[0]
            dy = b[1] - a[1]
            x = a[0] - dx
            y = a[1] - dy

            if not in_bounds(x, y, grid):
                continue

            antinodes.add((x, y))

    return antinodes


def in_bounds(x, y, grid):
    """
    Whether the given position is inside the grid
    :param x:
    :param y:
    :param grid:
    :return:
    """
    x_in_bounds = 0 <= x < len(grid)
    y_in_bounds = 0 <= y < len(grid[0])

    return x_in_bounds and y_in_bounds


def main():
    grid = get_grid()

    antinodes = find_antinodes(grid)

    print(len(antinodes))


if __name__ == "__main__":
    main()
