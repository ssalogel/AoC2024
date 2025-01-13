from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

from src.utils.IntCode import IntCode

logger = logging.getLogger("AoC")


def build_picture(data: list[str]) -> tuple[tuple[complex, str], set[complex]]:
    computer = IntCode([int(x) for x in data[0].split(",")])
    computer.run_until_end()
    screen = set()
    robot = -1
    row = 0
    col = 0
    for c in computer.output:
        c = chr(c)
        if c == "\n":
            row += 1
            col = 0
            continue
        if c != ".":
            screen.add(col + 1j * row)
        if c not in ".#":
            direction = c
            robot = col + 1j * row
        col += 1
    return (robot, direction), screen


def draw(path: set[complex], robot: tuple[complex, str]) -> None:
    width = int(max(x.real for x in path))
    length = int(max(x.imag for x in path))
    for y in range(length + 1):
        row = []
        for x in range(width + 1):
            pos = x + 1j * y
            if pos == robot[0]:
                row.append(robot[1])
                continue
            if pos in path:
                row.append("█")
                continue
            row.append(" ")

        logger.debug("".join(row))

# via looking at the input: one long path that loops a bit.
# viable looking strat: going straight as much as possible, and turning when forced
# if no new direction: path has ended
def find_path(path: set[complex], pos: complex, direction: complex) -> list[str]:
    res = []
    while True:
        c = 0
        while pos + direction in path:
            pos += direction
            c += 1
        if c:
            res.append(str(c))
        if pos + (direction * -1j) in path:
            res.append("L")
            direction *= -1j
            continue
        elif pos + (direction * 1j) in path:
            res.append("R")
            direction *= 1j
        else:
            break
    return res

def part_one(data: list[str]) -> Union[str, int]:
    _, path = build_picture(data)
    crossings = []
    for point in path:
        up = point - 1j
        right = point + 1
        down = point + 1j
        left = point - 1
        if all(map(lambda p: p in path, [up, right, down, left])):
            crossings.append(point)

    return sum(int(x.real * x.imag) for x in crossings)


def compress_path(path: list[str]) -> tuple[str, str, str]:
    #max length authorized is 20 char, including separating commas, so 9 commas for 10 args, with one arg being 2 chars
    for len_a in range(2, 11):
        func_a = path[:len_a]
        if len(','.join(func_a)) > 20:
            continue
        start_b = len_a
        while path[start_b:len_a + start_b] == func_a:
            start_b += len_a
        for len_b in range(2, 11):
            func_b = path[start_b:start_b + len_b]
            if len(','.join(func_b)) > 20:
                continue
            start_c = start_b + len_b
            while True:
                if path[start_c:start_c + len_a] == func_a:
                    start_c += len_a
                elif path[start_c:start_c + len_b] == func_b:
                    start_c += len_b
                else:
                    break
            for len_c in range(2, 11):
                func_c = path[start_c:start_c + len_c]
                if len(','.join(func_c)) > 20:
                    continue
                finished = True
                ix = start_c + len_c
                while ix < len(path):
                    if path[ix:ix + len_a] == func_a:
                        ix += len_a
                    elif path[ix:ix + len_b] == func_b:
                        ix += len_b
                    elif path[ix:ix + len_c] == func_c:
                        ix += len_c
                    else:
                        finished = False
                        break

                if finished:
                    return ','.join(func_a), ','.join(func_b), ','.join(func_c)


def part_two(data: list[str]) -> Union[str, int]:
    robot, level = build_picture(data)
    directions = {"^": -1j, "v": 1j, "<": -1, ">": 1}
    draw(level, robot)
    robot, direction = robot[0], directions[robot[1]]
    path = find_path(level, robot, direction)
    A, B, C = compress_path(path)
    path = ",".join(path).replace(A, "A").replace(B, "B").replace(C, "C")
    computer = IntCode([int(x) for x in data[0].split(",")])
    computer.code[0] = 2
    computer.add_inputs(map(ord, path + "\n"))
    computer.add_inputs(map(ord, A + "\n"))
    computer.add_inputs(map(ord, B + "\n"))
    computer.add_inputs(map(ord, C + "\n"))
    computer.add_inputs(map(ord, "n\n"))
    computer.run_until_end()
    return computer.output.pop()

def main(test: bool = False):
    test_case_1 = """"""

    day = 17
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
