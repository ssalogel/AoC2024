from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")

def get_wire_positions(wire: list[tuple[str, int]]) -> dict[complex, int]:
    positions = {}
    pos = c = 0
    directions = {"R": 1, "D": -1j, "L": -1, "U": 1j}
    for d, amnt in wire:
        for _ in range(amnt):
            c += 1
            pos += directions[d]
            if pos in positions:
                continue
            positions[pos] = c
    if 0 in positions: positions.pop(0)
    return positions

def part_one(data: list[str]) -> Union[str, int]:
    wires = []
    for w in data:
        wires.append(get_wire_positions([(instr[0], int(instr[1:])) for instr in w.split(",")]))
    crosses = set(wires[0]).intersection(wires[1])
    return min(int(abs(x.imag) + abs(x.real)) for x in crosses)


def part_two(data: list[str]) -> Union[str, int]:
    wires = []
    for w in data:
        wires.append(get_wire_positions([(instr[0], int(instr[1:])) for instr in w.split(",")]))
    crosses = set(wires[0]).intersection(wires[1])
    return min(wires[0][x] + wires[1][x] for x in crosses)


def main(test: bool = False):
    test_case_1 = """"""

    day = 3
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
