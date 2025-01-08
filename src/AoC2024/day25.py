from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def part_one(data: list[str]) -> Union[str, int]:
    keys = []
    locks = []
    for elem in data:
        rows = elem.replace(".", "0").replace("#", "1").split()
        if rows[0] == "00000":
            keys.append([int(x, 2) for x in rows[1:-1]])
        else:
            locks.append([int(x, 2) for x in rows[1:-1]])
    tot = 0
    for lock in locks:
        for key in keys:
            valid = True
            for a, b in zip(lock, key):
                valid &= not a & b
            tot += valid

    return tot


def main(test: bool = False):
    test_case_1 = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

    day = 25
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n\n")
    else:
        data = Day.get_data(2024, day).strip().split("\n\n")

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")

    return perf_counter() - start


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main(True)
