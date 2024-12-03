import re


def get_memory():
    """
    Returns the puzzle input in a single line
    :return:
    """
    with open("puzzle.txt") as file:
        memory = file.read()

    return memory


# Matches all valid instructions
INSTRUCTION_PATTERN = re.compile(r"do\(\)|don't\(\)|mul\(\d+,\d+\)")
MUL_PATTERN = re.compile(r"mul\((\d+),(\d+)\)")


def do_instructions(memory):
    """
    Finds valid mul instructions and executes them if enabled.
    Returns the sum of all executed instructions.
    :param memory:
    :return:
    """
    instructions = INSTRUCTION_PATTERN.findall(memory)

    total = 0
    enabled = True

    for instruction in instructions:
        # Enable/disable mul instructions
        if instruction in ("do()", "don't()"):
            enabled = instruction == "do()"
            continue

        # Mul is not enabled so skip
        if not enabled:
            continue

        # Extract a and b from the string
        (a, b) = MUL_PATTERN.search(instruction).group(1, 2)

        total += int(a) * int(b)

    return total


def main():
    memory = get_memory()

    total = do_instructions(memory)

    print(total)


if __name__ == "__main__":
    main()
