from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def get_loop_size(pub_key: int, subject_number: int = 7, mod: int = 20201227) -> int:
    value = 1
    count = 0
    while value != pub_key:
        count += 1
        value = value * subject_number % mod
    return count


def get_encr_key(loop_size: int, pub_key: int) -> int:
    value = 1
    for _ in range(loop_size):
        value = value * pub_key % 20201227
    return value


def part_one(data: list[str]) -> Union[str, int]:
    card, door = list(map(int, data))
    c_loop_size = get_loop_size(card)
    d_loop_size = get_loop_size(door)
    c_encr = get_encr_key(d_loop_size, card)
    d_encr = get_encr_key(c_loop_size, door)

    return c_encr


def main(test: bool = False):
    test_case_1 = """5_764_801
17_807_724"""

    day = 25
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2020, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")

    return perf_counter() - start


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
