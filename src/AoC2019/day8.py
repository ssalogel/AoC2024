from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def part_one(data: list[str], width: int, height: int) -> Union[str, int]:
    data = data[0]
    size = width * height
    image = []
    best_img = 0
    best_score = len(data)
    for layer in range(len(data) // size):
        layer_px = data[layer * size : (layer + 1) * size]
        image.append(layer_px)
        if layer_px.count("0") < best_score:
            best_img = layer
            best_score = layer_px.count("0")
    return image[best_img].count("1") * image[best_img].count("2")


def part_two(data: list[str], width: int, height: int) -> Union[str, int]:
    data = data[0]
    size = width * height
    image: list = [None] * size
    for layer in range(len(data) // size):
        layer_px = data[layer * size : (layer + 1) * size]
        for ix, c in enumerate(layer_px):
            if image[ix] is not None or c == "2":
                continue
            image[ix] = c
    for i in range(height):
        logger.debug("".join(image[i * width : (i + 1) * width]).replace("0", " ").replace("1", "█"))
    return image


def main(test: bool = False):
    test_case_1 = """0222112222120000"""

    day = 8
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
        width = 2
        height = 2
    else:
        data = Day.get_data(2019, day).strip().split("\n")
        width = 25
        height = 6

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data, width, height)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"\t\tday {day} part 2: {part_two(data, width, height)} in {perf_counter() - mid:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")

    return perf_counter() - start


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
