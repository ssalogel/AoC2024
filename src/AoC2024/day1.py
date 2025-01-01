from time import perf_counter

from src.utils import Day
import logging

logger = logging.getLogger("AoC")
from collections import Counter


def part_one(data):
    l1, l2 = [], []
    for line in data:
        front, back = line.split("   ", 1)
        l1.append(int(front))
        l2.append(int(back))
    l1.sort()
    l2.sort()
    assert len(l1) == len(l2)
    return sum(abs(a - b) for a, b in zip(l1, l2))


def part_two(data):
    l1, l2 = [], []
    for line in data:
        front, back = line.split("   ", 1)
        l1.append(int(front))
        l2.append(int(back))

    right = Counter(l2)
    return sum(right[n] * n for n in l1)


def main():
    test_case_1 = """3   4
    4   3
    2   5
    1   3
    3   9
    3   3"""

    test = False
    day = 1
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
