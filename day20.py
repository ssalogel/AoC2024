from typing import Union, Container
from time import perf_counter
from utils import Day
from collections import Counter, defaultdict
from itertools import combinations
from math import isnan


def bfs(grid: list[list[str]], start: tuple[int, int]) -> int:
    visited = set()
    to_visit = [(start, 0)]
    costs = defaultdict(lambda: float("inf"))
    while to_visit:
        pos, cost = to_visit.pop(0)
        costs[pos] = cost
        visited.add(pos)
        for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            npos = pos[0] + x, pos[1] + y
            if npos not in visited and grid[pos[1] + y][pos[0] + x] != "#":
                to_visit.append((npos, cost + 1))
    return costs


def part_one(data: list[str]) -> Union[str, int]:
    grid = list(list(row) for row in data)
    for y, row in enumerate(grid):
        if "S" in row:
            start = (row.index("S"), y)
            break
    costs = bfs(grid, start)
    cheats = []
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[0]) - 1):
            if grid[y][x] == "#":
                for a, b in combinations([(1, 0), (0, 1), (-1, 0), (0, -1)], 2):
                    pos_a = (x + a[0], y + a[1])
                    pos_b = (x + b[0], y + b[1])
                    cheat = abs(costs[pos_a] - costs[pos_b]) - 2
                    if cheat != float("inf") and not isnan(cheat):
                        cheats.append(cheat)
    c = Counter(cheats)
    return sum(map(lambda x: x >= 100, cheats))


def part_two(data: list[str]) -> Union[str, int]:
    grid = list(list(row) for row in data)
    for y, row in enumerate(grid):
        if "S" in row:
            start = (row.index("S"), y)
            break
    costs = bfs(grid, start)
    cheats = []
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[0]) - 1):
            pos = (x, y)
            if grid[y][x] != "#":
                for d_x in range(-20, 21):
                    vertical_range = 20 - abs(d_x)
                    for d_y in range(-vertical_range, vertical_range + 1):
                        n_pos = (x + d_x, y + d_y)
                        if costs[n_pos] == float("inf"):
                            continue
                        cheat = costs[n_pos] - costs[pos] - abs(d_x) - abs(d_y)
                        if cheat > 0:
                            cheats.append(cheat)
    c = Counter(cheats)
    return sum(map(lambda x: x >= 100, cheats))


def main():
    test_case_1 = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""

    test = False
    day = 20
    if test:
        print("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(day).strip().split("\n")

    start = perf_counter()
    print(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    print(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    print(f"the whole day {day} took {perf_counter() - start:.4f}s")


main()
