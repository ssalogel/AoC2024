from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from itertools import product

logger = logging.getLogger("AoC")


type Position = tuple[int,int,int] | tuple[int, int, int, int]

def get_neighs(pos: Position) -> list[Position]:
    ranges = ((c-1, c, c+1) for c in pos)
    yield from product(*ranges)


def alive_nei(cube: set[Position], pos: Position) -> int:
    nei_sum = sum(p in cube for p in get_neighs(pos))
    nei_sum -= pos in cube
    return nei_sum

def all_nei(cube: set[Position]) -> set[Position]:
    return set(x for p in cube for x in get_neighs(p))

def cycle(cube: set[Position]) -> set[Position]:
    new_cube = set()
    for p in all_nei(cube):
        nb_alive_nei = alive_nei(cube, p)
        if nb_alive_nei == 3 or (nb_alive_nei == 2 and p in cube):
            new_cube.add(p)
    return new_cube

def part_one(data: list[str], cycles: int) -> Union[str, int]:
    cube = set()
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell == "#":
                cube.add((x,y,0))
    for _ in range(cycles):
        cube = cycle(cube)
    return len(cube)


def part_two(data: list[str], cycles = 6) -> Union[str, int]:
    cube = set()
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell == "#":
                cube.add((x,y,0,0))

    for _ in range(cycles):
        cube = cycle(cube)
    return len(cube)


def main(test: bool = False):
    test_case_1 = """.#.
..#
###"""

    day = 17
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2020, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"day {day} part 1: {part_one(data, 6)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.info(f"the whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
