def get_register_and_instructions():
    """
    Parses the initial state of the registers from the puzzle file.
    Parses the program from the puzzle file.
    :return:
    """
    with open("puzzle.txt") as file:
        (registers, instructions) = file.read().split("\n\n")

    registers = map(lambda line: int(line.split(": ")[1]), registers.split("\n"))
    instructions = map(lambda instruction: int(instruction), instructions.split(": ")[1].split(","))

    return list(registers), list(instructions)


class Program:
    """
    Can be used to execute a given list of instructions
    """

    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7

    def __init__(self, registers, instructions):
        # A: 0
        # B: 1
        # C: 2
        self.registers = registers
        self.instructions = instructions
        self.pointer = 0
        self.output = list()

    def get_literal(self, operand):
        """
        Returns the value of the literal operand
        :param operand:
        :return:
        """
        return operand

    def get_combo(self, operand):
        """
        Returns the value of the combo operand
        :param operand:
        :return:
        """
        if operand <= 3:
            return operand

        if 4 <= operand <= 6:
            return self.registers[operand - 4]

        if operand == 7:
            raise ValueError("7 is not a valid combo operand")

    def adv(self, operand):
        """
        Performs division where
        - The numerator is the value in register A
        - The denominator is the combo operand
        Result of division is truncated to an integer and stored in register A
        :param operand:
        :return:
        """
        numerator = self.registers[0]
        denominator = pow(2, self.get_combo(operand))

        self.registers[0] = numerator // denominator

    def bxl(self, operand):
        """
        Calculates the bitwise XOR of register B with literal operand
        Result is stored in register B
        :param operand:
        :return:
        """
        self.registers[1] = self.registers[1] ^ self.get_literal(operand)

    def bst(self, operand):
        """
        Discards everything except the lowest 3 bits, with modulo 8
        Result is stored in register B
        :param operand:
        :return:
        """
        self.registers[1] = self.get_combo(operand) % 8

    def jnz(self, operand):
        """
        Jumps the instruction pointer to the value of the literal operand
        Returns whether the program should advance the instruction pointer by 2 after
        :param operand:
        :return:
        """
        if self.registers[0] == 0:
            return True

        self.pointer = self.get_literal(operand)

        return False

    def bxc(self, _):
        """
        Calculates the bitwise XOR between register B and C
        Result is stored in register B
        Given operand is ignored
        :param _:
        :return:
        """
        self.registers[1] = self.registers[1] ^ self.registers[2]

    def out(self, operand):
        """
        Adds the combo operand lowest 3 bits to the output.
        :param operand:
        :return:
        """
        self.output.append(self.get_combo(operand) % 8)

    def bdv(self, operand):
        """
        Performs division where
        - The numerator is the value in register A
        - The denominator is the combo operand
        Result of division is truncated to an integer and stored in register B
        :param operand:
        :return:
        """
        numerator = self.registers[0]
        denominator = pow(2, self.get_combo(operand))

        self.registers[1] = numerator // denominator

    def cdv(self, operand):
        """
        Performs division where
        - The numerator is the value in register A
        - The denominator is the combo operand
        Result of division is truncated to an integer and stored in register C
        :param operand:
        :return:
        """
        numerator = self.registers[0]
        denominator = pow(2, self.get_combo(operand))

        self.registers[2] = numerator // denominator

    def step(self):
        """
        Advances the program by one step
        Returns whether the program should be halted
        :return:
        """
        if self.pointer + 1 >= len(self.instructions):
            return True

        opcode = self.instructions[self.pointer]
        operand = self.instructions[self.pointer + 1]

        if opcode == Program.ADV:
            self.adv(operand)

        if opcode == Program.BXL:
            self.bxl(operand)

        if opcode == Program.BST:
            self.bst(operand)

        if opcode == Program.JNZ:
            advance_pointer = self.jnz(operand)
            if not advance_pointer:
                return

        if opcode == Program.BXC:
            self.bxc(operand)

        if opcode == Program.OUT:
            self.out(operand)

        if opcode == Program.BDV:
            self.bdv(operand)

        if opcode == Program.CDV:
            self.cdv(operand)

        self.pointer += 2

        return False

    def run(self):
        """
        Runs the program
        :return:
        """
        while True:
            halt = self.step()
            if halt:
                break


# Register A: 117440
# Register B: 0
# Register C: 0
#
# Program: 0,3,5,4,3,0
#
# [117440, 0, 0] []
# [14680, 0, 0] [0]
# [1835, 0, 0] [0, 3]
# [229, 0, 0] [0, 3, 5]
# [28, 0, 0] [0, 3, 5, 4]
# [3, 0, 0] [0, 3, 5, 4, 3]
# [0, 0, 0] [0, 3, 5, 4, 3, 0]
#
# The image above depicts the state of the program when a new item is added to the output
# As visible, each time the program adds an item to the output, the output after that is register A // 8
# This means that, in order to reach (in this case) 6 outputs, we need to number to be divisible by 8.
# As there is a jump statement (3 0) at the end, we will keep repeating until register A is 0.
# This also means that if we start backwards, we will start with a=0, as A should be 0 at the end.
# Another observation is that register B and C will remain 0, which is important for this solution to work.
# So now we know that between each output the value in register A decreases by 8, we can use this to find the answer.
# As we start at a=0 and at the last instruction, the output of the program will be [0], as A is 0 and can not be divided by 8 anymore,
# the program will stop. Now for the next output we want, 3, we need to make sure the program does not end at this step,
# which means that A != 0, and as it's one output from the end, A // 8 == 0, which means that any A lower than 8
# and with output [3, 0] will work, to do this, simply keep incrementing A by 1 until the wanted output is found.
# Then for the next output, [4, 3, 0] we want an A where A // 8**2 == 0, so to get the minimum where this will be true,
# we multiply the value in register A b *8, and this will be the lowest number that would keep A // 8**2 == 0 true,
# now again we can find the specific value A by incrementing it by 1 until we find output [4, 3, 0].
# Just continue doing this until the whole output is matched, the resulting value in register A is the answer.
# Now, the only thing that makes this work is that both the example and actual puzzle share the jump statement at the end,
# the fact that at each output A = A // 8, and that the output is always A % 8.


def find_register_a_value(registers, instructions):
    """
    Finds the value of register A for which the program will copy itself
    :param registers:
    :param instructions:
    :return:
    """
    program = Program(registers, instructions)

    # At the end of the program there is a jump
    # This means that to end the program, a needs to be 0 at the end
    # As we work back from the end to the start a will start at 0
    a = 0
    i = 1

    while True:
        # Reset the program to it's initial state
        program.registers = [a, registers[1], registers[2]]
        program.pointer = 0
        program.output = list()

        program.run()

        # If the output is not long enough increment a by 1
        if len(program.output) < i:
            a += 1
            continue

        # The end of the output matches the end of the instructions
        # This means that we found a valid a for this stage of the program
        if program.output[-i:] == instructions[-i:]:
            i += 1

            # If i has gone out of bounds, we have verified the output is a copy of itself
            # Which means we can return a, this answer
            if i > len(instructions):
                return a

            a *= 8

            continue

        a += 1


def main():
    registers, instructions = get_register_and_instructions()

    register_a = find_register_a_value(registers, instructions)

    print(register_a)


if __name__ == "__main__":
    main()
