from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from collections import Counter

logger = logging.getLogger("AoC")


def part_one(data: list[str]) -> Union[str, int]:
    tot = 0
    for group in data:
        tot += len(set(group.replace("\n", "")))
    return tot


def part_two(data: list[str]) -> Union[str, int]:
    tot = 0
    for group in data:
        c = Counter(group)
        min_value = c["\n"] + 1
        tot += len([x for _, x in c.most_common() if x >= min_value])
    return tot


def main(test: bool = False):
    test_case_1 = """abc

a
b
c

ab
ac

a
a
a
a

b"""

    day = 6
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n\n")
    else:
        data = Day.get_data(2020, day).strip().split("\n\n")

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"\t\tday {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")

    return perf_counter() - start


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
