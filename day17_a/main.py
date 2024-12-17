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
        self.output.append(str(self.get_combo(operand) % 8))

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


def main():
    registers, instructions = get_register_and_instructions()

    program = Program(registers, instructions)

    program.run()

    print(",".join(program.output))


if __name__ == "__main__":
    main()
