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


def get_neigh(garden, gardenplot: GardenPlot, width, height, uncheck=False) -> list[complex]:
    neigh = []
    for d in [1, 1j, -1, -1j]:
        pos = gardenplot.pos + d
        if uncheck or (0 <= pos.real < width and 0 <= pos.imag < height):
            neigh.append(pos)
    return neigh


def bfs(
    garden: dict[complex, GardenPlot],
    start: GardenPlot,
    width: int,
    height: int,
    visited: set[complex] = None,
) -> set[complex]:
    if visited is None:
        visited = set()
    visited.add(start.pos)
    neighbors = get_neigh(garden, start, width, height, True)
    fences = [x not in garden or start.plant != garden[x].plant for x in neighbors]
    corners = [x and y for x, y in zip(fences, fences[1:] + [fences[0]])]
    start.corner = sum(corners)
    if start.corner == 1:
        for i, c in enumerate(corners):
            if not c:
                continue
            if i == 0 and (start.pos - 1 - 1j) in garden:
                start.corner += garden[(start.pos - 1 - 1j)].plant != start.plant
            if i == 1 and (start.pos + 1 - 1j) in garden:
                start.corner += garden[(start.pos + 1 - 1j)].plant != start.plant
            if i == 2 and (start.pos + 1 + 1j) in garden:
                start.corner += garden[(start.pos + 1 + 1j)].plant != start.plant
            if i == 3 and (start.pos - 1 + 1j) in garden:
                start.corner += garden[(start.pos - 1 + 1j)].plant != start.plant
    if start.corner == 0:
        if (start.pos - 1 - 1j) in garden and garden[start.pos - 1].plant == start.plant == garden[
            start.pos - 1j
        ].plant:
            start.corner += garden[(start.pos - 1 - 1j)].plant != start.plant
        if (start.pos + 1 - 1j) in garden and garden[start.pos + 1].plant == start.plant == garden[
            start.pos - 1j
        ].plant:
            start.corner += garden[(start.pos + 1 - 1j)].plant != start.plant
        if (start.pos + 1 + 1j) in garden and garden[start.pos + 1].plant == start.plant == garden[
            start.pos + 1j
        ].plant:
            start.corner += garden[(start.pos + 1 + 1j)].plant != start.plant
        if (start.pos - 1 + 1j) in garden and garden[start.pos - 1].plant == start.plant == garden[
            start.pos + 1j
        ].plant:
            start.corner += garden[(start.pos - 1 + 1j)].plant != start.plant
    for neigh in get_neigh(garden, start, width, height):
        if neigh in visited:
            continue
        if garden[neigh].plant == start.plant:
            bfs(garden, garden[neigh], width, height, visited)

    return visited


def part_one(data: list[str]) -> Union[str, int]:
    garden = data_to_map(data)
    width = len(data[0])
    height = len(data)
    for pos, plot in garden.items():
        if plot.area == 0:
            section = bfs(garden, plot, width, height)
            for plant in section:
                garden[plant].area = len(section)
        neighbors = get_neigh(garden, plot, width, height)
        plot.fences = 4 - len(neighbors)
        for neigh in neighbors:
            if garden[neigh].plant != plot.plant:
                plot.fences += 1

    return sum(x.fences * x.area for x in garden.values())


def part_two(data: list[str]) -> Union[str, int]:
    garden = data_to_map(data)
    width = len(data[0])
    height = len(data)
    total = 0
    for pos, plot in garden.items():
        if plot.area == 0:
            section = bfs(garden, plot, width, height)
            # total.append((plot.plant, len(section), sum(garden[x].corner for x in section)))
            total += len(section) * sum(garden[x].corner for x in section)
            for plant in section:
                garden[plant].area = len(section)
    return total


def main():
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

    test = False
    day = 12
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2024, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.info(f"the whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
