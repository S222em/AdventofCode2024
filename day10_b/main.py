def get_grid():
    """
    Returns the topographic map as a grid of integers
    :return:
    """
    with open("puzzle.txt") as file:
        lines = file.readlines()

    return [[int(char) for char in line.strip()] for line in lines]


def find_trailheads(grid):
    """
    Finds all the trailheads in the grid
    Trailheads are where the height = 0
    :param grid:
    :return:
    """
    trailheads = list()

    for x, row in enumerate(grid):
        for y, height in enumerate(row):
            if height != 0:
                continue

            trailheads.append((x, y))

    return trailheads


DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def get_trailhead_rating(trailhead, grid):
    """
    Get the rating of the trailhead
    Rating is equal to the number of paths that lead to trailends (height=9)
    :param trailhead:
    :param grid:
    :return:
    """
    queue = [[trailhead]]
    paths = set()

    while len(queue) != 0:
        path = queue.pop(0)

        x, y = path[-1]

        for dx, dy in DIRECTIONS:
            px = x + dx
            py = y + dy

            if (px, py) in path:
                continue

            if not is_in_bounds(px, py, grid) or grid[x][y] + 1 != grid[px][py]:
                continue

            next_path = path + [(px, py)]

            # We found a path leading to a trailend
            # Save the path as a tuple (as it's hashable)
            if grid[px][py] == 9:
                paths.add(tuple(next_path))
                continue

            queue.append(next_path)

    return len(paths)


def is_in_bounds(x, y, grid):
    """
    Whether the given coordinate is in bounds
    :param x:
    :param y:
    :param grid:
    :return:
    """
    x_in_bounds = 0 <= x < len(grid)
    y_in_bounds = 0 <= y < len(grid[0])

    return x_in_bounds and y_in_bounds


def sum_trailheads_ratings(grid):
    """
    Sums the ratings of all trailheads in the grid
    :param grid:
    :return:
    """
    trailheads = find_trailheads(grid)
    total = 0

    for trailhead in trailheads:
        rating = get_trailhead_rating(trailhead, grid)
        total += rating

    return total


def main():
    grid = get_grid()

    total = sum_trailheads_ratings(grid)

    print(total)


if __name__ == "__main__":
    main()
