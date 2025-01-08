from typing import Union
from src.utils import Day
import sys
import logging
from src.utils.Grids import data_to_grid
from time import perf_counter


logger = logging.getLogger("AoC")


def get_visited(grid: dict[complex, str], guard: complex) -> set[complex]:
    visited = set()
    move = 1j
    while grid[guard] != "_":
        visited.add(guard)
        while grid[guard + move] == "#":
            move *= -1j
        guard += move
    return visited


def part_one(data: list[str]) -> Union[str, int]:
    grid = data_to_grid(data, default_value="_")
    for pos, value in grid.items():
        if "^" == value:
            guard = pos
            break
    return len(get_visited(grid, guard))


def part_two(data: list[str]) -> Union[str, int]:
    grid = data_to_grid(data, default_value="_")
    total = 0
    for pos, value in grid.items():
        if "^" == value:
            guard = pos
            break

    for pos in get_visited(grid, guard):
        if grid[pos] in ["^", "#"]:
            continue
        grid[pos] = "#"
        move = 1j
        n_guard = guard
        visited = set()

        while grid[guard] != "_":
            if (n_guard, move) in visited:
                total += 1
                break
            visited.add((n_guard, move))
            while grid[n_guard + move] == "#":
                move *= -1j
            n_guard += move

        grid[pos] = "."
    return total


def main(test: bool = False):

    test_case_1 = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

    day = 6
    if test:
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
