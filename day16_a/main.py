def get_maze():
    """
    Returns the maze
    :return:
    """
    with open("puzzle.txt") as file:
        lines = file.readlines()

    return [[char for char in line] for line in lines]


def find_char(find, maze):
    """
    Finds the specified char in the maze
    :param find:
    :param maze:
    :return:
    """
    for x, row in enumerate(maze):
        for y, char in enumerate(row):
            if char != find:
                continue

            return x, y

    return None


def find_start(maze):
    """
    Finds the starting point in the maze
    :param maze:
    :return:
    """
    return find_char("S", maze)


def find_end(maze):
    """
    Finds the end point in the maze
    :param maze:
    :return:
    """
    return find_char("E", maze)


def find_lowest_score(maze):
    """
    Searches the maze for the lowest possible score to get start->end.
    Uses a modified version of dijkstra's to get the lowest possible score.
    :param maze:
    :return:
    """
    start = find_start(maze)
    end = find_end(maze)

    queue = [(start, (0, 1), 0), ]
    visited = set()

    while queue:
        # Get the lowest score so far from the queue
        item = min(queue, key=lambda item: item[2])
        # Remove the item from the queue
        queue.remove(item)
        position, direction, score = item

        # Can't move backwards, so this little formula makes sure we can only move left, straight or right
        for dx, dy in (direction, (-direction[1], direction[0]), (direction[1], -direction[0])):
            x = position[0] + dx
            y = position[1] + dy

            # The new position is a wall so we can not do anything.
            # The new position has already been visited.
            if maze[x][y] == "#" or (x, y) in visited:
                continue

            visited.add((x, y))

            # If we made a 90-degree turn it adds 1000 points, +1 for the step
            new_score = score + (1 if direction == (dx, dy) else 1001)

            # We found the end
            # As we always look at the lowest score first,
            # this is the lowest score in which we can reach the end
            if (x, y) == end:
                return new_score

            # Add the new position, direction and score back into the queue
            queue.append(((x, y), (dx, dy), new_score))

    return 0


def main():
    maze = get_maze()

    lowest_score = find_lowest_score(maze)

    print(lowest_score)


if __name__ == "__main__":
    main()
