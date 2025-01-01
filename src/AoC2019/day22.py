from typing import Union
from time import perf_counter
from src.utils import Day
import logging

logger = logging.getLogger("AoC")


def part_one(data: list[str]) -> Union[str, int]:
    return data


def part_two(data: list[str]) -> Union[str, int]:
    pass


def main():
    test_case_1 = """"""

    test = True
    day = 22
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2019, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.info(f"the whole day {day} took {perf_counter() - start:.4f}s")

if __name__ == '__main__': 
    main()
