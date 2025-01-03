from typing import Union
from time import perf_counter
from src.utils import Day
from itertools import combinations
import sys
import logging
from math import prod

logger = logging.getLogger("AoC")


def part_one(data: list[str]) -> Union[str, int]:
    expense_report = [int(x) for x in data]
    expense_report.sort()
    head = 0
    tail = -1
    while expense_report[head] + expense_report[tail] != 2020:
        if expense_report[head] + expense_report[tail] < 2020:
            head += 1
        else:
            tail -= 1
        if len(expense_report) + tail < head:
            logging.error("this fucked")
            break
    return expense_report[head] * expense_report[tail]


def part_two(data: list[str]) -> Union[str, int]:
    expense_report = [int(x) for x in data]
    for c in combinations(expense_report, 3):
        if sum(c) == 2020:
            return prod(c)


def main(test: bool = False):
    test_case_1 = """1721
979
366
299
675
1456"""

    day = 1
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
    main(True)
