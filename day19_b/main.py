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


def count_design_combinations(design, towels, seen):
    """
    Counts all possible combinations of a given design.
    Uses a cache with previous results of this function.
    :param design:
    :param towels:
    :param seen:
    :return:
    """
    if not design:
        return 1

    if design in seen:
        return seen[design]

    total = 0

    for towel in towels:
        if not design.startswith(towel):
            continue

        total += count_design_combinations(design[len(towel):], towels, seen)

    seen[design] = total

    return total


def count_total_design_combinations(designs, towels):
    """
    Count the possible designs
    :param designs:
    :param towels:
    :return:
    """
    seen = dict()

    return sum(count_design_combinations(design, towels, seen) for design in designs)


def main():
    towels, designs = get_towels_and_designs()

    total = count_total_design_combinations(designs, towels)

    print(total)


if __name__ == "__main__":
    main()
