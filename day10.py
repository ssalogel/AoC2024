from typing import Union

from utils import Day

def to_map(data: list[str]) -> dict[tuple[int, int], dict[str, int|set[int]]]:
    res = {}
    for y, row in enumerate(data):
        for x,digit in enumerate(row):
            res[(x, y)] = {"height": int(digit), "score": set()}
    return res

def get_neigh_score(top_map: dict[tuple[int, int], dict[str, int|set]], pos: tuple[int, int], width: int, height: int) -> set[tuple[int, int]]:
    directions = [(1,0), (0, 1), (-1, 0), (0, -1)]
    target_height = top_map[pos]["height"] + 1
    scores = set()
    for d in directions:
        neigh = (pos[0] + d[0], pos[1] + d[1])
        if 0 > neigh[0] or neigh[0] >= width or 0 > neigh[1] or neigh[1] >= height:
            continue
        if top_map[neigh]["height"] == target_height:
            scores.update(top_map[neigh]["score"])
    return scores

def get_neigh_trails(top_map: dict[tuple[int, int], dict[str, int|set]], pos: tuple[int, int], width: int, height: int) -> set[tuple[int, int]]:
    directions = [(1,0), (0, 1), (-1, 0), (0, -1)]
    target_height = top_map[pos]["height"] + 1
    scores = set()
    for d in directions:
        neigh = (pos[0] + d[0], pos[1] + d[1])
        if 0 > neigh[0] or neigh[0] >= width or 0 > neigh[1] or neigh[1] >= height:
            continue
        if top_map[neigh]["height"] == target_height:
            sc = [(pos, x) for x in top_map[neigh]["score"]]
            scores.update(sc)
    return scores

def part_one(data: list[str]) -> Union[str, int]:
    width = len(data)
    height = len(data[0])
    top_map = to_map(data)
    for d in reversed(range(10)):
        for x in range(width):
            for y in range((height)):
                pos = (x, y)
                if d == 9 and top_map[pos]["height"] == d:
                    top_map[pos]["score"].add(pos)
                    continue
                if top_map[pos]["height"] == d:
                    top_map[pos]["score"].update(get_neigh_score(top_map, pos, width, height))
    return sum(len(x["score"]) for x in top_map.values() if x["height"] == 0) 

def part_two(data: list[str]) -> Union[str, int]:
    width = len(data)
    height = len(data[0])
    top_map = to_map(data)
    for d in reversed(range(10)):
        for x in range(width):
            for y in range((height)):
                pos = (x, y)
                if d == 9 and top_map[pos]["height"] == d:
                    top_map[pos]["score"].add(pos)
                    continue
                if top_map[pos]["height"] == d:
                    top_map[pos]["score"].update(get_neigh_trails(top_map, pos, width, height))
    return sum([len(x["score"]) for x in top_map.values() if x["height"] == 0])

def main():
    test_case_1 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""

    test = False
    day = 10
    if test:
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(day).strip().split("\n")


    print(f"day {day} part 1: {part_one(data)}")
    print(f"day {day} part 2: {part_two(data)}")


main()
