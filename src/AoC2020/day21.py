from collections import defaultdict, Counter
from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def get_allergens_possible_translations(data: list[str]) -> tuple[dict[str, set[str]], Counter[str]]:
    allergens_translation = {}
    amount = Counter()
    for line in data:
        unknowns, allergens = line.replace(")", "").split(" (contains ", 1)
        unknowns = set(unknowns.split(" "))
        amount.update(unknowns)
        allergens = allergens.split(", ")
        for allergen in allergens:
            if allergen not in allergens_translation:
                allergens_translation[allergen] = unknowns.copy()
            else:
                allergens_translation[allergen].intersection_update(unknowns)
    return allergens_translation, amount


def part_one(data: list[str]) -> Union[str, int]:
    allergens_translation, amount = get_allergens_possible_translations(data)
    know_unknown_words = set(amount.keys())
    for v in allergens_translation.values():
        know_unknown_words.difference_update(v)
    return sum(amount[c] for c in know_unknown_words)

def part_two(data: list[str]) -> Union[str, int]:
    allergens_translation, _ = get_allergens_possible_translations(data)
    translated = set()
    while len(translated) < len(allergens_translation):
        for word, translations in allergens_translation.items():
            if len(translations) == 1:
                translated |= translations
                continue
            allergens_translation[word] -= translated
    solution = [(w, t.pop()) for w,t in allergens_translation.items()]
    solution.sort()
    return ','.join([t for _,t in solution])





def main(test: bool = False):
    test_case_1 = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

    day = 21
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
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
