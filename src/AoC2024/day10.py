from time import perf_counter
from typing import Union
from src.utils.Grids import data_to_grid
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def to_map(data: list[str]) -> dict[complex, dict[str, int | set[complex]]]:
    res = data_to_grid(data)
    for k, v in res.items():
        res[k] = {"height": int(v), "score": set()}
    return res


def get_neigh_score(top_map: dict[complex, dict[str, int | set]], pos: complex) -> set[complex]:
    d = 1j
    target_height = top_map[pos]["height"] + 1
    scores = set()
    for _ in range(4):
        d *= -1j
        neigh = pos + d
        if neigh not in top_map:
            continue
        if top_map[neigh]["height"] == target_height:
            scores.update(top_map[neigh]["score"])
    return scores


def get_neigh_trails(top_map: dict[complex, dict[str, int | set]], pos: complex) -> set[complex]:
    d = 1j
    target_height = top_map[pos]["height"] + 1
    scores = set()
    for _ in range(4):
        d *= -1j
        neigh = pos + d
        if neigh not in top_map:
            continue
        if top_map[neigh]["height"] == target_height:
            sc = [(pos, x) for x in top_map[neigh]["score"]]
            scores.update(sc)
    return scores


def part_one(data: list[str]) -> Union[str, int]:
    top_map = to_map(data)
    for d in reversed(range(10)):
        for pos, v in top_map.items():
            if d == 9 and v["height"] == d:
                v["score"].add(pos)
                continue
            if v["height"] == d:
                v["score"].update(get_neigh_score(top_map, pos))
    return sum(len(x["score"]) for x in top_map.values() if x["height"] == 0)


def part_two(data: list[str]) -> Union[str, int]:
    top_map = to_map(data)
    for d in reversed(range(10)):
        for pos, v in top_map.items():
            if d == 9 and v["height"] == d:
                v["score"].add(pos)
                continue
            if v["height"] == d:
                v["score"].update(get_neigh_trails(top_map, pos))
    return sum([len(x["score"]) for x in top_map.values() if x["height"] == 0])


def main(test: bool = False):
    test_case_1 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

    day = 10
    if test:
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2024, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"\t\tday {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
