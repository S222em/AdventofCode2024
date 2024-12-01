def total_distance(list_a: list[int], list_b: list[int]) -> int:
    """
    Finds the total difference between the 2 lists
    :param list_a:
    :param list_b:
    :return:
    """
    # Sort the lists from small->high
    # Needed as we need to compare each smallest number in the lists
    list_a.sort()
    list_b.sort()

    total = 0

    for a, b in zip(list_a, list_b):
        total += abs(b - a)

    return total


def get_lists() -> (list[int], list[int]):
    """
    Parses the puzzle file into list a and b:

    A   B
    3   4
    4   3
    2   5
    1   3
    3   9
    3   3
    :return: Tuple of list A and B
    """
    list_a = []
    list_b = []

    with open("puzzle.txt") as file:
        lines = file.readlines()

    for line in lines:
        [left, right] = line.split(maxsplit=1)

        list_a.append(int(left))
        list_b.append(int(right))

    return list_a, list_b


def main():
    list_a, list_b = get_lists()

    total = total_distance(list_a, list_b)

    print(total)


if __name__ == "__main__":
    main()
