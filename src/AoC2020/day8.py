from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


class Console:
    def __init__(self, code):
        self.past_instr = set()
        self.instr = []
        for instr in code:
            op = instr[: instr.index(" ")]
            operand = int(instr[instr.index(" ") + 1 :])
            self.instr.append((op, operand))
        self.pc = 0
        self.acc = 0

    def run_one(self) -> None:
        op, oper = self.instr[self.pc]
        self.past_instr.add(self.pc)
        match op:
            case "nop":
                self.pc += 1
            case "acc":
                self.acc += oper
                self.pc += 1
            case "jmp":
                self.pc += oper

    def loop_check(self) -> int:
        self.pc = 0
        self.past_instr = set()
        self.acc = 0
        while self.pc not in self.past_instr:
            self.run_one()
        return self.acc

    def fix_instrs(self):
        for ix, (op, oper) in enumerate(self.instr.copy()):
            if op == "acc":
                continue
            if op == "nop":
                self.instr[ix] = ("jmp", oper)
            else:
                self.instr[ix] = ("nop", oper)
            try:
                r = self.loop_check()
            except IndexError:
                return self.acc
            self.instr[ix] = (op, oper)


def part_one(data: list[str]) -> Union[str, int]:
    console = Console(data)
    return console.loop_check()


def part_two(data: list[str]) -> Union[str, int]:
    console = Console(data)
    return console.fix_instrs()


def main(test: bool = False):
    test_case_1 = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

    day = 8
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

    return perf_counter() - start


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
