from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def part_one(data: list[str]) -> Union[str, int]:
    boat = 0
    direction = 1
    directions = [1j, 1, -1j, -1]
    for ix, instr in enumerate(data):
        if ix == 8:
            pass
        op, value = instr[0], int(instr[1:])
        match op:
            case "N":
                boat += value * 1j
            case "S":
                boat -= value * 1j
            case "E":
                boat += value
            case "W":
                boat -= value
            case "L":
                direction = (direction - (value // 90)) % 4
            case "R":
                direction = (direction + (value // 90)) % 4
            case "F":
                boat += value * directions[direction]

    return int(abs(boat.imag) + abs(boat.real))


def part_two(data: list[str]) -> Union[str, int]:
    waypoint = 10 + 1j
    boat = 0
    direction = 1
    directions = [1j, 1, -1j, -1]
    for ix, instr in enumerate(data):
        if ix == 8:
            pass
        op, value = instr[0], int(instr[1:])
        match op:
            case "N":
                waypoint += value * 1j
            case "S":
                waypoint -= value * 1j
            case "E":
                waypoint += value
            case "W":
                waypoint -= value
            case "L":
                for _ in range(value // 90):
                    waypoint *= 1j
            case "R":
                for _ in range(value // 90):
                    waypoint *= -1j
            case "F":
                boat += value * waypoint

    return int(abs(boat.imag) + abs(boat.real))


def main(test: bool = False):
    test_case_1 = """F10
N3
F7
R90
F11
"""

    day = 12
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
    main(False)
