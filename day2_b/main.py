def get_reports() -> list[list[int]]:
    """
    Loads and parses the puzzle input to a list of reports
    :return:
    """
    with open("puzzle.txt") as file:
        lines = file.readlines()

    return [[int(level) for level in line.split()] for line in lines]


def is_following_rules(a: int, b: int, ascending: bool) -> bool:
    """
    Whether the given 2 levels follow the rules:
    - Ascending/descending as described in arg "ascending"
    - Difference is min 1 and max 3
    :param a:
    :param b:
    :param ascending:
    :return:
    """
    return 1 <= abs(a - b) <= 3 and (a > b) == ascending


# Initially made the mistake that if i and i - 1 are not following the rules that
# one of them is a "bad" level.
# Unfortunately this is not true, take case: [40, 41, 39, 37]
# Here the rule will not be followed at i = 2, (41 and 39)
# But as we can see the report can be valid if i = 0 is removed
# Therefor the "bad" level does not have to be i or i - 1, but any j for j <= i

def is_report_safe(report: list[int], tolerate=True) -> bool:
    """
    Whether a report is safe
    This is True if:
    - The report is constantly ascending/descending
    - Steps are at least 1 and at most 3
    - Maximum of one level can be removed to meet above conditions
    :param report:
    :param tolerate: Whether to tolerate a bad level
    :return:
    """
    i = 1
    ascending = report[i] > report[i - 1]

    while i < len(report):
        if is_following_rules(report[i], report[i - 1], ascending):
            i += 1
            continue

        if not tolerate:
            return False

        # Try to remove levels in the report where j <= i and see if any is safe
        for j in range(i + 1):
            if is_report_safe(report[:j] + report[j + 1:], tolerate=False):
                return True

        return False

    return True


def count_safe_reports(reports: list[list[int]]) -> int:
    """
    Returns the amount of safe reports
    :param reports:
    :return:
    """
    return sum(1 for report in reports if is_report_safe(report))


def main():
    reports = get_reports()

    safe_reports = count_safe_reports(reports)

    print(safe_reports)


if __name__ == "__main__":
    main()
