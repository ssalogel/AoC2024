from typing import Union
from math import log10, floor
from utils import Day
from collections import Counter

def step(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    stone_size = floor(log10(stone)) + 1
    if stone_size % 2 == 0:
        div, mod = divmod(stone, 10 ** (stone_size // 2))
        return [div, mod]
    return [stone * 2024]

def step2(stone: int, amount: int) -> dict[int, int]:
    if stone == 0:
        return {1: amount}
    stone_size = floor(log10(stone)) + 1
    if stone_size % 2 == 0:
        div, mod = divmod(stone, 10 ** (stone_size // 2))
        return {div: amount, mod: amount} if div != mod else {div: amount*2}
    return {stone * 2024: amount}



def part_one(data: list[str]) -> Union[str, int]:
    stones = [int(x) for x in data[0].split()]

    for _ in range(25):
        tmp = []
        for stone in stones:
            tmp.extend(step(stone))
        stones = tmp

    return len(stones)

def part_two(data: list[str]) -> Union[str, int]:
    stones2 = Counter([int(x) for x in data[0].split()])

    for _ in range(75):
        next_stones = Counter()
        for stone2, amount in stones2.items():
            next_stones.update(step2(stone2, amount))
        stones2 = next_stones
    return stones2.total()


def main():
    test_case_1 = """125 17"""

    test = False
    day = 11
    if test:
        print("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(day).strip().split("\n")


    print(f"day {day} part 1: {part_one(data)}")
    print(f"day {day} part 2: {part_two(data)}")


main()