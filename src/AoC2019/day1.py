from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def part_one(data: list[str]) -> Union[str, int]:
    return sum([int(x) // 3 - 2 for x in data])


def get_fuel_req(mass: int) -> int:
    fuel = max(0, mass // 3 - 2)
    if fuel:
        return get_fuel_req(fuel) + fuel
    return fuel


def part_two(data: list[str]) -> Union[str, int]:
    return sum([get_fuel_req(int(x)) for x in data])


def main(test: bool = False):
    test_case_1 = """12
14
1969
100756"""

    day = 1
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
