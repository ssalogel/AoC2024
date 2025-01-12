from heapq import heappop, heappush
from collections import defaultdict
from math import inf
from typing import Any
from itertools import product


type Position = tuple[int, int, int] | tuple[int, int, int, int]


def data_to_grid(
    data: list[str], char_to_keep: str = None, default_value: Any = None, true_value: str = None, dimension: int = 2
) -> dict[Any, Any]:
    if default_value is not None:
        d = defaultdict(lambda: default_value)
    else:
        d = {}
    if dimension == 2:
        return __make_2D_grid(data, d, true_value, char_to_keep)
    return __make_XD_grid(data, d, true_value, char_to_keep, dimension - 2)


def __make_XD_grid(
    data: list[str], d: dict[Any, Any], true_value: str, char_to_keep: Any, extraDim: int
) -> dict[tuple[...], Any]:
    if true_value is not None:
        d.update(
            [
                (tuple([x, y] + [0] * extraDim), c in true_value)
                for y, line in enumerate(reversed(data))
                for x, c in enumerate(line)
                if char_to_keep is None or c in char_to_keep
            ]
        )
    else:
        d.update(
            [
                (tuple([x, y] + [0] * extraDim), c)
                for y, line in enumerate(reversed(data))
                for x, c in enumerate(line)
                if char_to_keep is None or c in char_to_keep
            ]
        )
    return d


def __make_2D_grid(data: list[str], d: dict[complex, Any], true_value: str, char_to_keep: Any) -> dict[complex, Any]:
    if true_value is not None:
        d.update(
            [
                (x + y * 1j, c in true_value)
                for y, line in enumerate(reversed(data))
                for x, c in enumerate(line)
                if char_to_keep is None or c in char_to_keep
            ]
        )
    else:
        d.update(
            [
                (x + y * 1j, c)
                for y, line in enumerate(reversed(data))
                for x, c in enumerate(line)
                if char_to_keep is None or c in char_to_keep
            ]
        )
    return d


def get_neighbors4(pos: complex) -> list[complex]:
    return [pos - 1j, pos + 1, pos + 1j, pos - 1]


def get_neighbors8(pos: complex) -> list[complex]:
    return [pos - 1j, pos + 1 - 1j, pos + 1, pos + 1 + 1j, pos + 1j, pos - 1 + 1j, pos - 1, pos - 1 - 1j]


def get_self_and_neighs_multi_dim(pos: Position) -> list[Position]:
    ranges = ((c - 1, c, c + 1) for c in pos)
    yield from product(*ranges)


def get_all_costs(grid: dict[complex, str], start: complex = 0) -> dict[complex, int]:
    count = 0
    heap = [(0, count, complex(0))]
    costs = dict([(x, inf) for x in grid if grid[x] != "#"])
    costs[start] = 0
    while heap:
        cost, _, curr_pos = heappop(heap)
        for next_pos in get_neighbors4(curr_pos):
            next_cost = cost + 1
            if next_pos in grid and grid[next_pos] != "#" and next_cost < costs[next_pos]:
                costs[next_pos] = next_cost
                count += 1
                heappush(heap, (next_cost, count, next_pos))
    return costs
