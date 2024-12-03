import re


def get_memory():
    """
    Returns the puzzle input in a single line
    :return:
    """
    with open("puzzle.txt") as file:
        memory = file.read()

    return memory


# Matches all valid mul instructions and extracts the 2 digits
MUL_INSTRUCTION_PATTERN = re.compile(r"mul\((\d+),(\d+)\)")


def do_uncorrupted_mul_instructions(memory):
    """
    Finds valid mul instructions and executes them.
    Returns the sum of all executed instructions.
    :param memory:
    :return:
    """
    valid_mul_instructions = MUL_INSTRUCTION_PATTERN.findall(memory)

    return sum(int(a) * int(b) for a, b in valid_mul_instructions)


def main():
    memory = get_memory()

    total = do_uncorrupted_mul_instructions(memory)

    print(total)


if __name__ == "__main__":
    main()
