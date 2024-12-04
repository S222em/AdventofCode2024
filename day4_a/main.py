def get_puzzle():
    """
    Returns the puzzle input in lines with newline chars stripped
    :return:
    """
    with open("puzzle.txt") as file:
        lines = file.readlines()

    return [line.strip() for line in lines]


WORD = "XMAS"
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)]


def find_word_occurrences(puzzle: list[str]) -> int:
    """
    Find occurrences of the word XMAS
    :param puzzle:
    :return:
    """
    words_found = 0

    for x, row in enumerate(puzzle):
        for y, char in enumerate(row):
            # Look from the first char of the word.
            # As we always start from the first char it's not possible to get duplicates.
            if char != WORD[0]:
                continue

            words_found += find_words_from(x, y, puzzle)

    return words_found


def find_words_from(x: int, y: int, puzzle: list[str]) -> int:
    """
    Finds occurrences of the word from the given x, y coordinate
    The x, y coordinate is the location of the first char in the word
    :param x:
    :param y:
    :param puzzle:
    :return:
    """
    words_found = 0

    # Check every direction we can go in from x, y
    for dx, dy in DIRECTIONS:
        px = x
        py = y

        # Skip first char as we already know it's position
        # Then loop until:
        # - We run out of bounds
        # - The char at px, py is not the one we are looking for
        # - We found the whole word
        for char in WORD[1:]:
            px += dx
            py += dy
            if not is_in_bounds(px, py, puzzle):
                break

            if puzzle[px][py] != char:
                break

            if char == WORD[-1]:
                words_found += 1

    return words_found


def is_in_bounds(x: int, y: int, puzzle: list[str]) -> bool:
    """
    Whether the given x, y is in bounds of the puzzle
    :param x:
    :param y:
    :param puzzle:
    :return:
    """
    x_in_bounds = 0 <= x < len(puzzle)
    y_in_bounds = 0 <= y < len(puzzle[0])

    return x_in_bounds and y_in_bounds


def main():
    puzzle = get_puzzle()

    occurrences = find_word_occurrences(puzzle)

    print(occurrences)


if __name__ == "__main__":
    main()
