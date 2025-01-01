from time import perf_counter
from typing import Union

from src.utils import Day
import logging

logger = logging.getLogger("AoC")


def all_same_sign(change: list[int]) -> bool:
    return all(map(lambda x: x >= 0, change)) or all(map(lambda x: x <= 0, change))


def all_within_bounds(change: list[int], minbound: int, maxbound: int) -> bool:
    return all(map(lambda x: maxbound >= x >= minbound, map(abs, change)))


def try_removing_any(level: list[int]) -> bool:
    for i in range(len(level)):
        if i == 0:
            attempt = level[1:]
        elif i == len(level):
            attempt = level
        else:
            attempt = level[:i] + level[i + 1 :]
        change = [level - attempt[i + 1] for i, level in enumerate(attempt[:-1])]
        valid = all_within_bounds(change, 1, 3) and all_same_sign(change)
        if valid:
            return True
    return False


def part_one(data: list[str]) -> Union[str, int]:
    safe = 0
    for report in data:
        levels = list(map(int, report.split()))
        changes = [level - levels[i + 1] for i, level in enumerate(levels[:-1])]
        safe += all_within_bounds(changes, 1, 3) and all_same_sign(changes)
    return safe


def part_two(data: list[str]) -> Union[str, int]:

    safe = 0
    for report in data:
        levels = list(map(int, report.split()))
        safe += try_removing_any(levels)
    return safe


def main():
    test_case_1 = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

    test = False
    day = 2
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
    logging.basicConfig(level=logging.NOTSET)
    main()
