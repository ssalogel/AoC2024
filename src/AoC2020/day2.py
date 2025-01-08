from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from collections import Counter

logger = logging.getLogger("AoC")


def part_one(data: list[str]) -> Union[str, int]:
    tot = 0
    for line in data:
        rule, password = line.split(": ", 1)
        minshow, maxshow, letter = (
            int(rule[: rule.index("-")]),
            int(rule[rule.index("-") + 1 : rule.index(" ")]),
            rule[-1],
        )
        c = Counter(password)
        tot += minshow <= c[letter] <= maxshow
    return tot


def part_two(data: list[str]) -> Union[str, int]:
    tot = 0
    for line in data:
        rule, password = line.split(": ", 1)
        pos1, pos2, letter = int(rule[: rule.index("-")]), int(rule[rule.index("-") + 1 : rule.index(" ")]), rule[-1]
        tot += (password[pos1 - 1] == letter) ^ (password[pos2 - 1] == letter)
    return tot


def main(test: bool = False):
    test_case_1 = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""

    day = 2
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
    main(True)
