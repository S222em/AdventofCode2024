def get_towels_and_designs():
    """
    Returns the available towels in a set and the designs
    that have to be made with them
    :return:
    """
    with open("puzzle.txt") as file:
        [towels, designs] = file.read().split("\n\n")

    towels = set(towels.strip().split(", "))
    designs = designs.split("\n")

    return towels, designs


def is_possible(design, towels):
    """
    Whether it's possible to get the given design with the available towels
    :param design:
    :param towels:
    :return:
    """
    if not design:
        return True

    for towel in towels:
        if not design.startswith(towel):
            continue

        if is_possible(design[len(towel):], towels):
            return True

    return False


def count_possible(designs, towels):
    """
    Count the possible designs
    :param designs:
    :param towels:
    :return:
    """
    return sum(is_possible(design, towels) for design in designs)


def main():
    towels, designs = get_towels_and_designs()

    total = count_possible(designs, towels)

    print(total)


if __name__ == "__main__":
    main()
