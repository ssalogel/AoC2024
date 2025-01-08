from collections import defaultdict
from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def part_one(data: list[str], end: int) -> Union[str, int]:
    starting_numbers = [int(x) for x in data[0].split(",")]
    res = [-1] * end  # about twice as fast as using a defaultdict(lambda: -1)
    for ix, n in enumerate(starting_numbers[:-1]):
        res[n] = ix
    n = starting_numbers[-1]
    for ix in range(len(starting_numbers) - 1, end - 1):
        t = res[n]
        res[n] = ix
        n = ix - t if t != -1 else 0
    return n


def main(test: bool = False):
    test_case_1 = """0,3,6"""

    day = 15
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2020, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data, 2020)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"\t\tday {day} part 2: {part_one(data, 30000000)} in {perf_counter() - mid:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")

    return perf_counter() - start


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
