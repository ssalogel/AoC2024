from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def get_mask(mask: str) -> tuple[int, int]:
    mask_and = mask[7:]
    mask_or = mask[7:]
    mask_and = int(mask_and.replace("X", "1"), 2)
    mask_or = int(mask_or.replace("X", "0"), 2)
    return mask_and, mask_or


def part_one(data: list[str]) -> Union[str, int]:
    res = {}
    for instr in data:
        if instr.startswith("mask"):
            mask_and, mask_or = get_mask(instr)
        else:
            reg = int(instr[instr.index("[") + 1 : instr.index("]")])
            value = int(instr[instr.index("=") + 2 :])
            value &= mask_and
            value |= mask_or
            res[reg] = value
    return sum(res.values())


def get_all_addresses(mask: str, reg: int) -> list[int]:
    reg_b = bin(reg)[2:].rjust(36, "0")
    res = [[] for _ in range(2 ** mask.count("X"))]
    c = 0
    for r, m in zip(reg_b, mask):
        if m != "X":
            for l in res:
                l.append(r)
            continue
        c += 1
        e = "1"
        switch = 2 ** (mask.count("X") - c)
        for i, l in enumerate(res):
            if i % switch == 0:
                e = "1" if e == "0" else "0"
            l.append(e)
    return res


def part_two(data: list[str]) -> Union[str, int]:
    res = {}
    for instr in data:
        if instr.startswith("mask"):
            mask = instr[7:]
            _, mask_or = get_mask(instr)
        else:
            regs = get_all_addresses(mask, int(instr[instr.index("[") + 1 : instr.index("]")]))
            value = int(instr[instr.index("=") + 2 :])
            for reg in regs:
                reg = int("".join(reg), 2) | mask_or
                res[reg] = value
    return sum(res.values())


def main(test: bool = False):
    test_case_1 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""

    day = 14
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


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
