from collections import defaultdict
from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging
from math import lcm


logger = logging.getLogger("AoC")


type Ingredient = tuple[int, str]
type Recipe = tuple[int, list[Ingredient]]


def parse_recipes(data: list[str]) -> dict[str, Recipe]:
    production = {}
    for line in data:
        ingredients, product = line.split(" => ", 2)
        ingredients = ingredients.split(", ")
        product = int(product[: product.index(" ")]), product[product.index(" ") + 1 :]
        production[product[1]] = (product[0], [])
        for ingr in ingredients:
            num = int(ingr[: ingr.index(" ")])
            name = ingr[ingr.index(" ") + 1 :]
            production[product[1]][1].append((num, name))
    return production


def produce(inventory: dict[str, int], recipe_book: dict[str, Recipe], target: str, qty: int) -> dict[str, int]:
    if target == "ORE":
        inventory["ORE"] += qty
        return inventory
    if qty <= 0:
        return inventory

    recipe_w, recipes = recipe_book[target]
    n_rec = (qty // recipe_w) + (qty % recipe_w != 0)

    for amnt, ingredient in recipes:
        qty_tot = (n_rec * amnt) - inventory[ingredient] if ingredient != "ORE" else n_rec * amnt
        inventory = produce(inventory, recipe_book, ingredient, qty_tot)
        inventory[ingredient] -= n_rec * amnt if ingredient != "ORE" else 0
    inventory[target] += n_rec * recipe_w
    return inventory


def part_one(data: list[str]) -> Union[str, int]:
    recipes = parse_recipes(data)
    inventory = defaultdict(lambda: 0)
    inventory = produce(inventory, recipes, "FUEL", 1)
    return inventory["ORE"]


def part_two(data: list[str]) -> Union[str, int]:
    recipes = parse_recipes(data)
    AV_ORE = 10**12
    ceil = AV_ORE // part_one(data)
    while True:
        inventory = defaultdict(lambda: 0)
        inventory = produce(inventory, recipes, "FUEL", ceil)
        if inventory["ORE"] < AV_ORE:
            ceil *= 2
        else:
            break

    hi = ceil
    low = ceil // 2

    while hi - low > 1:
        pivot = (hi + low) // 2
        inventory = defaultdict(lambda: 0)
        inventory = produce(inventory, recipes, "FUEL", pivot)
        if inventory["ORE"] > AV_ORE:
            hi = pivot
        else:
            low = pivot

    return low


def main(test: bool = False):
    test_case_1 = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX"""

    day = 14
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
