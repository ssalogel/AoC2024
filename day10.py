from time import perf_counter
from typing import Union

from utils import Day

def to_map(data: list[str]) -> dict[complex, dict[str, int|set[complex]]]:
    res = {}
    for y, row in enumerate(reversed(data)):
        for x,digit in enumerate(row):
            res[x + 1j * y] = {"height": int(digit), "score": set()}
    return res

def get_neigh_score(top_map: dict[complex, dict[str, int|set]], pos: complex, width: int, height: int) -> set[complex]:
    d = 1j
    target_height = top_map[pos]["height"] + 1
    scores = set()
    for _ in range(4):
        d *= -1j
        neigh = pos + d
        if 0 > neigh.real or neigh.real >= width or 0 > neigh.imag or neigh.imag >= height:
            continue
        if top_map[neigh]["height"] == target_height:
            scores.update(top_map[neigh]["score"])
    return scores

def get_neigh_trails(top_map: dict[complex, dict[str, int|set]], pos: complex, width: int, height: int) -> set[complex]:
    d = 1j
    target_height = top_map[pos]["height"] + 1
    scores = set()
    for _ in range(4):
        d *= -1j
        neigh = pos + d
        if 0 > neigh.real or neigh.real >= width or 0 > neigh.imag or neigh.imag >= height:
            continue
        if top_map[neigh]["height"] == target_height:
            sc = [(pos, x) for x in top_map[neigh]["score"]]
            scores.update(sc)
    return scores

def part_one(data: list[str]) -> Union[str, int]:
    width = len(data)
    height = len(data[0])
    top_map = to_map(data)
    for d in reversed(range(10)):
        for x in range(width):
            for y in range(height):
                pos = x + 1j * y
                if d == 9 and top_map[pos]["height"] == d:
                    top_map[pos]["score"].add(pos)
                    continue
                if top_map[pos]["height"] == d:
                    top_map[pos]["score"].update(get_neigh_score(top_map, pos, width, height))
    return sum(len(x["score"]) for x in top_map.values() if x["height"] == 0) 

def part_two(data: list[str]) -> Union[str, int]:
    width = len(data)
    height = len(data[0])
    top_map = to_map(data)
    for d in reversed(range(10)):
        for x in range(width):
            for y in range(height):
                pos = x + 1j * y
                if d == 9 and top_map[pos]["height"] == d:
                    top_map[pos]["score"].add(pos)
                    continue
                if top_map[pos]["height"] == d:
                    top_map[pos]["score"].update(get_neigh_trails(top_map, pos, width, height))
    return sum([len(x["score"]) for x in top_map.values() if x["height"] == 0])

def main():
    test_case_1 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

    test = False
    day = 10
    if test:
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(day).strip().split("\n")


    start = perf_counter()
    print(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    print(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    print(f"the whole day {day} took {perf_counter() - start:.4f}s")



main()
