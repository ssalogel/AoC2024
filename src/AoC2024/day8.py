from time import perf_counter
from typing import Union
from itertools import combinations
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def to_grid(data: list[str]) -> dict[str, list[complex]]:
    d = {}
    for char, pos in [(c, x + 1j * y) for y, line in enumerate(reversed(data)) for x, c in enumerate(line)]:
        if char == ".":
            continue
        if char in d:
            d[char].append(pos)
        else:
            d[char] = [pos]
    return d


def part_one(data: list[str]) -> Union[str, int]:
    width = len(data)
    heigth = len(data[0])
    antinodes = set()
    for char, positions in to_grid(data).items():
        for pair in combinations(positions, 2):
            el1, el2 = pair
            dist = el1 - el2
            n1 = el1 + dist
            if 0 <= n1.real < width and 0 <= n1.imag < heigth:
                antinodes.add(n1)
            n2 = el2 - dist
            if 0 <= n2.real < width and 0 <= n2.imag < heigth:
                antinodes.add(n2)
    return len(antinodes)


def part_two(data: list[str]) -> Union[str, int]:
    width = len(data)
    heigth = len(data[0])
    antinodes = set()
    for char, positions in to_grid(data).items():
        for pair in combinations(positions, 2):
            el1, el2 = pair
            antinodes.add(el1)
            antinodes.add(el2)
            dist = el1 - el2
            nf = el1 + dist
            while 0 <= nf.real < width and 0 <= nf.imag < heigth:
                antinodes.add(nf)
                nf = nf + dist
            nb = el2 - dist
            while 0 <= nb.real < width and 0 <= nb.imag < heigth:
                antinodes.add(nb)
                nb = nb - dist
    return len(antinodes)


def main():
    test_case_1 = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

    test = False
    day = 8
    if test:
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2024, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.info(f"the whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
