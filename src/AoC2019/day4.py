from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def part_one(data: list[str]) -> Union[str, int]:
    a, b = data[0].split("-")
    a = int(a)
    b = int(b) + 1
    c = 0
    for num in range(a, b):
        d_6, d_5, d_4, d_3, d_2, d_1 = (
            num // 100_000,
            num // 10_000 % 10,
            num // 1_000 % 10,
            num // 100 % 10,
            num // 10 % 10,
            num % 10,
        )
        if d_6 <= d_5 <= d_4 <= d_3 <= d_2 <= d_1:
            if d_6 == d_5 or d_5 == d_4 or d_4 == d_3 or d_3 == d_2 or d_2 == d_1:
                c += 1
    return c


def part_two(data: list[str]) -> Union[str, int]:
    a, b = data[0].split("-")
    a = int(a)
    b = int(b) + 1
    c = 0
    for num in range(a, b):
        d_6, d_5, d_4, d_3, d_2, d_1 = (
            num // 100_000,
            num // 10_000 % 10,
            num // 1_000 % 10,
            num // 100 % 10,
            num // 10 % 10,
            num % 10,
        )
        if d_6 <= d_5 <= d_4 <= d_3 <= d_2 <= d_1:
            if (
                d_6 == d_5 != d_4
                or d_6 != d_5 == d_4 != d_3
                or d_5 != d_4 == d_3 != d_2
                or d_4 != d_3 == d_2 != d_1
                or d_3 != d_2 == d_1
            ):
                c += 1
    return c


def main(test: bool = False):
    test_case_1 = """"""

    day = 4
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2019, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"\t\tday {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")

    return perf_counter() - start


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
