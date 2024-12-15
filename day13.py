from typing import Union
from time import perf_counter
from utils import Day


def solve_linear(
    buttonA: tuple[int, int],
    buttonB: tuple[int, int],
    target: tuple[int, int],
    target_offset: int = 0,
) -> tuple[int, int]:
    X, Y = 0, 1
    prize = target[X] + target_offset, target[Y] + target_offset
    """
    n * bA[X] + m * bB[X] = prize[X]
    n * bA[Y] + m * bB[Y] = prize[Y]

    2 equations, with 2 unknown

    linear algebra =/
    3blue1Brown (Cramer's rule):
        https://www.youtube.com/watch?v=jBsC34PxzoM
    actual how to (Cramer's rule):
        https://www.youtube.com/watch?v=vXqlIOX2itM

    n = Dn/D,  m = Dm/D

    D = bA[X] * bB[Y] - bA[Y] * bB[X]
    Dn = prize[X] * bB[Y] - prize[Y] * bB[X]
    Dm = prize[X] * bA[Y] - prize[Y] * bA[X]
    """
    D = buttonA[X] * buttonB[Y] - buttonA[Y] * buttonB[X]
    Dn = prize[X] * buttonB[Y] - prize[Y] * buttonB[X]
    Dm = prize[Y] * buttonA[X] - prize[X] * buttonA[Y]
    n, rn = divmod(Dn, D)
    m, rm = divmod(Dm, D)
    if rm != 0 or rn != 0:
        return 0, 0
    return n, m


def part_one(data: list[str]) -> Union[str, int]:
    total = 0
    for game in [x.split("\n") for x in data]:

        buttonA = int(game[0][game[0].find("+") + 1 : game[0].find(",")]), int(game[0][game[0].rfind("+") + 1 :])
        buttonB = int(game[1][game[1].find("+") + 1 : game[1].find(",")]), int(game[1][game[1].rfind("+") + 1 :])
        prize = int(game[2][game[2].find("=") + 1 : game[2].find(",")]), int(game[2][game[2].rfind("=") + 1 :])

        a, b = solve_linear(buttonA, buttonB, prize)
        total += 3 * a + b

    return total


def part_two(data: list[str]) -> Union[str, int]:
    total = 0
    for game in [x.split("\n") for x in data]:
        buttonA = int(game[0][game[0].find("+") + 1 : game[0].find(",")]), int(game[0][game[0].rfind("+") + 1 :])
        buttonB = int(game[1][game[1].find("+") + 1 : game[1].find(",")]), int(game[1][game[1].rfind("+") + 1 :])
        prize = int(game[2][game[2].find("=") + 1 : game[2].find(",")]), int(game[2][game[2].rfind("=") + 1 :])

        a, b = solve_linear(buttonA, buttonB, prize, 10000000000000)
        total += 3 * a + b

    return total


def main():
    test_case_1 = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

    test = False
    day = 13
    if test:
        print("TEST VALUES")
        data = test_case_1.strip().split("\n\n")
    else:
        data = Day.get_data(day).strip().split("\n\n")

    start = perf_counter()
    print(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    print(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    print(f"the whole day {day} took {perf_counter() - start:.4f}s")


main()
