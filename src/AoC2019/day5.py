from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from IntCode import IntCode, State

logger = logging.getLogger("AoC")


def part_one(data: list[str]) -> Union[str, int]:
    code = list(map(int, data[0].split(",")))
    comp = IntCode(code)
    comp.add_input(1)
    while True:
        comp.resume()
        if comp.state != State.WAIT_OUTPUT:
            break
    return comp.output.pop()


def part_two(data: list[str]) -> Union[str, int]:
    code = list(map(int, data[0].split(",")))
    comp = IntCode(code)
    comp.add_input(5)
    while True:
        comp.resume()
        if comp.state != State.WAIT_OUTPUT:
            break
    return comp.output.pop()


def main(test: bool = False):
    test_case_1 = """3,9,8,9,10,9,4,9,99,-1,8"""

    day = 5
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
