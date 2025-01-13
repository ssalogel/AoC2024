from itertools import cycle
from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def phase(signal: list[int], pattern: list[int]) -> list[int]:
    res = []
    for i, elem in enumerate(signal):
        n_pattern = []
        for c in pattern:
            for _ in range(i + 1):
                n_pattern.append(c)
        n_pattern = n_pattern[1:] + [n_pattern[0]]
        mid = [a * b for a, b in zip(signal, cycle(n_pattern))]
        res.append(abs(sum(mid)) % 10)
    return res


def part_one(data: list[str]) -> Union[str, int]:
    signal = [int(c) for c in data[0]]
    pattern = [0, 1, 0, -1]
    for _ in range(100):
        signal = phase(signal, pattern)
    return "".join(str(x) for x in signal[:8])


def part_two(data: list[str]) -> Union[str, int]:
    signal = [int(c) for c in data[0]]
    to_skip = int("".join(data[0][:7]))
    full_length = len(signal) * 10_000
    signal = (signal * 10_000)[to_skip:]
    pattern = [0, 1, 0, -1]
    # if to_skip > full_length /2, the '1' bit of the pattern is the only one we need
    assert to_skip > full_length // 2
    for _ in range(100):
        cummulative_sum = 0
        for i in range(len(signal) - 1, -1, -1):
            cummulative_sum += signal[i]
            signal[i] = cummulative_sum % 10

    return "".join(str(x) for x in signal[:8])


def main(test: bool = False):
    test_case_1 = """69317163492948606335995924319873"""

    day = 16
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
