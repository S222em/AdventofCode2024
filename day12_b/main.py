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
    region = find_region(start, grid)

    # Update the visited squares
    visited.update(region)

    sides = find_sides(region)

    return len(region) * sides, visited


def find_sides(region):
    """
    Finds the amount of sides of given region
    :param region:
    :return:
    """
    sides = 0

    # Check from all directions
    for dx, dy in DIRECTIONS:
        border = set()

        # The rectangular border of the region
        min_x = min(region, key=lambda position: position[0])[0]
        min_y = min(region, key=lambda position: position[1])[1]
        max_x = max(region, key=lambda position: position[0])[0]
        max_y = max(region, key=lambda position: position[1])[1]

        # Whether we are going backwards through the region
        inverted = dx < 0 or dy < 0

        # Start of exploration, if inverted start on the other side
        start_x = max_x if inverted else min_x
        start_y = max_y if inverted else min_y

        x = start_x
        y = start_y

        # Loop until either x or y goes out of range of the region
        while min_x <= x <= max_x and min_y <= y <= max_y:
            # If x and y are in the region, check if it is a side,
            # e.g. square above is not in the region
            if (x, y) in region and is_side(x, y, dx, dy, region):
                # If this side has not already been counted
                # e.g. does not have an "adjacent" square.
                if not has_adjacent(x, y, dx, dy, border):
                    sides += 1

                # Add this to the outer border
                border.add((x, y))

            # Navigate to the next position
            # Keeps x or y inside the rectangular border
            x += dx
            y += dy

            if dx != 0 and (min_x > x or x > max_x):
                x = start_x
                y += dx

            if dy != 0 and (min_y > y or y > max_y):
                y = start_y
                x += dy

    return sides


def is_side(x, y, dx, dy, region):
    """
    Whether the given coordinate is a side from the perspective
    of the direction given by dx and dy
    :param x:
    :param y:
    :param dx:
    :param dy:
    :param region:
    :return:
    """
    ax = x - dx
    ay = y - dy

    # Check if the square "above" us is not in region
    # If it's not the current position is a side
    return (ax, ay) not in region


def has_adjacent(x, y, dx, dy, border):
    """
    Whether our current square has an adjacent border square that
    has already been counted.
    Only checks the "left" of the current square.
    As we explore left to right, the only possible location of it is on the left.
    :param x:
    :param y:
    :param dx:
    :param dy:
    :param border:
    :return:
    """
    ax = x - dy
    ay = y - dx

    return (ax, ay) in border


def find_region(start, grid):
    """
    Finds all the squares that belong to this region
    :param start:
    :param grid:
    :return:
    """
    region = {start}
    queue = [start]

    while len(queue) != 0:
        (x, y) = queue.pop(0)

        for dx, dy in DIRECTIONS:
            px = x + dx
            py = y + dy

            if not is_in_bounds(px, py, grid) or grid[x][y] != grid[px][py]:
                continue

            if (px, py) in region:
                continue

            region.add((px, py))
            queue.append((px, py))

    return region


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
