from typing import Union
from itertools import combinations
from utils import Day

def to_grid(data: list[str]) -> dict[str, list[tuple[int, int]]]:
    d = {}
    for char, pos in [(c, (x, y)) for y, line in enumerate(data) for x,c in enumerate(line)]:
        if char == '.':
            continue
        if char in d:
            d[char].append(pos)
        else:
            d[char] = [pos]
    return d

def get_distance(pos1: tuple[int, int], pos2: tuple[int, int]) -> tuple[int, int]:
    return pos1[0] - pos2[0], pos1[1] - pos2[1]

def part_one(data: list[str]) -> Union[str, int]:
    width = len(data)
    heigth = len(data[0])
    antinodes = set()
    for char, positions in to_grid(data).items():
        for pair in combinations(positions, 2):
            el1, el2 = pair
            dist = get_distance(el1, el2)
            n1 = (el1[0] + dist[0], el1[1] + dist[1])
            if 0 <= n1[0] < width and 0 <= n1[1] < heigth:
                antinodes.add(n1)
            n2 = (el2[0] - dist[0], el2[1] - dist[1])
            if 0 <= n2[0] < width and 0 <= n2[1] < heigth:
                antinodes.add(n2)
    return len(antinodes)

def part_two(data: list[str]) -> Union[str, int]:
    width = len(data)
    heigth = len(data[0])
    antinodes = set()
    for char, positions in to_grid(data).items():
        for pair in combinations(positions, 2):
            el1, el2 = pair
            antinodes.add(el1)
            antinodes.add(el2)
            dist = get_distance(el1, el2)
            nf = (el1[0] + dist[0], el1[1] + dist[1])
            while 0 <= nf[0] < width and 0 <= nf[1] < heigth:
                antinodes.add(nf)
                nf = (nf[0] + dist[0], nf[1] + dist[1])
            nb = (el2[0] - dist[0], el2[1] - dist[1])
            while 0 <= nb[0] < width and 0 <= nb[1] < heigth:
                antinodes.add(nb)
                nb = (nb[0] - dist[0], nb[1] - dist[1])
    return len(antinodes)


def main():
    test_case_1 = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""

    test = False
    day = 8
    if test:
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(day).strip().split("\n")


    print(f"day {day} part 1: {part_one(data)}")
    print(f"day {day} part 2: {part_two(data)}")


main()