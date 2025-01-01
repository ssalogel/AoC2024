from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def part_one(data: list[str]) -> Union[str, int]:
    seats = []
    for line in data:
        row = int(line[:-3].replace("F", "0").replace("B", "1"), 2)
        col = int(line[-3:].replace("R", "1").replace("L", "0"), 2)
        seats.append((row << 3) + col)


    return max(seats)


def part_two(data: list[str]) -> Union[str, int]:
    seats = []
    for line in data:
        row = int(line[:-3].replace("F", "0").replace("B", "1"), 2)
        col = int(line[-3:].replace("R", "1").replace("L", "0"), 2)
        seats.append((row << 3) + col)
    seats.sort()
    changes = [b - a for a, b in zip(seats, seats[1:])]
    ix = changes.index(2)
    return seats[ix] + 1

def main(test: bool = False):
    test_case_1 = """FBFBBFFRLR
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL"""


    day = 5
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2020, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.info(f"the whole day {day} took {perf_counter() - start:.4f}s")

if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout) 
    main()
