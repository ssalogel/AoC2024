from collections import defaultdict
from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from operator import add

logger = logging.getLogger("AoC")


def get_neighs(pos: tuple[int,], dim: int = 3) -> list[tuple[int, int, int]]:
    moves = [(-1,), (0,), (1,)]
    curr_dim = 1
    while curr_dim < dim:
        move_up = []
        for move in moves:
            for dimension in (-1, 0, 1):
                move_up.append(move + (dimension,))
        moves = move_up
        curr_dim += 1

    moves.remove(tuple(0 for _ in range(dim)))
    res = []
    for move in moves:
        res.append(tuple(a + b for a,b in zip(move, pos)))
    return res


def part_one(data: list[str], cycles: int) -> Union[str, int]:
    grid = {}

    for z in range(cycles * 2 + 1):
        for y in range(len(data) +  cycles * 2):
            for x in range(len(data[0]) + cycles * 2):
                grid[(x, y, z)] = False


    for y, row in enumerate(data):
        for x, p in enumerate(row):
            if p == "#":
                grid[(cycles + x, cycles + y, cycles)] = True

    for cycle in range(cycles):
        new_grid = {}
        for k,v in grid.items():
            nei = list(get_neighs(k))
            nei_sum = sum(grid[pos] for pos in nei if pos in grid)
            if v and nei_sum in (2, 3):
                new_grid[k] = True
            elif not v and nei_sum == 3:
                new_grid[k] = True
            else:
                new_grid[k] = False
        grid = new_grid
    return sum(v for v in grid.values())


def part_two(data: list[str], cycles = 6) -> Union[str, int]:
    grid = {}

    for z in range(cycles * 2 + 1):
        for y in range(len(data) + cycles * 2):
            for x in range(len(data[0]) + cycles * 2):
                for w in range(cycles * 2 + 1):
                    grid[(x, y, z, w)] = False

    for y, row in enumerate(data):
        for x, p in enumerate(row):
            if p == "#":
                grid[(cycles + x, cycles + y, cycles, cycles)] = True

    for cycle in range(cycles):
        new_grid = {}
        for k, v in grid.items():
            nei = list(get_neighs(k, 4))
            nei_sum = sum(grid[pos] for pos in nei if pos in grid)
            if v and nei_sum in (2, 3):
                new_grid[k] = True
            elif not v and nei_sum == 3:
                new_grid[k] = True
            else:
                new_grid[k] = False
        grid = new_grid
    return sum(v for v in grid.values())


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
