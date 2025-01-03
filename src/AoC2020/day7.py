from typing import Union
from time import perf_counter

from functools import cache

from src.utils import Day
import sys
import logging
from collections import defaultdict

logger = logging.getLogger("AoC")


def parse_bags(data: list[str]) -> tuple[dict[str, list[str]], dict[str, list[tuple[int, str]]]]:
    is_contained = defaultdict(list)
    containers = defaultdict(list)
    for line in data:
        container, contains = line.replace(".", "").replace("bags", "bag").split(" contain ")
        contains = contains.split(", ")
        if contains == ["no other bag"]:
            continue
        for contain in contains:
            num = int(contain[: contain.index(" ")])
            bag = contain[contain.index(" ") + 1 :]
            is_contained[bag].append(container)
            containers[container].append((num, bag))
    return is_contained, containers


def part_one(data: list[str]) -> Union[str, int]:
    contain, _ = parse_bags(data)
    target = "shiny gold bag"
    to_visit = [target]
    containers = set()
    while to_visit:
        curr = to_visit.pop()
        if curr in containers:
            continue
        containers.add(curr)
        for holder in contain[curr]:
            to_visit.append(holder)
    return len(containers) - 1


def part_two(data: list[str]) -> Union[str, int]:
    _, rules = parse_bags(data)
    target = "shiny gold bag"

    @cache
    def calculate_number_bags(bag: str) -> int:
        return sum(x * calculate_number_bags(y) + x for x, y in rules[bag])

    return calculate_number_bags(target)


def main(test: bool = False):
    test_case_1 = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""
    test_case_2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

    day = 7
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
        data = test_case_2.strip().split("\n")
    else:
        data = Day.get_data(2020, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.info(f"the whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
