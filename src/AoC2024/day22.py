from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")
from collections import deque, Counter


def derive(secret: int) -> int:
    secret ^= secret << 6
    secret = secret % 16777216
    secret ^= secret >> 5
    secret = secret % 16777216
    secret ^= secret << 11
    secret = secret % 16777216
    return secret


def part_one(data: list[str]) -> Union[str, int]:
    res = 0
    for d in data:
        d = int(d)
        for _ in range(2000):
            d = derive(d)
        res += d
    return res


def generate_patterns_sellability(secret: int) -> dict[tuple[int, int, int, int], int]:
    sequence = deque()
    results = {}
    prev = secret % 10
    for _ in range(2000):
        secret = derive(secret)
        curr = secret % 10
        diff = curr - prev
        sequence.append(diff)
        if len(sequence) > 4:
            sequence.popleft()
        if len(sequence) == 4:
            key = tuple(sequence)
            if key not in results:
                results[key] = curr
        prev = curr
    return results


def part_two(data: list[str]) -> Union[str, int]:
    c = Counter()
    for d in data:
        prices = generate_patterns_sellability(int(d))
        c.update(prices)

    return c.most_common(1).pop()[1]


def main(test: bool = False):
    test_case_1 = """1
3
2
AoC2024"""

    day = 22
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2024, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"\t\tday {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")

    return perf_counter() - start


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main(True)
