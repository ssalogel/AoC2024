from fractions import Fraction
from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from src.utils.Grids import data_to_grid
from math import gcd, atan2, degrees

logger = logging.getLogger("AoC")


def find_all_targets(grid: set[complex], pos: complex) -> set[tuple[int, int]]:
    angles = set()
    others = grid.difference({pos})
    for other in others:
        dx = int(other.real - pos.real)
        dy = int(other.imag - pos.imag)

        if dx == 0:
            angles.add((0, dy // abs(dy)))
            continue
        if dy == 0:
            angles.add((dx // abs(dx), 0))
            continue
        div = gcd(dx, dy)
        angles.add((dx // div, dy // div))
    return angles


def order_next_targets(grid, angles_s: set[tuple[int, int]], start: complex) -> list[complex]:
    angles = list(angles_s)
    angles.sort(key=lambda a: (degrees(atan2(a[0], -a[1]))) % 360)
    t = [(degrees(atan2(a[0], -a[1]))) % 360 for a in angles]
    res = []
    for x, y in angles:
        d = x + 1j * y
        pos = d + start
        while pos not in grid:
            pos += d
        res.append(pos)
    return res


def part_one(data: list[str]) -> Union[str, int]:
    grid: set[complex] = set(data_to_grid(list(reversed(data)), "#"))
    res = {}
    for pos in grid:
        res[pos] = len(find_all_targets(grid, pos))
    return max((v, (int(k.real), int(k.imag))) for k, v in res.items())


def part_two(data: list[str]) -> Union[str, int]:
    grid: set[complex] = set(data_to_grid(list(reversed(data)), "#"))
    pos = best = 0
    for n_pos in grid:
        curr = len(find_all_targets(grid, n_pos))
        if curr > best:
            best = curr
            pos = n_pos
    c = 0
    res = []
    grid.remove(pos)
    while c < 200 and grid:
        for n_pos in order_next_targets(grid, find_all_targets(grid, pos), pos):
            grid.remove(n_pos)
            res.append(n_pos)
            c += 1
            if c == 200:
                break
    two_hundredth = res[-1]
    return int(two_hundredth.real * 100 + two_hundredth.imag)


def main(test: bool = False):
    test_case_1 = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""

    day = 10
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2019, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data)[0]}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"\t\tday {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")

    return perf_counter() - start


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
