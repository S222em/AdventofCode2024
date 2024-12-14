import re

EXTRACT_PATTERN = re.compile(r"p=(.+),(.+) v=(.+),(.+)")
PICTURE_AMOUNT = 10000
PICTURE_INTERVAL = 0.5
WIDTH = 101
HEIGHT = 103


def get_robots():
    """
    Returns all robots in the puzzle as a tuple:
    - 0: position
    - 1: speed
    :return:
    """
    with open("puzzle.txt") as file:
        lines = file.readlines()

    robots = list()

    for line in lines:
        (x, y, vx, vy) = EXTRACT_PATTERN.match(line).group(1, 2, 3, 4)
        robots.append(((int(x), int(y)), (int(vx), int(vy))))

    return robots


def move_robots(robots):
    """
    Moves all given robots by 1 step
    :param robots:
    :return:
    """
    for i, robot in enumerate(robots):
        robots[i] = (move_robot(*robot), robot[1])

    return robots


def move_robot(position, speed):
    """
    Moves the given robot in speed
    Teleports to the other side of the map if a wall is hit
    :param position:
    :param speed:
    :return:
    """
    x = position[0] + speed[0]
    y = position[1] + speed[1]

    if x < 0:
        x += WIDTH

    if x >= WIDTH:
        x -= WIDTH

    if y < 0:
        y += HEIGHT

    if y >= HEIGHT:
        y -= HEIGHT

    return x, y


def create_picture(robots, t):
    """
    Creates a picture of the given robots
    :param robots:
    :param t:
    :return:
    """
    picture = ""

    for x in range(0, WIDTH):
        for y in range(0, HEIGHT):
            if any(position == (x, y) for position, _ in robots):
                picture += "*"
                continue

            picture += " "

        picture += "\n"

    return picture + f"Seconds elapsed: {t}"


# For some weird reason the picture of the tree exists
# if no robots are overlapping.
# No clue why this is the case, but it works.

def find_non_overlapping_picture(robots):
    """
    Find a picture where no robots are overlapping
    :param robots:
    :return:
    """
    t = 0

    while True:
        t += 1
        robots = move_robots(robots)
        if not overlapping_robots(robots):
            return create_picture(robots, t)


def overlapping_robots(robots):
    """
    Whether robots are overlapping
    :param robots:
    :return:
    """
    # Simply put all positions in a set and check if it's the same length
    positions = set(position for position, _ in robots)

    return len(robots) != len(positions)


def main():
    robots = get_robots()

    picture = find_non_overlapping_picture(robots)

    print(picture)


if __name__ == "__main__":
    main()
