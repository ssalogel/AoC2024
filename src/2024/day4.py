from time import perf_counter
from typing import Union

from src.utils import Day


def transpose(grid: list[str]) -> list[str]:
    return ["".join([grid[j][i] for j in range(len(grid))]) for i in range(len(grid))]


# \ diagonals
def backslash(grid: list[str]) -> list[str]:
    diags = []
    assert len(grid) == len(grid[0])
    for i in range(len(grid)):
        start_left = []
        start_top = []
        for j in range(len(grid)):
            if i + j == len(grid):
                break
            start_top.append(grid[j][i + j])
            start_left.append(grid[i + j][j])
        if i != 0:
            diags.append("".join(start_top))
        diags.append("".join(start_left))
    return diags


def forwardslash(grid: list[str]) -> list[str]:
    diags = []
    for i in reversed(range(len(grid))):
        start_right = []
        start_top = []
        for j in range(len(grid)):
            if i + j < len(grid):
                start_right.append(grid[i + j][len(grid) - 1 - j])
            if i - j >= 0:
                start_top.append(grid[j][len(grid) - 1 - i - j])
        if i != 0:
            diags.append("".join(start_top))
        diags.append("".join(start_right))
    return diags


def get_diags(grid: list[str]) -> list[str]:
    return backslash(grid) + forwardslash(grid)


def search_diag(grid: list[str], y, x, target) -> int:
    def search_dir(dy, dx):
        word = ""
        for i in range(len(target)):
            look_x, look_y = x + dx * i, y + dy * i
            if not (0 <= look_y < len(grid) and 0 <= look_x < len(grid[0])):
                return 0
            word += grid[look_y][look_x]
            if not target.startswith(word):
                return 0
            if word == target:
                return 1
        return 0

    dirs = (-1, -1), (-1, 1), (1, 1), (1, -1)
    return sum(search_dir(dy, dx) for dx, dy in dirs)


def part_one(data: list[str]) -> Union[str, int]:
    total = 0
    for elem in data + transpose(data):
        total += elem.count("XMAS")
        total += elem.count("SAMX")
    for y in range(len(data)):
        for x in range(len(data)):
            if data[y][x] == "X":
                total += search_diag(data, y, x, "XMAS")
    return total


def part_one_b(data: list[str]) -> Union[str, int]:
    total = 0
    for elem in data + transpose(data) + get_diags(data):
        total += elem.count("XMAS")
        total += elem.count("SAMX")
    return total


def part_two(data: list[str]) -> Union[str, int]:
    total = 0
    for y in range(1, len(data) - 1):
        for x in range(1, len(data) - 1):
            if data[y][x] == "A":
                if (
                    (data[y - 1][x - 1] == "S" and data[y + 1][x + 1] == "M")
                    or (data[y - 1][x - 1] == "M" and data[y + 1][x + 1] == "S")
                ) and (
                    (data[y + 1][x - 1] == "S" and data[y - 1][x + 1] == "M")
                    or (data[y + 1][x - 1] == "M" and data[y - 1][x + 1] == "S")
                ):
                    total += 1
    return total


def main():
    test_case_1 = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

    test = False
    day = 4
    if test:
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(day).strip().split("\n")

    start = perf_counter()
    print(f"day {day} part 1: {part_one_b(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    print(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    print(f"the whole day {day} took {perf_counter() - start:.4f}s")


main()
