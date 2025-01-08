from collections import deque
from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def part_one(data: list[str], window) -> Union[str, int]:
    preamble = deque()
    for x in range(window):
        preamble.append(int(data[x]))

    for x in data[window:]:
        x = int(x)
        for n in preamble:
            v = x - n
            if v in preamble and (v != n or preamble.count(n) > 1):
                break
        else:
            return x
        preamble.popleft()
        preamble.append(x)


def part_two(data: list[str], window) -> Union[str, int]:
    target = part_one(data, window)
    numbers = [int(x) for x in data]
    head = 0
    tail = 2
    s = sum(numbers[head:tail])
    while s != target:
        if s < target:
            tail += 1
        else:
            head += 1
        s = sum(numbers[head:tail])
    return max(numbers[head:tail]) + min(numbers[head:tail])


def main(test: bool = False):
    test_case_1 = """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576"""

    day = 9
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
        window = 5
    else:
        data = Day.get_data(2020, day).strip().split("\n")
        window = 25

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data, window)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"\t\tday {day} part 2: {part_two(data, window)} in {perf_counter() - mid:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")

    return perf_counter() - start


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
