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
    Whether the list of numbers can become expected with operators *, + and ||
    :param expected:
    :param numbers:
    :return:
    """

    if len(numbers) <= 1 or expected <= 0:
        return expected == numbers[0]

    results = (expected / numbers[-1], expected - numbers[-1])

    if any(can_be(result, numbers[:-1]) for result in results):
        return True

    # If the expected number does not end with the last number, concat is not possible
    if not str(int(expected)).endswith(str(numbers[-1])):
        return False

    # Strip any .0
    expected_str = str(expected)[:-2] if str(expected).endswith(".0") else str(expected)
    result_str = expected_str[:-len(str(numbers[-1]))]

    # If the result still has a . it's not possible to get the expected result as it can only be an int
    if not result_str or "." in result_str:
        return False
    
    if can_be(int(result_str), numbers[:-1]):
        return True

    return False


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
