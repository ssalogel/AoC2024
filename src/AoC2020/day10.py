from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from math import prod

logger = logging.getLogger("AoC")


def part_one(data: list[str]) -> Union[str, int]:
    adapters = [int(x) for x in data]
    adapters.sort()
    adapters.insert(0, 0)
    adapters.append(adapters[-1] + 3)
    changes = [b - a for a, b in zip(adapters, adapters[1:])]

    return changes.count(1) * changes.count(3)


def variate_list(numbers: list[int]) -> list[int]:
    changes = [b - a for a, b in zip(numbers, numbers[1:])]
    splits = [i for i, x in enumerate(changes) if x == 3]
    splited_on_3 = []
    prev = 0
    for ix in splits:
        splited_on_3.append(numbers[prev : ix + 1])
        prev = ix + 1
    # input max splited is of length 5, so 3 removables
    variations = []
    for splited in splited_on_3:
        if len(splited) < 3:
            continue
        if len(splited) == 3:
            # 0, 1, 2 -> no_change -- 0,2
            variations.append(2)
            continue
        if len(splited) == 4:
            # 0, 1, 2 ,3 -> no_change -- 0,2,3 -- 0,1,3 -- 0,3
            variations.append(4)
            continue
        if len(splited) == 5:
            # 0, 1, 2, 3, 4 -> no_change -- 0,2,3,4 -- 0,1,3,4 -- 0,1,2,4 -- 0,3,4 -- 0,2,4 -- 0,1,4
            variations.append(7)
            continue
        raise NotImplementedError
    return variations


def part_two(data: list[str]) -> Union[str, int]:
    adapters = [int(x) for x in data]
    adapters.sort()
    adapters.insert(0, 0)
    adapters.append(adapters[-1] + 3)
    return prod(variate_list(adapters))


def main(test: bool = False):
    test_case_1 = """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"""

    day = 10
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2020, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"\t\tday {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")

    return perf_counter() - start


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
