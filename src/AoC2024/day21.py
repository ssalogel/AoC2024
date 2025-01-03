from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")
from functools import lru_cache
from heapq import heappop, heappush

numpad = {
    "A": {"<": "0", "^": "3"},
    "0": {">": "A", "^": "2"},
    "1": {">": "2", "^": "4"},
    "2": {"<": "1", ">": "3", "^": "5", "v": "0"},
    "3": {"<": "2", "^": "6", "v": "A"},
    "4": {">": "5", "^": "7", "v": "1"},
    "5": {"<": "4", ">": "6", "^": "8", "v": "2"},
    "6": {"<": "5", "^": "9", "v": "3"},
    "7": {">": "8", "v": "4"},
    "8": {"<": "7", ">": "9", "v": "5"},
    "9": {"<": "8", "v": "6"},
}

keypad = {
    "A": {"<": "^", "v": ">"},
    "^": {">": "A", "v": "v"},
    "<": {">": "v"},
    "v": {"<": "<", "^": "^", ">": ">"},
    ">": {"<": "v", "^": "A"},
}


@lru_cache()
def navigate_numpad(start: str, end: str) -> set[str]:
    if start == end:
        return {"A"}
    length_solution = float("inf")
    paths: set[str] = set()
    to_explore = [(0, start, "")]
    while to_explore:
        len_path, pos, path_so_far = heappop(to_explore)
        if pos == end:
            paths.add(path_so_far + "A")
            length_solution = len_path + 1
            continue
        if len_path == length_solution:
            continue
        for d, n in numpad[pos].items():
            heappush(to_explore, (len_path + 1, n, path_so_far + d))
    return paths


@lru_cache()
def navigate_keypad(start: str, end: str) -> set[str]:
    if start == end:
        return {"A"}
    length_solution = float("inf")
    paths: set[str] = set()
    to_explore = [(0, start, "")]
    while to_explore:
        len_path, pos, path_so_far = heappop(to_explore)
        if pos == end:
            paths.add(path_so_far + "A")
            length_solution = len_path + 1
            continue
        if len_path == length_solution:
            continue
        for d, n in keypad[pos].items():
            heappush(to_explore, (len_path + 1, n, path_so_far + d))
    return paths


@lru_cache()
def get_best_key_paths_len(path: str, depth: int = 0) -> int:
    if depth == 0:
        return len(path)
    keys = []
    start = "A"
    for c in path:
        keys.append(navigate_keypad(start, c))
        start = c
    min_path = 0
    for key in keys:
        min_key = float("inf")
        for section in key:
            attmp = get_best_key_paths_len(section, depth - 1)
            if min_key > attmp:
                min_key = attmp
        min_path += min_key
    return min_path


def solve(code, depth):
    numpad_pos = "A"
    numpad_paths = []
    for c in code:
        ways = navigate_numpad(numpad_pos, c)
        numpad_paths.append(ways)
        numpad_pos = c
    min_path = 0
    for section in numpad_paths:
        min_section = float("inf")
        for path in section:
            length = get_best_key_paths_len(path, depth)
            if length < min_section:
                min_section = length
        min_path += min_section
    return min_path


def part_one(data: list[str]) -> Union[str, int]:
    res = []
    for code in data:
        res.append(solve(code, 2) * int(code[:-1]))
    return sum(res)


def part_two(data: list[str]) -> Union[str, int]:
    res = []
    for code in data:
        res.append(solve(code, 25) * int(code[:-1]))
    return sum(res)


def main(test: bool = False):
    test_case_1 = """029A
980A
179A
456A
379A"""

    day = 21
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2024, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.info(f"the whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main(True)
