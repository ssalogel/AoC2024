from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from src.utils.Grids import data_to_grid, get_neighbors8


logger = logging.getLogger("AoC")


def draw_grid(grid: dict[complex, bool], width: int, height: int) -> None:
    for j in range(height):
        for i in range(width):
            pos = i + j * 1j
            if pos not in grid:
                print(" ", end="")
            elif grid[pos]:
                print("▓", end="")
            else:
                print("_", end="")
        print()
    print("".join(["*"] * width))


def first_neighs_status(grid: dict[complex, bool], pos: complex, width: int, heigth: int) -> list[bool]:
    directions = [-1j, 1 - 1j, 1, 1 + 1j, 1j, -1 + 1j, -1, -1 - 1j]
    for direction in directions:
        curr = pos + direction
        while curr not in grid and 0 <= curr.real < width and 0 <= curr.imag < heigth:
            curr += direction
        if curr in grid:
            yield grid[curr]


def part_one(data: list[str]) -> Union[str, int]:
    grid: dict[complex, str] = data_to_grid(data, char_to_keep="L", true_value="")
    while True:
        newgrid = {}
        for pos, occupied in grid.items():
            neigh = get_neighbors8(pos)
            neigh_status = [grid[x] for x in neigh if x in grid]
            if occupied:
                occupied = sum(neigh_status) < 4
            else:
                occupied = not any(neigh_status)
            newgrid[pos] = occupied
        # draw_grid(newgrid, len(data[0]), len(data))
        if grid == newgrid:
            break
        grid = newgrid

    return sum(grid.values())


def part_two(data: list[str]) -> Union[str, int]:
    grid = data_to_grid(data, char_to_keep="L", true_value="")
    width = len(data[0])
    height = len(data)
    while True:
        newgrid = {}
        for pos, occupied in grid.items():
            neigh_status = list(first_neighs_status(grid, pos, width, height))
            if occupied:
                occupied = sum(neigh_status) < 5
            else:
                occupied = not any(neigh_status)
            newgrid[pos] = occupied
        # draw_grid(newgrid, width, height)
        if grid == newgrid:
            break
        grid = newgrid

    return sum(grid.values())


def main(test: bool = False):
    test_case_1 = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL
"""

    day = 11
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2020, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"\t\tday {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")

    return perf_counter() - start


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
