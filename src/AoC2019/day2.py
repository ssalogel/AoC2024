from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from IntCode import IntCode

logger = logging.getLogger("AoC")


def part_one(data: list[str]) -> Union[str, int]:
    code = list(map(int, data[0].split(",")))
    code[1] = 12
    code[2] = 2
    comp = IntCode(code)
    comp.run_until_end()
    return comp.code[0]


def part_two(data: list[str]) -> Union[str, int]:
    code = list(map(int, data[0].split(",")))
    comp = IntCode(code)
    for a in range(100):
        for b in range(100):
            comp.code[1] = a
            comp.code[2] = b
            comp.run_until_end()
            if comp.code[0] == 19690720:
                return 100 * a + b
            comp.reset()

def main(test: bool = False):
    test_case_1 = """1,9,10,3,2,3,11,0,99,30,40,50"""

    day = 2
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
