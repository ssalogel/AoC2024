from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from math import prod

logger = logging.getLogger("AoC")

def print_cups(cups: list[int], curr, limit: int = 9) -> list[int]:
    res = []
    for _ in range(min(len(cups) - 1, limit)):
        res.append(cups[curr])
        curr = cups[curr]
    return res


def cycle(num: int, cups: list[int], start: int) -> list[int]:
    curr = start
    for _ in range(num):
        a = cups[curr]
        b = cups[a]
        c = cups[b]
        end = cups[c]
        prev = curr - 1
        if prev == 0:
            prev = len(cups) - 1
        while prev in (a, b, c):
            prev -= 1
            if prev == 0:
                prev = len(cups) - 1
        cups[curr] = end
        cups[c] = cups[prev]
        cups[prev] = a
        curr = cups[curr]
    return cups

def part_one(data: list[str]) -> Union[str, int]:
    values = [int(x) for x in data[0]]
    cups = [0] * (len(values) + 1)
    for prev, curr in zip(values, values[1:]):
        cups[prev] = curr
    cups[values[-1]] = values[0]
    return "".join(str(x) for x in print_cups(cycle(100, cups, values[0]), 1, 8))



def part_two(data: list[str]) -> Union[str, int]:
    values = [int(x) for x in data[0]]
    cups = [0] * (len(values) + 1)
    for prev, curr in zip(values, values[1:]):
        cups[prev] = curr
    cups[values[-1]] = len(values) + 1
    cups += list(range(len(values) + 2, 1_000_000 + 2))
    cups[-1] = values[0]
    c = cycle(10_000_000, cups, values[0])
    return prod(print_cups(cups, 1, 2))



def main(test: bool = False):
    test_case_1 = """389125467"""

    day = 23
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2020, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.info(f"the whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
