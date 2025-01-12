from itertools import combinations
from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from math import lcm

logger = logging.getLogger("AoC")


type Velocity = list[int]
type Coords = list[int]
type Moon = tuple[Coords, Velocity]


def parse_moons(data: list[str]) -> list[Moon]:
    moons = []
    for moon in data:
        coords = moon[1:-1].split(", ")
        moons.append(([int(coords[0][2:]), int(coords[1][2:]), int(coords[2][2:])], [0, 0, 0]))
    return moons


def step(moons: list[Moon], axises: list[int]) -> list[Moon]:
    for moon_a, moon_b in combinations(moons, 2):
        for axis in axises:
            delta_b = (
                (moon_a[0][axis] - moon_b[0][axis]) // abs(moon_a[0][axis] - moon_b[0][axis])
                if moon_a[0][axis] != moon_b[0][axis]
                else 0
            )
            moon_a[1][axis] += -1 * delta_b
            moon_b[1][axis] += delta_b
    for moon in moons:
        for axis in axises:
            moon[0][axis] += moon[1][axis]
    return moons


def calc_moon_energy(moon: Moon) -> int:
    pos, vel = moon
    tot = sum(map(abs, pos))
    tot *= sum(map(abs, vel))
    return tot


def part_one(data: list[str]) -> Union[str, int]:
    moons = parse_moons(data)
    for _ in range(1000):
        moons = step(moons, [0, 1, 2])

    energy = sum(map(calc_moon_energy, moons))
    return energy


def part_two(data: list[str]) -> Union[str, int]:
    moons = parse_moons(data)
    og_pos = [pos for pos, v in moons]
    periods = []
    for axis in [0, 1, 2]:
        moons = parse_moons(data)
        c = 0
        while True:
            moons = step(moons, [axis])
            c += 1
            if all(map(lambda moon: moon[0] in og_pos and sum(moon[1]) == 0, moons)):
                periods.append(c)
                break
    return lcm(*periods)


def main(test: bool = False):
    test_case_1 = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""

    day = 12
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2019, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"\t\tday {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")

    return perf_counter() - start


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
