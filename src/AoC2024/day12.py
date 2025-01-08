from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


class GardenPlot:
    def __init__(self, plant: str, pos: complex):
        self.plant = plant
        self.visited = False
        self.fences = 0
        self.area = 0
        self.pos = pos
        self.corner = 0

    def __repr__(self):
        return f"{self.plant=}, {self.area=}, {self.fences=}, {self.corner=}"


def data_to_map(data: list[str]) -> dict[complex, GardenPlot]:
    return dict(
        [(x + y * 1j, GardenPlot(c, x + y * 1j)) for y, line in enumerate(reversed(data)) for x, c in enumerate(line)]
    )


def get_neigh(garden, gardenplot: GardenPlot, uncheck=False) -> list[complex]:
    neigh = []
    for d in [1, 1j, -1, -1j]:
        pos = gardenplot.pos + d
        if uncheck or pos in garden:
            neigh.append(pos)
    return neigh


def bfs(
    garden: dict[complex, GardenPlot],
    start: GardenPlot,
    visited: set[complex] = None,
) -> set[complex]:
    if visited is None:
        visited = set()
    visited.add(start.pos)
    neighbors = get_neigh(garden, start, True)
    fences = [x not in garden or start.plant != garden[x].plant for x in neighbors]
    corners = [x and y for x, y in zip(fences, fences[1:] + [fences[0]])]
    start.corner = sum(corners)
    n, e, s, w = start.pos + 1j, start.pos + 1, start.pos - 1j, start.pos - 1
    sw, nw, ne, se = s + w - start.pos, n + w - start.pos, n + e - start.pos, s + e - start.pos
    d_corners = [sw, se, ne, nw]
    if start.corner == 1:
        for d, c in zip(d_corners, corners):
            if not c:
                continue
            start.corner += d in garden and garden[d].plant != start.plant
    if start.corner == 0:
        for corner, side_a, side_b in [(sw, s, w), (nw, n, w), (ne, n, e), (se, s, e)]:
            if corner in garden and garden[side_a].plant == start.plant == garden[side_b].plant:
                start.corner += garden[corner].plant != start.plant
    for neigh in get_neigh(garden, start):
        if neigh in visited:
            continue
        if garden[neigh].plant == start.plant:
            bfs(garden, garden[neigh], visited)

    return visited


def part_one(data: list[str]) -> Union[str, int]:
    garden = data_to_map(data)

    for pos, plot in garden.items():
        if plot.area == 0:
            section = bfs(garden, plot)
            for plant in section:
                garden[plant].area = len(section)
        neighbors = get_neigh(garden, plot)
        plot.fences = 4 - len(neighbors)
        for neigh in neighbors:
            if garden[neigh].plant != plot.plant:
                plot.fences += 1

    return sum(x.fences * x.area for x in garden.values())


def part_two(data: list[str]) -> Union[str, int]:
    garden = data_to_map(data)
    total = 0
    for pos, plot in garden.items():
        if plot.area == 0:
            section = bfs(garden, plot)
            # total.append((plot.plant, len(section), sum(garden[x].corner for x in section)))
            total += len(section) * sum(garden[x].corner for x in section)
            for plant in section:
                garden[plant].area = len(section)
    return total


def main(test: bool = False):
    test_case_1 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

    day = 12
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
