import re
from functools import reduce
from operator import mul

EXTRACT_PATTERN = re.compile(r"p=(.+),(.+) v=(.+),(.+)")
SECONDS = 100
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
    x = (position[0] + speed[0]) % WIDTH
    y = (position[1] + speed[1]) % HEIGHT

    return x, y


def find_safety_factor_after(robots, seconds=100):
    """
    Find the safety factor after a certain amount of time has passed
    :param robots:
    :param seconds:
    :return:
    """
    for _ in range(seconds):
        robots = move_robots(robots)

    return get_safety_factor(robots)


def get_safety_factor(robots):
    """
    Returns the safety factor
    :param robots:
    :return:
    """
    mx = WIDTH // 2
    my = HEIGHT // 2

    quadrants = [0, 0, 0, 0]

    for position, _ in robots:
        if position[0] < mx and position[1] < my:
            quadrants[0] += 1

        if position[0] > mx and position[1] < my:
            quadrants[1] += 1

        if position[0] < mx and position[1] > my:
            quadrants[2] += 1

        if position[0] > mx and position[1] > my:
            quadrants[3] += 1

    return reduce(mul, quadrants)


def main():
    robots = get_robots()

    safety_factor = find_safety_factor_after(robots)

    print(safety_factor)


if __name__ == "__main__":
    main()
