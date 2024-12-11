from collections import Counter


# As we need much more iterations of blink in part 2, it's no longer runs in acceptable time
# Therefor, instead of "blinking" every stone, we rather create a dictionary with as key the number on the stone
# and as a value the amount of times we have that specific stone.
# This way we can reduce the amount of iterations significantly as we "blink" all stones with the same number at once.

def get_stones():
    """
    Returns the amount of times a stone appears in the puzzle
    :return:
    """
    with open("puzzle.txt") as file:
        puzzle = file.read()

    return Counter(int(stone) for stone in puzzle.split())


def blink(before: dict[int, int]):
    """
    Does a single blink for all stones
    :param before:
    :return:
    """
    after = dict()

    for stone, count in before.items():
        # Stone becomes 1 if it is 0.
        if stone == 0:
            after[1] = after.setdefault(1, 0) + count
            continue

        number = str(stone)

        # If the number of digits is even we split the number in the middle and create 2 stones.
        if len(number) % 2 == 0:
            middle = len(number) // 2
            left = int(number[:middle])
            right = int(number[middle:])

            after[left] = after.setdefault(left, 0) + count
            after[right] = after.setdefault(right, 0) + count

            continue

        # If no other rules apply we multiply the stone by 2024
        after[stone * 2024] = after.setdefault(stone * 2024, 0) + count

    return after


def do_blinks(stones, amount):
    """
    Does the specified amount of blinks
    :param stones:
    :param amount:
    :return:
    """
    for _ in range(amount):
        stones = blink(stones)

    return stones


def count_stones(stones):
    """
    Counts the total amount of stones
    :param stones:
    :return:
    """
    return sum(amount for amount in stones.values())


def main():
    stones = get_stones()

    stones = do_blinks(stones, 75)

    count = count_stones(stones)

    print(count)


if __name__ == "__main__":
    main()
