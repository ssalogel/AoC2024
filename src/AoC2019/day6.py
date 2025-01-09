from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from collections import defaultdict, deque

logger = logging.getLogger("AoC")


def calc_num_orbits(orbits, planet: str = "COM", v: int = 0) -> int:
    if len(orbits[planet]) == 0:
        return v
    return sum(calc_num_orbits(orbits, x, v + 1) for x in orbits[planet]) + v


def part_one(data: list[str]) -> Union[str, int]:
    orbits = defaultdict(list)
    for line in data:
        a, b = line.split(")", 2)
        orbits[a].append(b)

    return calc_num_orbits(orbits)


def part_two(data: list[str]) -> Union[str, int]:
    transfers = defaultdict(list)
    for line in data:
        a, b = line.split(")", 2)
        transfers[a].append(b)
        transfers[b].append(a)

    visited = set()
    to_visit = deque()
    to_visit.append((-1, "YOU"))
    while True:
        cost, pos = to_visit.popleft()
        visited.add(pos)
        for npos in transfers[pos]:
            if npos == "SAN":
                return cost
            if npos not in visited:
                to_visit.append((cost + 1, npos))


def main(test: bool = False):
    test_case_1 = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN"""

    day = 6
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
