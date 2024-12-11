def get_stones():
    """
    Returns all the stones in the puzzle
    :return:
    """
    with open("puzzle.txt") as file:
        puzzle = file.read()

    return [int(stone) for stone in puzzle.split()]


def blink(stones: list[int]):
    """
    Does a single blink for all stones
    :param stones:
    :return:
    """
    blinked = list()

    for stone in stones:
        # Stone becomes 1 if it is 0.
        if stone == 0:
            blinked.append(1)
            continue

        number = str(stone)

        # If the number of digits is even we split the number in the middle and create 2 stones.
        if len(number) % 2 == 0:
            number_middle = len(number) // 2
            blinked.append(int(number[:number_middle]))
            blinked.append(int(number[number_middle:]))
            continue

        # If no other rules apply we multiply the stone by 2024
        blinked.append(stone * 2024)

    return blinked


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


def main():
    stones = get_stones()

    stones = do_blinks(stones, 25)

    print(len(stones))


if __name__ == "__main__":
    main()
