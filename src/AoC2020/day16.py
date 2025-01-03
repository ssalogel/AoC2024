from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from math import prod

logger = logging.getLogger("AoC")

type Category = tuple[str, list[int]]
type Ticket = list[int]

def get_categories(cats: list[str]) -> list[Category]:
    categories = []
    for c in cats:
        name = c[:c.index(":")]
        constraint1 = c[c.index(":")+2:c.index(" or")]
        lim_min_1 = int(constraint1[:constraint1.index("-")])
        lim_max_1 = int(constraint1[constraint1.index("-")+1:])
        constraint2 = c[c.rindex(" ") + 1:]
        lim_min_2 = int(constraint2[:constraint2.index("-")])
        lim_max_2 = int(constraint2[constraint2.index("-")+1:])
        categories.append((name, set(range(lim_min_1, lim_max_1 + 1)).union(set(range(lim_min_2, lim_max_2 + 1)))))
    return categories

def parse_data(data: list[str]) -> tuple[list[Category], Ticket, list[Ticket]]:
    cats = data[0].split("\n")
    categories = get_categories(cats)
    ticket = [int(x) for x in data[1].split("\n")[1].split(",")]
    tickets = [[int(e) for e in x.split(",")] for x in data[2].split("\n")[1:]]
    return categories, ticket, tickets


def part_one(data: list[str]) -> Union[str, int]:
    cats, _, tickets = parse_data(data)
    acceptable_numbers = set()
    for _, valids in cats:
        acceptable_numbers.update(valids)
        acceptable_numbers.update(valids)
    tot = 0
    for ticket in tickets:
        for n in ticket:
            if n not in acceptable_numbers:
                tot += n
    return tot


def part_two(data: list[str]) -> Union[str, int]:
    cats, my_ticket, tickets = parse_data(data)
    acceptable_numbers = set()
    for _, valids in cats:
        acceptable_numbers.update(valids)
        acceptable_numbers.update(valids)
    valid = []
    for ticket in tickets:
        for n in ticket:
            if n not in acceptable_numbers:
                break
        else:
            valid.append(ticket)
    potentials = [[True for c,_ in cats] for _ in cats]
    for ticket in valid:
        for ix, m in enumerate(ticket):
            for jx, cat in enumerate(cats):
                if m not in cat[1]:
                    potentials[jx][ix] = False
    solution = {}
    while True:
        if len(solution) == len(cats):
            break
        for i in range(len(potentials)):
            if potentials[i][0] in solution:
                continue
            if sum(potentials[i]) == 1:
                pos = potentials[i].index(True)
                solution[cats[i][0]] = pos
                for ix, p in enumerate(potentials):
                    if ix != i:
                        p[pos] = False

    answer = []
    for c, p in solution.items():
        answer.append((c, my_ticket[p]))
    return prod(n for name, n in answer if name.startswith("departure"))


def main(test: bool = False):
    test_case_1 = """class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""

    day = 16
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
