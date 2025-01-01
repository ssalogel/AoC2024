from time import perf_counter
from typing import Union
from math import log10, floor
from src.utils import Day
from collections import Counter


def step(stone: int, amount: int) -> dict[int, int]:
    if stone == 0:
        return {1: amount}
    stone_size = floor(log10(stone)) + 1
    if stone_size % 2 == 0:
        div, mod = divmod(stone, 10 ** (stone_size // 2))
        return {div: amount, mod: amount} if div != mod else {div: amount * 2}
    return {stone * 2024: amount}


def iterate(stones: Counter[int], amount: int) -> Counter[int]:
    for _ in range(amount):
        next_stones = Counter()
        for stone, amount in stones.items():
            next_stones.update(step(stone, amount))
        stones = next_stones
    return stones


def part_one(data: list[str]) -> Union[str, int]:
    stones = Counter(int(x) for x in data[0].split())
    return iterate(stones, 25).total()


def part_two(data: list[str]) -> Union[str, int]:
    stones = Counter([int(x) for x in data[0].split()])
    return iterate(stones, 75).total()


def main():
    test_case_1 = """125 17"""

    test = False
    day = 11
    if test:
        print("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2024, day).strip().split("\n")

    start = perf_counter()
    print(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    print(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    print(f"the whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    main()
