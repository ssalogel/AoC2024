from math import inf
from typing import Union
from time import perf_counter
from utils import Day
from heapq import heappush, heappop

def djikstra(grid: dict[complex, str], width, length) -> dict[complex, int]:
        count = 0
        heap = [(0, count, 0)]
        costs = dict([(x, inf) for x in grid if grid[x] != "#"])
        costs[0] = 0
        directions = [1, 1j, -1, -1j]
        while heap:
            cost, _, curr_pos = heappop(heap)
            for direction in directions:
                next_pos = curr_pos + direction
                next_cost = cost + 1
                if next_pos in grid and grid[next_pos] != "#" and next_cost < costs[next_pos]:
                    costs[next_pos] = next_cost
                    count += 1
                    heappush(heap, (next_cost, count, next_pos))
        return costs



def part_one(data: list[str], width, length, safe) -> Union[str, int]:
    target = (width - 1) + (length - 1) * 1j
    grid = {x + y * 1j: "." for x in range(width) for y in range(length)}
    for i, pos in enumerate(int(b[:b.index(",")]) + int(b[b.index(",") + 1:]) * 1j for b in data):
        if i >= safe:
            break
        grid[pos] = "#"

    return djikstra(grid, width, length)[target]


def part_two(data: list[str], width, length, safe) -> Union[str, int]:
    target = (width - 1) + (length - 1) * 1j
    grid = {x + y * 1j: "." for x in range(width) for y in range(length)}
    for i, pos in enumerate(int(b[:b.index(",")]) + int(b[b.index(",") + 1:]) * 1j for b in data):
        if i >= safe:
            break
        grid[pos] = "#"

    for i, pos in enumerate(int(b[:b.index(",")]) + int(b[b.index(",") + 1:]) * 1j for b in data[safe:]):
        grid[pos] = "#"
        costs = djikstra(grid, width, length)
        if costs[target] != inf:
            continue
        return str(int(pos.real)) + "," + str(int(pos.imag))


def main():
    test_case_1 = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""

    test = False
    day = 18
    if test:
        print("TEST VALUES")
        data = test_case_1.strip().split("\n")
        width = length = 7
        safe = 12
    else:
        data = Day.get_data(day).strip().split("\n")
        width = length = 71
        safe = 1024

    start = perf_counter()
    print(f"day {day} part 1: {part_one(data, width, length, safe)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    print(f"day {day} part 2: {part_two(data, width, length, safe)} in {perf_counter() - mid:.4f}s")
    print(f"the whole day {day} took {perf_counter() - start:.4f}s")


main()
