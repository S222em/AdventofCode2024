def similarity_score(list_a: list[int], list_b: list[int]) -> int:
    """
    Returns the similarity score between the 2 lists
    Score is sum of all values in A * occurrence in B
    :param list_a:
    :param list_b:
    :return:
    """
    return sum(a * list_b.count(a) for a in list_a)


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

    score = similarity_score(list_a, list_b)

    print(score)


if __name__ == "__main__":
    main()
