from collections import defaultdict
from typing import Union
from time import perf_counter

from src.AoC2019.IntCode import IntCode, State
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def paint_hull(computer: IntCode, robot: complex, direction: complex, hull: dict[complex, int]) -> dict[complex, int]:
    while computer.state != State.DONE:
        computer.add_input(hull[robot])
        computer.run_until_end()
        hull[robot] = computer.output.popleft()
        turn = computer.output.popleft()
        if turn == 1:
            direction *= -1j
        else:
            direction *= 1j
        robot += direction
    return hull


def draw_hull(hull: dict[complex, int]) -> None:
    white = set((int(pos.real), int(pos.imag)) for pos, col in hull.items() if col == 1)
    width = max(a for a, _ in white)
    height = -min(b for _, b in white)
    res = [[] for _ in range(height + 1)]
    for x in range(width + 1):
        for y in range(height + 1):
            if (x, -y) in white:
                res[y].append("█")
            else:
                res[y].append(" ")
    for row in res:
        logger.debug("".join(row))


def part_one(data: list[str]) -> Union[str, int]:
    hull = defaultdict(lambda: 0)
    direction = 1j
    robot = 0
    comp = IntCode([int(x) for x in data[0].split(",")])
    hull = paint_hull(comp, robot, direction, hull)
    return len(hull)


def part_two(data: list[str]) -> Union[str, int]:
    hull = defaultdict(lambda: 0)
    hull[0] = 1
    direction = 1j
    robot = 0
    comp = IntCode([int(x) for x in data[0].split(",")])
    hull = paint_hull(comp, robot, direction, hull)
    draw_hull(hull)
    return len(hull)


def main(test: bool = False):
    test_case_1 = """"""

    day = 11
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
