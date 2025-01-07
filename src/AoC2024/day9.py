from time import perf_counter
from typing import Union

from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def get_fs(data: list[str]) -> list[tuple[str, int]]:
    fs = []
    for ix, x in enumerate(data[0]):
        if ix % 2 != 0:
            fs.append((".", int(x)))
        else:
            fs.append((str(ix // 2), int(x)))
    return fs


def get_fs2(data: list[str]) -> list[str]:
    fs = []
    for ix, c in enumerate(data[0]):
        if ix % 2:
            [fs.append(".") for _ in range(int(c))]
        else:
            [fs.append(ix // 2) for _ in range(int(c))]
    return fs


def part_one(data: list[str]) -> Union[str, int]:
    fs = get_fs2(data)
    tail = len(fs) - 1
    for ix in range(len(fs)):
        if fs[ix] != "." or ix > tail:
            continue
        while tail > ix and fs[tail] == ".":
            tail -= 1
        fs[ix], fs[tail] = fs[tail], fs[ix]
        tail - 1

    return sum([ix * x for ix, x in enumerate(fs) if x != "."])


def part_two(data: list[str]) -> Union[str, int]:
    fs = get_fs(data)
    end = []
    while fs:
        to_place = fs.pop()
        if to_place[0] == ".":
            if to_place[1] > 0:
                end = [to_place] + end
            continue
        tpsize = to_place[1]
        for ix, elem in enumerate(fs):
            if elem[0] == ".":
                esize = elem[1]
                if esize == tpsize:
                    end = [fs[ix]] + end
                    fs[ix] = to_place
                    break
                elif esize > tpsize:
                    fs.remove(elem)
                    fs.insert(ix, (".", esize - tpsize))
                    fs.insert(ix, to_place)
                    end = [(".", tpsize)] + end
                    break
        else:
            end = [to_place] + end
    disk = []
    for iden, amnt in end:
        for _ in range(amnt):
            disk.append(int(iden) if iden != "." else ".")
    return sum([ix * x for ix, x in enumerate(disk) if x != "."])


def main(test: bool = False):
    test_case_1 = """2333133121414131402"""

    day = 9
    if test:
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2024, day).strip().split("\n")

    start = perf_counter()
    logger.info(f"\t\tday {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"\t\tday {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.warning(f"\tthe whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main(True)
