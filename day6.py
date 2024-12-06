from typing import Union
from itertools import cycle
from utils import Day
from collections import defaultdict
from time import perf_counter


UP = (0, -1)
RIGHT = (1, 0)
DOWN = (0, 1)
LEFT = (-1, 0)

def get_visited(grid: dict[tuple[int, int], str], width, height, guard: tuple[int, int]) -> set[tuple[int,int]]:
    directions = cycle([UP, RIGHT, DOWN, LEFT])
    move = directions.__next__()
    pos = guard
    visited = set()
    while 0 <= pos[0] < width and 0 <= pos[1] < height:
        visited.add(guard)
        pos = (guard[0] + move[0], guard[1] + move[1])
        while grid[pos] == '#':
            move = directions.__next__()
            pos = (guard[0] + move[0], guard[1] + move[1])
        guard = pos
    return visited

def data_to_map(data: list[str]) -> dict[tuple[int, int], str]:
    d = defaultdict(lambda: '_')
    d.update([((x, y), letter) for y, line in enumerate(data) for x, letter in enumerate(line) ])
    return d


def part_one(data: list[str]) -> Union[str, int]:
    width = len(data)
    heigth = len(data[0])
    grid = data_to_map(data)
    for y, row in enumerate(data):
        if '^' in row:
            guard = (row.find('^'), y)
    return len(get_visited(grid, width, heigth, guard))

def part_two(data: list[str]) -> Union[str, int]:
    width = len(data)
    height = len(data[0])
    grid = data_to_map(data)
    total = 0
    for y, row in enumerate(data):
        if '^' in row:
            start = (row.find('^'), y)

    for pos in get_visited(grid, width, height, start):
        if grid[pos] in ['^', '#']:
            continue
        grid[pos] = '#'
        directions = cycle([UP, RIGHT, DOWN, LEFT])
        move = directions.__next__()
        n_guard = start
        guard = start
        visited = set()

        while 0 <= n_guard[0] < width and 0 <= n_guard[1] < height:
            if (guard, move) in visited:
                total += 1
                break
            visited.add((guard, move))
            n_guard = (guard[0] + move[0], guard[1] + move[1])
            while grid[n_guard] == '#':
                move = directions.__next__()
                n_guard = (guard[0] + move[0], guard[1] + move[1])
            guard = n_guard
        grid[pos] = '.'
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


    print(f"day {day} part 1: {part_one(data)}")
    start = perf_counter()
    print(f"day {day} part 2: {part_two(data)}, {perf_counter()-start}")


main()