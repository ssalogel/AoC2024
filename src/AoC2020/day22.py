from collections import deque
from itertools import islice
from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def parse_deck(data: list[str]) -> tuple[deque[int], deque[int]]:
    p1 = deque()
    p2 = deque()
    for line in data[0].split("\n")[1:]:
        p1.append(int(line))
    for line in data[1].split("\n")[1:]:
        p2.append(int(line))
    return p1, p2


def part_one(data: list[str]) -> Union[str, int]:
    p1, p2 = parse_deck(data)

    while len(p1) > 0 and len(p2) > 0:
        c1, c2 = p1.popleft(), p2.popleft()
        if c1 > c2:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)
    winner = max(p1, p2, key=len)
    return sum((i+1) * x for i,x in enumerate(reversed(winner)))


def part_two(data: list[str]) -> Union[str, int]:
    p1, p2 = parse_deck(data)
    def play(p1: deque[int], p2: deque[int]) -> tuple[int, deque[int], deque[int]]:
        recur_break = set()
        while len(p1) > 0 and len(p2) > 0:
            recur_check = (",".join(str(x) for x in p1), ",".join(str(x) for x in p2))
            if recur_check in recur_break:
                return 1, p1, p2
            recur_break.add(recur_check)

            c1, c2 = p1.popleft(), p2.popleft()
            if c1 <= len(p1) and c2 <= len(p2):
                w, _, _ = play(deque(list(p1)[0:c1]), deque(list(p2)[0:c2]))
            else:
                w = int(c1 > c2)
            if w == 1:
                p1.append(c1)
                p1.append(c2)
            else:
                p2.append(c2)
                p2.append(c1)
        return len(p1) > 0, p1, p2

    res = play(p1, p2)
    return sum((i+1) * x for i,x in enumerate(reversed(res[1 if res[0] else 2])))


def main(test: bool = False):
    test_case_1 = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

    day = 22
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n\n")
    else:
        data = Day.get_data(2020, day).strip().split("\n\n")

    start = perf_counter()
    logger.info(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.info(f"the whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
