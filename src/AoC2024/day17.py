from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def adv(operand: int):
    registers["A"] //= 2 ** combo[operand]()
    registers["pointer"] += 2


def bxl(operand: int):
    registers["B"] ^= operand
    registers["pointer"] += 2


def bst(operand: int):
    registers["B"] = combo[operand]() % 8
    registers["pointer"] += 2


def jnz(operand: int):
    if registers["A"]:
        registers["pointer"] = operand
    else:
        registers["pointer"] += 2


def bxc(operand: int):
    registers["B"] ^= registers["C"]
    registers["pointer"] += 2


def out(operand: int):
    output.append(combo[operand]() % 8)
    registers["pointer"] += 2


def bdv(operand: int):
    registers["B"] = registers["A"] // 2 ** combo[operand]()
    registers["pointer"] += 2


def cdv(operand: int):
    registers["C"] = registers["A"] // 2 ** combo[operand]()
    registers["pointer"] += 2


operation = {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}

registers = {"A": 0, "B": 0, "C": 0, "pointer": 0}

combo = {
    0: (lambda: 0),
    1: (lambda: 1),
    2: (lambda: 2),
    3: (lambda: 3),
    4: (lambda: registers["A"]),
    5: (lambda: registers["B"]),
    6: (lambda: registers["C"]),
}

output = []


def part_one(data: list[str]) -> Union[str, int]:
    regs, instr = data
    registers.update({chr(i + ord("A")): int(r[r.index(":") + 2 :]) for i, r in enumerate(regs.split("\n"))})
    instr = [int(x) for x in instr[9:].split(",")]

    while registers["pointer"] < len(instr):
        operation[instr[registers["pointer"]]](instr[registers["pointer"] + 1])

    return ",".join(str(x) for x in output)


"""
Program: 2,4,1,5,7,5,1,6,0,3,4,2,5,5,3,0
2,4 -> B = A % 8
1,5 -> B = B ^ 5  (101)
7,5 -> C = A // B
1,6 -> B = B ^ 6  (110)
0,3 -> A = A // 8
4,2 -> B = B ^ C
5,5 -> out(B % 8)
3,0 -> jmp 0 if A != 0


"""


def part_two(data: list[str]) -> Union[str, int]:
    _, instr = data
    instr = [int(x) for x in instr[9:].split(",")]
    target = ",".join(str(x) for x in instr)
    new_start = [0]
    for p in range(len(instr)):
        new_start, a = [], new_start
        for t in a:
            for i in range(8):
                global output
                output = []
                start_value = i + (t << 3)
                registers["A"] = start_value
                registers["pointer"] = 0
                while registers["pointer"] < len(instr):
                    operation[instr[registers["pointer"]]](instr[registers["pointer"] + 1])
                if target.endswith(",".join(str(x) for x in output)):
                    new_start.append(start_value)

    return min(new_start)


def main(test: bool = False):
    test_case_1 = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

    
    day = 17
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n\n")
    else:
        data = Day.get_data(2024, day).strip().split("\n\n")

    start = perf_counter()
    logger.info(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.info(f"the whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main(True)
