from math import inf
from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from src.utils.Grids import get_all_costs

logger = logging.getLogger("AoC")


def part_one(data: list[str], width, length, safe) -> Union[str, int]:
    target = (width - 1) + (length - 1) * 1j
    grid = {x + y * 1j: "." for x in range(width) for y in range(length)}
    for i, pos in enumerate(int(b[: b.index(",")]) + int(b[b.index(",") + 1 :]) * 1j for b in data):
        if i >= safe:
            break
        grid[pos] = "#"

    return get_all_costs(grid, ["."])[target]


def part_two(data: list[str], width, length, safe) -> Union[str, int]:
    target = (width - 1) + (length - 1) * 1j
    grid = {x + y * 1j: "." for x in range(width) for y in range(length)}
    blocks = [int(b[: b.index(",")]) + int(b[b.index(",") + 1 :]) * 1j for b in data]
    for i, pos in enumerate(blocks):
        if i >= safe:
            break
        grid[pos] = "#"

    # binary search position that blocks
    last_working, first_blocking = safe - 1, len(data) - 1
    while last_working + 1 < first_blocking:
        test_stop = (last_working + first_blocking) // 2
        test_grid = grid.copy()
        for pos in blocks[last_working : test_stop + 1]:
            test_grid[pos] = "#"
        costs = get_all_costs(test_grid, ["."])
        if costs[target] != inf:
            last_working = test_stop
            grid = test_grid
        else:
            first_blocking = test_stop
    blocker = blocks[first_blocking]
    return f"{int(blocker.real)},{int(blocker.imag)}"


def main(test: bool = False):
    test_case_1 = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

    day = 18
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
        width = length = 7
        safe = 12
    else:
        data = Day.get_data(2024, day).strip().split("\n")
        width = length = 71
        safe = 1024

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data, width, length, safe)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"\t\tday {day} part 2: {part_two(data, width, length, safe)} in {perf_counter() - mid:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")

    return perf_counter() - start


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
