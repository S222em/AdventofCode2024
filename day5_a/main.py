def get_rules_and_updates():
    """
    Parses the puzzle files into:
    - Rules: list of tuple (before, after)
    - Updates: list of list of int
    :return:
    """
    with open("puzzle.txt") as file:
        text = file.read()

    [rules_str, updates_str] = text.split("\n\n")

    rules = list()

    for rule in rules_str.split("\n"):
        [before, after] = rule.split("|")
        rules.append((int(before), int(after)))

    updates = list()

    for update in updates_str.split("\n"):
        updates.append([int(item) for item in update.split(",")])

    return rules, updates


def is_in_right_order(update: list[int], rules: list[(int, int)]) -> bool:
    """
    Whether a given update is in the right order
    :param update:
    :param rules:
    :return:
    """
    for i, a in enumerate(update):
        if not all(any(rule == (a, b) for rule in rules) for b in update[i + 1:]):
            return False

    return True


def sum_middle_of_correct_updates(updates: list[list[int]], rules: list[(int, int)]) -> int:
    """
    Sum the middle item of the already correctly sorted updates
    :param updates:
    :param rules:
    :return:
    """
    total = 0

    for update in updates:
        if not is_in_right_order(update, rules):
            continue

        total += update[len(update) // 2]

    return total


def main():
    rules, updates = get_rules_and_updates()

    total = sum_middle_of_correct_updates(updates, rules)

    print(total)


if __name__ == "__main__":
    main()
