def get_reports() -> list[list[int]]:
    """
    Loads and parses the puzzle input to a list of reports
    :return:
    """
    with open("puzzle.txt") as file:
        lines = file.readlines()

    return [[int(level) for level in line.split()] for line in lines]


def is_report_safe(report: list[int]) -> bool:
    """
    Whether a report is safe
    This is True if:
    - The report is constantly ascending/descending
    - No duplicate values are present
    - Steps are at least 1 and at most 3
    :param report:
    :return:
    """
    ascending = None

    for i, level in enumerate(report[1:]):
        if level == report[i]:
            return False

        if ascending is None:
            ascending = level > report[i]

        if (level > report[i]) != ascending or 1 < abs(report[i] - level) > 3:
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
