import re

BUTTON_A_TOKENS = 3
BUTTON_B_TOKENS = 1
MAX_BUTTON_PRESSES = 100000

BUTTON_PATTERN = re.compile(r"Button [AB]: X\+(\d+), Y\+(\d+)")
PRIZE_PATTERN = re.compile(r"Prize: X=(\d+), Y=(\d+)")
PRIZE_CONVERSION_ERROR = 10000000000000


def get_machine_from(lines):
    """
    Returns the position of the prize and the amount a button press moves the claw
    Parsed from the given lines
    :param lines:
    :return:
    """
    [button_a, button_b, prize] = lines.split("\n")

    (px, py) = PRIZE_PATTERN.match(prize).group(1, 2)
    (dx_a, dy_a) = BUTTON_PATTERN.match(button_a).group(1, 2)
    (dx_b, dy_b) = BUTTON_PATTERN.match(button_b).group(1, 2)

    # Add the conversion error to the prizes position
    p = (int(px) + PRIZE_CONVERSION_ERROR, int(py) + PRIZE_CONVERSION_ERROR)
    ba = (int(dx_a), int(dy_a))
    bb = (int(dx_b), int(dy_b))

    return p, ba, bb


def get_machines():
    """
    Parses the puzzle file into a list of machines
    :return:
    """
    with open("puzzle.txt") as file:
        machines = file.read().split("\n\n")

    return list(map(get_machine_from, machines))


def find_fewest_tokens_for(prize, a, b):
    """
    Finds the fewest amount of tokens needed to get the prize.
    :param prize:
    :param a:
    :param b:
    :return:
    """
    # Formulas below are from the following equations:
    # { i * ax + j * bx = px
    # { i * ay + j * by = py
    # Below we eliminate j, find i and then plug i back into one of the equations above
    # to find j.
    # After that simply test if i and j were supposed to be integers, by checking if the reached coordinate
    # matches the prize coordinate, if they don't the prize is not reachable so return 0.

    i = (prize[0] * b[1] - prize[1] * b[0]) // (a[0] * b[1] - a[1] * b[0])
    j = (prize[0] - i * a[0]) // b[0]

    x = i * a[0] + j * b[0]
    y = i * a[1] + j * b[1]

    if (x, y) != prize:
        return 0

    return i * BUTTON_A_TOKENS + j * BUTTON_B_TOKENS


def find_fewest_tokens(machines):
    """
    Finds the least tokens needed to get all possible prizes
    :param machines:
    :return:
    """
    total = 0

    for prize, a, b in machines:
        total += find_fewest_tokens_for(prize, a, b)

    return total


def main():
    machines = get_machines()

    total = find_fewest_tokens(machines)

    print(total)


if __name__ == "__main__":
    main()
