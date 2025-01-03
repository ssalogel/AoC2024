from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from math import lcm

logger = logging.getLogger("AoC")


def part_one(data: list[str]) -> Union[str, int]:
    start = int(data[0])
    times = [int(x) for x in data[1].split(",") if x != "x"]
    wait = [x - (start % x) for x in times]
    best = min(wait)
    return best * times[wait.index(best)]


def part_two(data: list[str]) -> Union[str, int]:
    buses = [(int(x), ix) for ix, x in enumerate(data[1].split(",")) if x != "x"]
    time = buses[0][0]
    for ix, (bus, delay) in enumerate(buses[1:]):
        jmp = lcm(*[t for t, d in buses[: ix + 1]])
        while time % bus != (bus - delay) % bus:
            time += jmp
    return time


def main(test: bool = False):
    test_case_1 = """939
1789,37,47,1889"""

    day = 13
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
