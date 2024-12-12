from typing import Union, Callable
from math import log10, floor
from utils import Day


def split(number, target) -> tuple[bool, int]:
    length = floor(log10(target)) + 1
    divider, mod = divmod(number, pow(10, length))
    return mod == target, divider

def div(number, target) -> tuple[bool, int]:
    return number % target == 0, number//target

def sub(number, target) -> tuple[bool, int]:
    return number >= target, number - target

def test_calibration(target: int, steps: list[int], operators: list[Callable[[int, int], tuple[bool, int]]]) -> bool:
    if len(steps) == 1:
        return steps[0] == target
    valid = False
    for op in operators:
        success, new_target = op(target, steps[-1])
        if success:
            valid |= test_calibration(new_target, steps[:-1], operators)
        if valid:
            break
    return valid

def part_one(data: list[str]) -> Union[str, int]:
    total = 0
    for line in data:
        goal, steps = line.split(': ')
        goal = int(goal)
        steps = [int(x) for x in steps.split()]
        total += goal * test_calibration(goal, steps, [div, sub])
    return total

def part_two(data: list[str]) -> Union[str, int]:
    total = 0
    for line in data:
        goal, steps = line.split(': ')
        goal = int(goal)
        steps = [int(x) for x in steps.split()]
        total += goal * test_calibration(goal, steps, [div, sub, split])
    return total


def main():
    test_case_1 = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""

    test = False
    day = 7
    if test:
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(day).strip().split("\n")


    print(f"day {day} part 1: {part_one(data)}")
    print(f"day {day} part 2: {part_two(data)}")


main()