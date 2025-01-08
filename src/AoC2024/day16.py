from collections import defaultdict
from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from src.utils.Grids import data_to_grid, get_neighbors4

logger = logging.getLogger("AoC")
from heapq import heappop, heappush
from math import inf


def get_all_path(data: list[str]):
    dimx = len(data[0])
    maze = "".join(data)
    visited = {}
    heap = []
    start, target = maze.index("S"), maze.index("E")
    best_score = inf
    directions = [-dimx, 1, dimx, -1]
    paths = []

    heappush(heap, (0, start, 1, []))
    while heap:
        score, pos, direction, path = heappop(heap)
        if score > best_score:
            break
        if (pos, direction) in visited and visited[(pos, direction)] < score:
            continue
        visited[(pos, direction)] = score
        if pos == target:
            best_score = score
            paths.append(path + [target])
        if maze[pos + directions[direction]] != "#":
            heappush(heap, (score + 1, pos + directions[direction], direction, path + [pos]))
        heappush(heap, (score + 1000, pos, (direction + 1) % 4, path + [pos]))
        heappush(heap, (score + 1000, pos, (direction - 1) % 4, path + [pos]))
    return paths


def djikstra(grid: dict[complex, str], start: complex):
    count = 0
    heap = [(0, count, 1, start)]
    costs = dict([(x, inf) for x in grid if grid[x] != "#"])
    costs[start] = (0, set())
    while heap:
        cost, _, direction, curr_pos = heappop(heap)
        # go ahead
        next_pos = curr_pos + direction
        next_cost = cost + 1
        if grid[next_pos] != "#" and next_cost < costs[next_pos]:
            costs[next_pos] = next_cost
            count += 1
            heappush(heap, (next_cost, count, direction, next_pos))
        # turn left
        next_dir = direction * -1j
        next_pos = curr_pos + next_dir
        next_cost = cost + 1001
        if grid[next_pos] != "#" and next_cost < costs[next_pos]:
            costs[next_pos] = next_cost
            count += 1
            heappush(heap, (next_cost, count, next_dir, next_pos))
        # turn right
        next_dir = direction * 1j
        next_pos = curr_pos + next_dir
        next_cost = cost + 1001
        if grid[next_pos] != "#" and next_cost < costs[next_pos]:
            costs[next_pos] = next_cost
            count += 1
            heappush(heap, (next_cost, count, next_dir, next_pos))

    return costs


def build_neigh_map(data: list[str]) -> tuple[dict[complex, list[complex]], complex, complex]:
    grid = data_to_grid(data)
    nei_grid = defaultdict(list)
    start = end = 0
    for pos, char in grid.items():
        if char == "S":
            start = pos
        if char == "E":
            end = pos
        for nei in get_neighbors4(pos):
            if grid[pos] != "#":
                nei_grid[pos].append(nei)
    return nei_grid, start, end


def explore(start, end, nei_grid, direction) -> int:
    count = 0
    q = [(0, count, start, direction, frozenset([start]))]
    distance = defaultdict(lambda: float("inf"))
    best_path_points = set()
    best = float("inf")

    while q:
        score, _, pos, direction, path = heappop(q)
        if pos == end:
            if score < best:
                best = score
                best_path_points = path
            elif score == best:
                best_path_points |= path
            continue

        k = pos, direction
        if distance[k] < score:
            continue

        distance[k] = score

        for nei in nei_grid[pos]:
            if nei in path:
                continue

            dir2 = nei - pos
            turn_cost = 0
            if dir2 != direction:
                turn_cost = 1000
            if dir2 + direction == 0:
                turn_cost = 2000
            count += 1
            heappush(q, (score + 1 + turn_cost, count, nei, dir2, path | {nei}))
    return len(best_path_points)


def part_one(data: list[str]) -> Union[str, int]:
    grid = data_to_grid(data)
    reindeer = target = 0
    for pos, c in grid.items():
        if c == "S":
            reindeer = pos
        if c == "E":
            target = pos
    costs = djikstra(grid, reindeer)
    return costs[target]


def part_two(data: list[str]) -> Union[str, int]:
    nei_grid, start, end = build_neigh_map(data)
    return explore(start, end, nei_grid, 1)


def main(test: bool = False):
    test_case_1 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""

    day = 16
    if test:
        logger.info("TEST VALUES")
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
    main()
