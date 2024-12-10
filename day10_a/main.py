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


def get_trailhead_score(trailhead, grid):
    """
    Get the score of the trailhead
    Score is equal to the number of trailends (height=9) reachable
    :param trailhead:
    :param grid:
    :return:
    """
    queue = [trailhead]
    visited = {trailhead}
    trailends = set()

    while len(queue) != 0:
        x, y = queue.pop(0)

        for dx, dy in DIRECTIONS:
            px = x + dx
            py = y + dy

            if not is_in_bounds(px, py, grid) or grid[x][y] + 1 != grid[px][py]:
                continue

            if (px, py) in visited:
                continue

            if grid[px][py] == 9:
                trailends.add((px, py))
                continue

            visited.add((px, py))
            queue.append((px, py))

    return len(trailends)


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


def sum_trailheads_scores(grid):
    """
    Sums the scores of all trailheads in the grid
    :param grid:
    :return:
    """
    trailheads = find_trailheads(grid)
    total = 0

    for trailhead in trailheads:
        total += get_trailhead_score(trailhead, grid)

    return total


def main():
    grid = get_grid()

    total = sum_trailheads_scores(grid)

    print(total)


if __name__ == "__main__":
    main()
