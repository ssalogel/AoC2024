from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from src.utils.Grids import data_to_grid, get_neighbors4
from collections import Counter, defaultdict
from itertools import combinations
from math import isnan

logger = logging.getLogger("AoC")


def bfs(grid: dict[complex, str], start: complex) -> dict[complex, int | float]:
    visited = set()
    to_visit = [(start, 0)]
    costs: dict[complex, int | float] = defaultdict(lambda: float("inf"))
    while to_visit:
        pos, cost = to_visit.pop(0)
        costs[pos] = cost
        visited.add(pos)
        for npos in get_neighbors4(pos):
            if npos not in visited and grid[npos] != "#":
                to_visit.append((npos, cost + 1))
    return costs


def part_one(data: list[str]) -> Union[str, int]:
    grid = data_to_grid(data)
    start = 0
    for pos, char in grid.items():
        if char == "S":
            start = pos
            break
    costs = bfs(grid, start)
    cheats = []
    for pos, char in grid.items():
        if char == "#":
            for a, b in combinations([1, 1j, -1, -1j], 2):
                pos_a = pos + a
                pos_b = pos + b
                cheat = abs(costs[pos_a] - costs[pos_b]) - 2
                if cheat != float("inf") and not isnan(cheat):
                    cheats.append(cheat)
    return sum(map(lambda x: x >= 100, cheats))


def part_two(data: list[str]) -> Union[str, int]:
    grid = data_to_grid(data)
    start = 0
    for pos, char in grid.items():
        if char == "S":
            start = pos
            break
    costs = bfs(grid, start)
    cheats = []
    for pos, char in grid.items():
        if grid[pos] == "#":
            continue

        for d_x in range(-20, 21):
            vertical_range = 20 - abs(d_x)
            for d_y in range(-vertical_range, vertical_range + 1):
                n_pos = pos + d_x + d_y * 1j
                if costs[n_pos] == float("inf"):
                    continue
                cheat = costs[n_pos] - costs[pos] - abs(d_x) - abs(d_y)
                if cheat > 0:
                    cheats.append(cheat)
    return sum(map(lambda x: x >= 100, cheats))


def main(test: bool = False):
    test_case_1 = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""

    day = 20
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2024, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"\t\tday {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
