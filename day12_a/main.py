def get_grid():
    """
    Returns the puzzle's grid
    :return:
    """
    with open("puzzle.txt") as file:
        lines = file.readlines()

    return [line.strip() for line in lines]


DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def find_total_price(grid):
    """
    Finds the total price for all the fences
    :param grid:
    :return:
    """
    visited = set()
    total = 0

    for x, row in enumerate(grid):
        for y, char in enumerate(row):
            if (x, y) in visited:
                continue

            price, visited = find_price_from((x, y), visited, grid)
            total += price

    return total


def find_price_from(start, visited, grid):
    """
    Finds the total price for the garden plot starting at a point
    :param start:
    :param visited:
    :param grid:
    :return:
    """
    area = 0
    fencing = 0

    visited.add(start)
    queue = [start]

    while len(queue) != 0:
        (x, y) = queue.pop(0)

        area += 1

        for dx, dy in DIRECTIONS:
            px = x + dx
            py = y + dy

            if not is_in_bounds(px, py, grid) or grid[x][y] != grid[px][py]:
                fencing += 1
                continue

            if (px, py) in visited:
                continue

            visited.add((px, py))
            queue.append((px, py))

    return area * fencing, visited


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


def main():
    grid = get_grid()

    total = find_total_price(grid)

    print(total)


if __name__ == "__main__":
    main()
