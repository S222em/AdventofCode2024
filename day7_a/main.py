def get_equations():
    """
    Returns the expected result and the equation without operators
    :return:
    """
    with open("puzzle.txt") as file:
        lines = file.readlines()

    equations = list()

    for line in lines:
        [expected, numbers] = line.split(": ")
        equations.append((int(expected), [int(number) for number in numbers.split()]))

    return equations


def can_be(expected, numbers):
    """
    Whether the list of numbers can become expected with operators * and +
    Basically do the operation in reverse, so start with expected and use / and - until 1 number is left
    :param expected:
    :param numbers:
    :return:
    """
    i = len(numbers) - 1

    if i == 0 or expected <= 0:
        return False

    j = i - 1

    a = expected / numbers[i]
    b = expected - numbers[i]

    if (a == numbers[j] or b == numbers[j]) and j == 0:
        return True

    return can_be(a, numbers[:i]) or can_be(b, numbers[:i])


def get_total(equations):
    """
    Get the sum of true equations
    :param equations:
    :return:
    """
    total = 0

    for expected, numbers in equations:
        if not can_be(expected, numbers):
            continue

        total += expected

    return total


def main():
    equations = get_equations()

    total = get_total(equations)

    print(total)


if __name__ == "__main__":
    main()
