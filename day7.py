from typing import Union
from operator import add, mul
from functools import reduce
from itertools import product
from utils import Day

def conc(x, y):
    return int(str(x) + str(y))

def part_one(data: list[str]) -> Union[str, int]:
    total = 0
    for line in data:
        goal, steps = line.split(': ')
        goal = int(goal)
        steps = [int(x) for x in steps.split()]
        for operators in product([add, mul], repeat=len(steps)-1):
            op = iter(operators)
            calc = reduce(lambda x, y: next(op)(x, y), steps)
            if calc == goal:
                total += goal
                break
    return total

def part_two(data: list[str]) -> Union[str, int]:
    total = 0
    for line in data:
        goal, steps = line.split(': ')
        goal = int(goal)
        steps = [int(x) for x in steps.split()]
        for operators in product([add, mul, conc], repeat=len(steps) - 1):
            op = iter(operators)
            calc = reduce(lambda x, y: next(op)(x, y), steps)
            if calc == goal:
                total += goal
                break
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