from typing import Union, Callable
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def get_parenth_level(equation: list[int | str]) -> list[int]:
    parenth_level = []
    level = 0
    for c in equation:
        if c == "(":
            level += 1
        elif c == ")":
            level -= 1
        parenth_level.append(level)
    return parenth_level


def calc_eq(equation: list[str | int]) -> int:
    if len(equation) % 2 != 1:
        raise NotImplementedError
    if len(equation) == 1:
        return int(equation[0])

    if len(equation) == 3:
        if equation[1] == "+":
            return int(equation[0]) + int(equation[2])
        elif equation[1] == "*":
            return int(equation[0]) * int(equation[2])
    else:
        if equation[1] == "+":
            return calc_eq([int(equation[0]) + int(equation[2])] + equation[3:])
        elif equation[1] == "*":
            return calc_eq([int(equation[0]) * int(equation[2])] + equation[3:])


def calc_eq2(equation: list[str | int]) -> int:
    if len(equation) % 2 != 1:
        raise NotImplementedError
    if len(equation) == 1:
        return int(equation[0])
    if len(equation) == 3:
        if equation[1] == "+":
            return int(equation[0]) + int(equation[2])
        elif equation[1] == "*":
            return int(equation[0]) * int(equation[2])
    else:
        plus = equation.index("+") if "+" in equation else None
        if plus is None:
            return calc_eq2([int(equation[0]) * int(equation[2])] + equation[3:])
        elif plus == 1:
            return calc_eq2([int(equation[0]) + int(equation[2])] + equation[3:])

        return calc_eq2(
            equation[: plus - 1] + [int(equation[plus - 1]) + int(equation[plus + 1])] + equation[plus + 2 :]
        )


def solve_equation(equation: list[str], resolver: Callable[[list[str | int]], int]) -> int:
    parenth = get_parenth_level(equation)
    if max(parenth) == 0:
        return resolver(equation)
    start_p = parenth.index(max(parenth))
    i = start_p
    while parenth[i] == max(parenth):
        i += 1
    solv = resolver(equation[start_p + 1 : i])
    equation = equation[:start_p] + [solv] + equation[i + 1 :]
    return solve_equation(equation, resolver)


def part_one(data: list[str]) -> Union[str, int]:
    return sum(solve_equation(x.replace("(", "( ").replace(")", " )").split(), calc_eq) for x in data)


def part_two(data: list[str]) -> Union[str, int]:
    return sum(solve_equation(x.replace("(", "( ").replace(")", " )").split(), calc_eq2) for x in data)


def main(test: bool = False):
    test_case_1 = """((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"""

    day = 18
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2020, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"\t\tday {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")

    return perf_counter() - start


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
