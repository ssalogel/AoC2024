from time import perf_counter
from typing import Union
import re
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def part_one(data: str) -> Union[str, int]:
    mul_finder = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    total = 0
    muls = re.findall(mul_finder, data)
    total += sum([int(a) * int(b) for a, b in muls])
    return total


def part_two(data: str) -> Union[str, int]:
    mul_finder = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    total = 0
    stop_go = re.compile(r"don't\(\).*?do\(\)")
    only_go = re.sub(stop_go, "----", data)
    muls = re.findall(mul_finder, only_go)
    total += sum([int(a) * int(b) for a, b in muls])
    return total


def main(test: bool = False):
    test_case_1 = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
    test_case_2 = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?don't()do()mul(8,5))"""

    day = 3
    if test:
        data = test_case_1.strip().split("\n")
        data = test_case_2.strip().split("\n")
    else:
        data = Day.get_data(2024, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data[0])}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"\t\tday {day} part 2: {part_two(data[0])} in {perf_counter() - mid:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")

    return perf_counter() - start


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main(True)
