from functools import reduce
from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from functools import reduce

logger = logging.getLogger("AoC")
type Tile = tuple[int, int, int]


def get_neigh(tile: Tile) -> tuple[Tile, Tile, Tile, Tile, Tile, Tile]:
    return (
        (tile[0] + 1, tile[1], tile[2] - 1),
        (tile[0] - 1, tile[1], tile[2] + 1),
        (tile[0], tile[1] + 1, tile[2] - 1),
        (tile[0] - 1, tile[1] + 1, tile[2]),
        (tile[0] + 1, tile[1] - 1, tile[2]),
        (tile[0], tile[1] - 1, tile[2] + 1),
    )


def parse_instr(data: list[str]) -> list[list[str]]:
    res = []
    for line in data:
        index = 0
        instr = []
        while index < len(line):
            if line[index] in ("e", "w"):
                instr.append(line[index])
                index += 1
            else:
                instr.append(line[index : index + 2])
                index += 2
        res.append(instr)
    return res


def make_tile_floor(tile_paths: list[list[str]]) -> set[Tile]:
    grid: set[Tile] = set()
    for tile_path in tile_paths:
        tile = (0, 0, 0)
        for instr in tile_path:
            match instr:
                case "e":
                    tile = (tile[0] + 1, tile[1], tile[2] - 1)
                case "w":
                    tile = (tile[0] - 1, tile[1], tile[2] + 1)
                case "se":
                    tile = (tile[0], tile[1] + 1, tile[2] - 1)
                case "sw":
                    tile = (tile[0] - 1, tile[1] + 1, tile[2])
                case "ne":
                    tile = (tile[0] + 1, tile[1] - 1, tile[2])
                case "nw":
                    tile = (tile[0], tile[1] - 1, tile[2] + 1)
        if tile in grid:
            grid.remove(tile)
        else:
            grid.add(tile)
    return grid


def part_one(data: list[str]) -> Union[str, int]:
    tile_paths = parse_instr(data)

    return len(make_tile_floor(tile_paths))


def part_two(data: list[str]) -> Union[str, int]:
    tiles = make_tile_floor(parse_instr(data))
    for _ in range(100):
        new_tiles: set[Tile] = set()
        tiles_to_check: set[Tile] = set(x for t in tiles for x in get_neigh(t))
        tiles_to_check.update(tiles)
        for tile in tiles_to_check:
            black_nei = sum(t in tiles for t in get_neigh(tile))
            if black_nei == 2 or (tile in tiles and black_nei == 1):
                new_tiles.add(tile)
        tiles = new_tiles
    return len(tiles)


def main(test: bool = False):
    test_case_1 = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

    day = 24
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2020, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"\t\tday {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")

    return perf_counter() - start


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
