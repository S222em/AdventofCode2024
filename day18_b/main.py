from collections import deque

START = (0, 0)

# For example:
# END = (6, 6)


# For real:
END = (70, 70)


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
    visited = corrupted.copy()

    queue = deque(((start, set()),))

    while queue:
        (x, y), path = queue.popleft()

        for dx, dy in DIRECTIONS:
            px = x + dx
            py = y + dy

            if not is_in_bounds(x, y, start, end):
                continue

            if (px, py) in visited:
                continue

            visited.add((px, py))
            next_path = path | {(px, py)}

            if (px, py) == end:
                return next_path

            queue.append(((px, py), next_path))

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


def find_first_blocking_byte(start, end, incoming):
    """
    Finds the first falling byte that blocks the path from start->end
    :param start:
    :param end:
    :param incoming:
    :return:
    """
    corrupted = set()
    path = None

    for x, y in incoming:
        corrupted.add((x, y))
        if path and (x, y) not in path:
            continue

        path = find_shortest_path(start, end, corrupted)
        if not path:
            return x, y

    return None


def main():
    incoming = get_incoming()

    first = find_first_blocking_byte(START, END, incoming)

    print(f"{first[0]},{first[1]}")


if __name__ == "__main__":
    main()
