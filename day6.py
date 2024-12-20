from typing import Union
from utils import Day
from collections import defaultdict
from time import perf_counter


def get_visited(grid: dict[complex, str], width, height, guard: complex) -> set[complex]:
    visited = set()
    move = 1j
    while 0 <= guard.real < width and 0 <= guard.imag < height:
        visited.add(guard)
        while grid[guard + move] == "#":
            move *= -1j
        guard += move
    return visited


def data_to_map(data: list[str]) -> dict[complex, str]:
    d = defaultdict(lambda: "_")
    d.update([(x + y * 1j, letter) for y, line in enumerate(reversed(data)) for x, letter in enumerate(line)])
    return d


def part_one(data: list[str]) -> Union[str, int]:
    width = len(data)
    heigth = len(data[0])
    grid = data_to_map(data)
    for pos, value in grid.items():
        if "^" == value:
            guard = pos
            break
    return len(get_visited(grid, width, heigth, guard))


def part_two(data: list[str]) -> Union[str, int]:
    width = len(data)
    height = len(data[0])
    grid = data_to_map(data)
    total = 0
    for pos, value in grid.items():
        if "^" == value:
            guard = pos
            break

    for pos in get_visited(grid, width, height, guard):
        if grid[pos] in ["^", "#"]:
            continue
        grid[pos] = "#"
        move = 1j
        n_guard = guard
        visited = set()

        while 0 <= n_guard.real < width and 0 <= n_guard.imag < height:
            if (n_guard, move) in visited:
                total += 1
                break
            visited.add((n_guard, move))
            while grid[n_guard + move] == "#":
                move *= -1j
            n_guard += move

        grid[pos] = "."
    return total


def main():
    test = False
    test_case_1 = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

    day = 6
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
