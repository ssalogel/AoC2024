from typing import Union
from time import perf_counter
from utils import Day
from heapq import heappop, heappush, heapify
from math import inf


def data_to_map(data: list[str]) -> dict[complex, str]:
    return dict([(x + y * 1j, c) for y, line in enumerate(reversed(data)) for x, c in enumerate(line)])


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


def part_one(data: list[str]) -> Union[str, int]:
    grid = data_to_map(data)
    reindeer = target = 0
    for pos, c in grid.items():
        if c == "S":
            reindeer = pos
        if c == "E":
            target = pos
    costs = djikstra(grid, reindeer)
    return costs[target]


def part_two(data: list[str]) -> Union[str, int]:
    paths = get_all_path(data)
    s = set()
    [s.update(x) for x in paths]
    return len(s)


def main():
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

    test = False
    day = 16
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
