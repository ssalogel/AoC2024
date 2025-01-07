from collections import defaultdict
from itertools import combinations
from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from math import prod

logger = logging.getLogger("AoC")


class Tile:
    def __init__(self, ID: int, draw: list[list[str]], rot: int = 0, hflip: bool = False, vflip: bool = False):
        self.ID = ID
        self.drawing = draw
        self.rotation = rot
        self.hflip = hflip
        self.vflip = vflip
        self.edges = self.get_edges()

    def __eq__(self, other):
        return (
            self.ID == other.ID
            and self.rotation == other.rotation
            and self.hflip == other.hflip
            and self.vflip == other.vflip
        )

    def flip_hor(self) -> "Tile":
        if self.hflip:
            raise NotImplementedError
        drawing = [line[::-1] for line in self.drawing]
        return Tile(self.ID, drawing, self.rotation, True, self.vflip)

    def flip_ver(self) -> "Tile":
        if self.vflip:
            raise NotImplementedError
        drawing = self.drawing[::-1]
        return Tile(self.ID, drawing, self.rotation, self.hflip, True)

    def rotate(self, nb) -> "Tile":
        if nb not in (-1, 1):
            raise NotImplementedError
        drawing = [[] for _ in range(len(self.drawing[0]))]
        for i, y in enumerate(range(len(self.drawing) - 1, -1, -1)):
            it = iter(self.drawing[y]) if nb == 1 else reversed(self.drawing[i])
            for x, v in enumerate(it):
                drawing[x].append(v)

        return Tile(self.ID, drawing, nb, self.hflip, self.vflip)

    def get_edges(self) -> dict[str, str]:
        res = {
            "n": "".join(self.drawing[0]),
            "s": "".join(self.drawing[-1]),
            "e": "".join(line[-1] for line in self.drawing),
            "w": "".join(line[0] for line in self.drawing),
        }
        return res

    def __repr__(self):
        return f"{self.ID}, {self.rotation=}, {self.hflip=}, {self.vflip=}"


def find_corners(tiles: dict[int, list[Tile]]) -> dict[int, str]:
    matching_sides = defaultdict(str)
    corners = {}

    for a_tile, b_tile in combinations(tiles, 2):
        a, b = tiles[a_tile][0], tiles[b_tile][0]
        for side_a in "nswe":
            for side_b in "nswe":
                edge_a, edge_b = a.edges[side_a], b.edges[side_b]
                if edge_a == edge_b or edge_a == edge_b[::-1]:
                    matching_sides[a_tile] += side_a
                    matching_sides[b_tile] += side_b

    for tile_id, sides in matching_sides.items():
        if len(sides) == 2:
            corners[tile_id] = sides
    return corners


def part_one(data: list[str]) -> Union[str, int]:
    tiles = {
        int(line.split("\n")[0][5:-1]): [Tile(int(line.split("\n")[0][5:-1]), [list(x) for x in line.split("\n")[1:]])]
        for line in data
    }
    corners = find_corners(tiles)
    return prod(corners)


# returns tile that has a side_conn edge match with start_tile side_start's edge
def match_tile(start_tile: Tile, tiles: dict[int, list[Tile]], side_start: str, side_conn: str) -> Tile:
    start_edge = start_tile.edges[side_start]

    for t_id, tile in tiles.items():
        for orientation in tile:
            if start_edge == orientation.edges[side_conn]:
                tiles.pop(orientation.ID)
                return orientation


def make_row(start_tile: Tile, tiles: dict[int, list[Tile]], len_row) -> list[Tile]:
    res = [start_tile]
    for _ in range(len_row - 1):
        tile = match_tile(res[-1], tiles, "e", "w")
        res.append(tile)
    return res


def find_dragons(puzzle: Tile) -> int:
    # Dragon: |                  # |
    #         |#    ##    ##    ###|
    #         | #  #  #  #  #  #   |
    start_ix = 18
    count = 0
    for y, row in enumerate(puzzle.drawing[:-2]):
        for x, c in enumerate(row[start_ix:-1], 18):
            if c == "#":
                row2 = puzzle.drawing[y + 1]
                row3 = puzzle.drawing[y + 2]
                if (
                    "#"
                    == row2[x - 18]
                    == row2[x - 13]
                    == row2[x - 12]
                    == row2[x - 7]
                    == row2[x - 6]
                    == row2[x - 1]
                    == row2[x]
                    == row2[x + 1]
                ):
                    if "#" == row3[x - 17] == row3[x - 14] == row3[x - 11] == row3[x - 8] == row3[x - 5] == row3[x - 2]:
                        count += 1
    return count


def part_two(data: list[str]) -> Union[str, int]:
    tiles = {
        int(line.split("\n")[0][5:-1]): [Tile(int(line.split("\n")[0][5:-1]), [list(x) for x in line.split("\n")[1:]])]
        for line in data
    }
    corners = find_corners(tiles)
    # arbitrary top_left corner:
    top_left_id, sides = corners.popitem()
    topleft = tiles[top_left_id][0]

    if sides in ("ne", "en"):
        topleft = topleft.rotate(1)
    elif sides in ("nw", "wn"):
        topleft = topleft.flip_hor().flip_ver()
    elif sides in ("ws", "sw"):
        topleft = topleft.rotate(-1)

    img_size = int(len(tiles) ** 0.5)

    tiles.pop(top_left_id)

    # pre-generate all possibilities for every tile (8 total arrangements per tile, x143 tiles, 1152 total tiles)
    for tile_id in tiles:
        tile = tiles[tile_id][0]
        vtile = tile.flip_ver()
        htile = tile.flip_hor()
        tiles[tile_id].extend(
            [vtile, htile, vtile.flip_hor(), tile.rotate(1), tile.rotate(-1), htile.rotate(-1), htile.rotate(1)]
        )

    puzzle_pieces = []
    for r in range(img_size):
        if r == 0:
            row = make_row(topleft, tiles, img_size)
        else:
            first = match_tile(puzzle_pieces[-1][0], tiles, "s", "n")
            row = make_row(first, tiles, img_size)
        puzzle_pieces.append(row)

    puzzle = []
    for row in puzzle_pieces:
        for line in range(1, len(row[0].drawing[0]) - 1):
            puzzle.append("".join(["".join(x.drawing[line][1:-1]) for x in row]))
    puzzle = Tile(0, puzzle)
    vpuzzle = puzzle.flip_ver()
    hpuzzle = puzzle.flip_hor()
    puzzle = [puzzle] + [
        vpuzzle,
        hpuzzle,
        vpuzzle.flip_hor(),
        puzzle.rotate(1),
        puzzle.rotate(-1),
        hpuzzle.rotate(-1),
        hpuzzle.rotate(1),
    ]

    d = max(find_dragons(p) for p in puzzle)
    return sum(c == "#" for row in puzzle[0].drawing for c in row) - d * 15


def main(test: bool = False):
    test_case_1 = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"""

    day = 20
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n\n")
    else:
        data = Day.get_data(2020, day).strip().split("\n\n")

    start = perf_counter()
    logger.info(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.info(f"the whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
