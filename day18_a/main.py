from collections import deque

START = (0, 0)

# For example:
# END = (6, 6)
# AMOUNT = 12

# For real:
END = (70, 70)
AMOUNT = 1024


def get_incoming():
    """
    Returns a list of all incoming bytes
    :return:
    """
    with open("puzzle.txt") as file:
        lines = file.readlines()

    incoming = list()

    for line in lines:
        [left, right] = line.split(",")

        incoming.append((int(left), int(right)))

    return incoming


def fall(incoming, amount):
    """
    Lets the specified amount of incoming bytes fall
    Returns a set of all tiles that have become corrupted as a result.
    :param incoming:
    :param amount:
    :return:
    """
    corrupted = set()

    for i in range(amount):
        x, y = incoming[i]

        corrupted.add((x, y))

    return corrupted


DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def find_shortest_path(start, end, corrupted):
    """
    Finds the shortest path from start->end.
    Corrupted tiles are avoided
    :param start:
    :param end:
    :param corrupted:
    :return:
    """
    visited = set()

    queue = deque(((start, 0),))

    while queue:
        (x, y), steps = queue.popleft()

        for dx, dy in DIRECTIONS:
            px = x + dx
            py = y + dy

            if not is_in_bounds(x, y, start, end):
                continue

            if (px, py) in corrupted or (px, py) in visited:
                continue

            if (px, py) == end:
                return steps + 1

            visited.add((px, py))

            queue.append(((px, py), steps + 1))

    return None


def is_in_bounds(x, y, start, end):
    """
    Whether x and y are in bounds.
    The bounds are given by start and end, as they are both the most extreme values.
    :param x:
    :param y:
    :param start:
    :param end:
    :return:
    """
    x_in_bounds = start[0] <= x <= end[0]
    y_in_bounds = start[1] <= y <= end[1]

    return x_in_bounds and y_in_bounds


def main():
    incoming = get_incoming()

    corrupted = fall(incoming, AMOUNT)

    steps = find_shortest_path(START, END, corrupted)

    print(steps)


if __name__ == "__main__":
    main()
