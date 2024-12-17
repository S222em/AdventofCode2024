from day17_a.main import Program


def test_bst():
    program = Program([0, 0, 9], [2, 6])
    program.run()

    assert program.registers[1] == 1


def test_bxl():
    program = Program([0, 29, 0], [1, 7])
    program.run()

    assert program.registers[1] == 26


def test_bxc():
    program = Program([0, 2024, 43690], [4, 0])
    program.run()

    assert program.registers[1] == 44354


def test_example_1():
    program = Program([10, 0, 0], [5, 0, 5, 1, 5, 4])
    program.run()

    assert program.output == ["0", "1", "2"]


def test_example_2():
    program = Program([2024, 0, 0], [0, 1, 5, 4, 3, 0])
    program.run()

    assert program.output == ["4", "2", "5", "6", "7", "7", "7", "7", "3", "1", "0"]
    assert program.registers[0] == 0
