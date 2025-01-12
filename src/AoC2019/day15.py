from heapq import heappop, heappush
from math import inf
from typing import Union
from time import perf_counter

from src.utils.IntCode import IntCode
from src.utils import Day
import sys
import logging

from src.utils.Grids import get_all_costs

logger = logging.getLogger("AoC")


def explore_halls(computer) -> dict[complex, int]:
    robot = 0
    grid = {0: 1}
    moves = [(1, True), (2, True), (3, True), (4, True)]
    move_comp = {1: 1j, 2: -1j, 3: -1, 4: 1}
    opp = {1: 2, 2: 1, 3: 4, 4: 3}
    while moves:
        move, explore = moves.pop()
        n_pos = robot + move_comp[move]
        computer.add_input(move)
        computer.run_until_end()
        res = computer.output.popleft()
        if not explore:
            robot = n_pos
            continue
        grid[n_pos] = res
        if res == 0:
            continue
        robot = n_pos
        moves.append((opp[move], False))
        for m in range(1, 5):
            if m == opp[move]:
                continue
            moves.append((m, True))
    return grid


def part_one(data: list[str]) -> Union[str, int]:
    computer = IntCode([int(x) for x in data[0].split(",")])
    grid = explore_halls(computer)
    start = 0
    target = [p for p, v in grid.items() if v == 2]
    assert len(target) == 1
    target = target.pop()
    costs = get_all_costs(grid, [1, 2])
    return costs[target]


def part_two(data: list[str]) -> Union[str, int]:
    computer = IntCode([int(x) for x in data[0].split(",")])
    grid = explore_halls(computer)
    start = 0
    source = [p for p, v in grid.items() if v == 2]
    assert len(source) == 1
    source = source.pop()
    costs = get_all_costs(grid, [1, 2], start=source)
    return max(*costs.values())


def main(test: bool = False):
    test_case_1 = """"""

    day = 15
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
