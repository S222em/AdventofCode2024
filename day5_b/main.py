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


def order(update: list[int], rules: list[(int, int)]) -> list[int]:
    """
    Order a given update with the rules
    :param update:
    :param rules:
    :return:
    """
    ordered = list()

    while len(update) != 0:
        a = update.pop(0)
        if all(any(rule == (a, b) for rule in rules) for b in update):
            ordered.append(a)
            continue

        update.append(a)

    return ordered


def sum_middle_of_ordered_updates(updates: list[list[int]], rules: list[(int, int)]) -> int:
    """
    Sum the middle item of the newly ordered updates
    :param updates:
    :param rules:
    :return:
    """
    total = 0

    for update in updates:
        if is_in_right_order(update, rules):
            continue

        ordered = order(update, rules)
        print(ordered)
        total += ordered[len(ordered) // 2]

    return total


def main():
    rules, updates = get_rules_and_updates()

    total = sum_middle_of_ordered_updates(updates, rules)

    print(total)


if __name__ == "__main__":
    main()
