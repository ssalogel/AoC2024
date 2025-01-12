from typing import Union
from time import perf_counter

from src.AoC2019.IntCode import IntCode, State
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def part_one(data: list[str]) -> Union[str, int]:
    comp = IntCode([int(d) for d in data[0].split(",")])
    comp.run_until_end()
    grid = {}
    while comp.output:
        x, y, tile = comp.output.popleft(), comp.output.popleft(), comp.output.popleft()
        grid[(x, y)] = tile
    return sum(v == 2 for v in grid.values())


def part_two(data: list[str]) -> Union[str, int]:
    comp = IntCode([int(d) for d in data[0].split(",")])
    comp.code[0] = 2
    screen = {}
    ball = (0, 0)
    paddle = (0, 0)
    while comp.state != State.DONE:
        comp.run_until_end()
        while comp.output:
            x, y, tile = comp.output.popleft(), comp.output.popleft(), comp.output.popleft()
            screen[(x, y)] = tile
            if tile == 4:
                ball = (x, y)
            if tile == 3:
                paddle = (x, y)
        if ball[0] > paddle[0]:
            comp.add_input(1)
        elif ball[0] < paddle[0]:
            comp.add_input(-1)
        else:
            comp.add_input(0)

    return screen[(-1, 0)]


def main(test: bool = False):
    test_case_1 = """"""

    day = 13
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
