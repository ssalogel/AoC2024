from typing import Union, Iterable
from time import perf_counter
from src.utils import Day
import sys
import logging
from IntCode import IntCode, State
from itertools import permutations


logger = logging.getLogger("AoC")


def part_one(data: list[str]) -> Union[str, int]:
    code = list(map(int, data[0].split(",")))
    c1, c2, c3, c4, c5 = IntCode(code), IntCode(code), IntCode(code), IntCode(code), IntCode(code)
    best = -999_999_999
    for n1, n2, n3, n4, n5 in permutations(range(5)):
        out1 = c1.reset().add_inputs((n1, 0)).run_until_end().output.pop()
        out2 = c2.reset().add_inputs((n2, out1)).run_until_end().output.pop()
        out3 = c3.reset().add_inputs((n3, out2)).run_until_end().output.pop()
        out4 = c4.reset().add_inputs((n4, out3)).run_until_end().output.pop()
        out5 = c5.reset().add_inputs((n5, out4)).run_until_end().output.pop()
        if out5 > best:
            best = out5
    return best


def part_two(data: list[str]) -> Union[str, int]:
    code = list(map(int, data[0].split(",")))
    comps: list[IntCode] = [IntCode(code), IntCode(code), IntCode(code), IntCode(code), IntCode(code)]
    best = -999_999_999
    for n1, n2, n3, n4, n5 in permutations(range(5, 10)):
        seeded = False
        for c in comps:
            c.reset()
        comps[0].add_input(n1)
        comps[1].add_input(n2)
        comps[2].add_input(n3)
        comps[3].add_input(n4)
        comps[4].add_input(n5)
        while comps[-1].state != State.DONE:
            for i, comp in enumerate(comps):
                if not seeded:
                    comp.add_input(0)
                    seeded = True
                else:
                    comp.add_input(comps[i - 1].output.popleft())
                comp.run_until_end()
        curr = comps[-1].output.popleft()
        if curr > best:
            best = curr
    return best


def main(test: bool = False):
    test_case_1 = """3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"""

    day = 7
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
