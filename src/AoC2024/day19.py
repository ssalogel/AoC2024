from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")
from functools import lru_cache


@lru_cache()
def make_design(design: str, towels: frozenset[str]) -> int:
    if design == "":
        return True
    for towel in towels:
        if design.startswith(towel):
            if make_design(design.removeprefix(towel), towels):
                return True
    return False


@lru_cache()
def count_design(design: str, towels: frozenset[str]) -> int:
    if design == "":
        return 1
    nb = 0
    for towel in towels:
        if design.startswith(towel):
            nb += count_design(design.removeprefix(towel), towels)
    return nb


def part_one(data: list[str]) -> Union[str, int]:
    towels, designs = data
    towels = frozenset(towels.split(", "))
    designs = designs.splitlines()

    return sum(make_design(x, towels) for x in designs)


def part_two(data: list[str]) -> Union[str, int]:
    towels, designs = data
    towels = frozenset(towels.split(", "))
    designs = designs.splitlines()

    return sum(count_design(x, towels) for x in designs)


def main(test: bool = False):
    test_case_1 = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

    day = 19
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n\n")
    else:
        data = Day.get_data(2024, day).strip().split("\n\n")

    start = perf_counter()
    logger.info(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.info(f"the whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main(True)
