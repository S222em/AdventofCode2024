from collections import deque

DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))
MIN_TIME_SAVE = 100


def get_track():
    """
    Returns the track from the puzzle file
    :return:
    """
    with open("puzzle.txt") as file:
        lines = file.readlines()

    return lines


def find_char(char_a, track):
    """
    Finds a char in the track
    :param char_a:
    :param track:
    :return:
    """
    for x, row in enumerate(track):
        for y, char_b in enumerate(row):
            if char_a != char_b:
                continue

            return x, y

    return None


def find_shortest_path(track):
    """
    Finds the shortest possible path from S->E.
    Returns the positions in this path and the time it takes to get there.
    :param track:
    :return:
    """
    start = find_char("S", track)
    end = find_char("E", track)

    visited = {start}
    queue = deque(((start, 0, {start: 0}),))

    while queue:
        (x, y), time, path = queue.popleft()

        for dx, dy in DIRECTIONS:
            px = x + dx
            py = y + dy

            if track[px][py] == "#":
                continue

            if (px, py) in visited:
                continue

            new_time = time + 1
            new_path = path | {(px, py): new_time}
            visited.add((px, py))

            if (px, py) == end:
                return new_path

            queue.append(((px, py), new_time, new_path))

    return None


def find_amount_of_cheats(path, min_time):
    """
    Finds all possible cheats and time they save
    Returns the total amount of cheats that save more than min_time
    :param path:
    :param min_time:
    :return:
    """
    total = 0

    for position, time in path.items():
        for dx, dy in DIRECTIONS:
            # See where we can go in 2 picoseconds
            x = position[0] + dx * 2
            y = position[1] + dy * 2

            # At the second picosecond we should be back on the path
            if (x, y) not in path:
                continue

            # See if the time we save is more or equal then the minimum time save
            dt = path[(x, y)] - time - 2
            if dt < min_time:
                continue

            total += 1

    return total


def main():
    track = get_track()

    path = find_shortest_path(track)

    total = find_amount_of_cheats(path, MIN_TIME_SAVE)

    print(total)


if __name__ == "__main__":
    main()
