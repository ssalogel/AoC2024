from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from math import prod

logger = logging.getLogger("AoC")


def count_tree_in_path(pattern: list[str], delta_x: int, delta_y: int) -> int:
    res = 0
    x = 0
    y = 0
    while y < len(pattern):
        res += pattern[y][x] == "#"
        x = (x + delta_x) % len(pattern[0])
        y += delta_y
    return res

def part_one(data: list[str]) -> Union[str, int]:
    return count_tree_in_path(data, 3, 1)


def part_two(data: list[str]) -> Union[str, int]:
    return prod((count_tree_in_path(data, 1, 1),
                 count_tree_in_path(data, 3, 1),
                 count_tree_in_path(data, 5, 1),
                 count_tree_in_path(data, 7, 1),
                 count_tree_in_path(data, 1, 2),
                 ))


def main(test: bool = False):
    test_case_1 = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

    
    day = 3
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
    main(True)
