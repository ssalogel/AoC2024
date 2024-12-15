from typing import Union
from time import perf_counter
from utils import Day


def move(grid, start, direction) -> tuple[bool, tuple[int, int]]:
    new_x = start[0] + direction[0]
    new_y = start[1] + direction[1]
    if grid[new_y][new_x] == "#":
        return False, start
    if grid[new_y][new_x] in "O[]":
        if not move(grid, (new_x, new_y), direction)[0]:
            return False, start
    if grid[new_y][new_x] == ".":
        grid[new_y][new_x] = grid[start[1]][start[0]]
        grid[start[1]][start[0]] = "."
        return True, (new_x, new_y)


def move_vert(grid, start: list[tuple[int, int]], direction) -> tuple[bool, list[tuple[int, int]]]:
    new_xys = [(x + direction[0], y + direction[1]) for x, y in start]
    if any(map(lambda pos: grid[pos[1]][pos[0]] == "#", new_xys)):
        return False, start
    ## handle boxes
    if any(map(lambda pos: grid[pos[1]][pos[0]] in "[]", new_xys)):
        boxes = set()
        for x, y in new_xys:
            if grid[y][x] == "]":
                boxes.add((x, y))
                boxes.add((x - 1, y))
            elif grid[y][x] == "[":
                boxes.add((x, y))
                boxes.add((x + 1, y))
        if not move_vert(grid, list(boxes), direction)[0]:
            return False, start
    if all(map(lambda pos: grid[pos[1]][pos[0]] == ".", new_xys)):
        for i, (x, y) in enumerate(new_xys):
            grid[y][x] = grid[start[i][1]][start[i][0]]
            grid[start[i][1]][start[i][0]] = "."
        return True, list(new_xys)
    return True, list(new_xys)


def part_one(data: list[str]) -> Union[str, int]:
    moves = data[1].replace("\n", "")
    grid = [list(x) for x in data[0].split("\n")]

    robot = (0, 0)
    for y, row in enumerate(grid):
        if "@" in row:
            robot = (row.index("@"), y)

    for action in moves:
        if action == "<":
            _, robot = move(grid, robot, (-1, 0))
        elif action == "^":
            _, robot = move(grid, robot, (0, -1))
        elif action == ">":
            _, robot = move(grid, robot, (1, 0))
        elif action == "v":
            _, robot = move(grid, robot, (0, 1))
        else:
            raise NotImplementedError

    return sum([x + 100 * y for y, row in enumerate(grid) for x, c in enumerate(row) if c == "O"])


def part_two(data: list[str]) -> Union[str, int]:
    moves = data[1].replace("\n", "")
    grid = [
        list(x.replace("#", "##").replace("O", "[]").replace(".", "..").replace("@", "@.")) for x in data[0].split("\n")
    ]

    robot = (0, 0)
    for y, row in enumerate(grid):
        if "@" in row:
            robot = (row.index("@"), y)
    for action in moves:
        if action == "<":
            _, robot = move(grid, robot, (-1, 0))
        elif action == "^":
            _, robot = move_vert(grid, [robot], (0, -1))
            robot = robot.pop()
        elif action == ">":
            _, robot = move(grid, robot, (1, 0))
        elif action == "v":
            _, robot = move_vert(grid, [robot], (0, 1))
            robot = robot.pop()
        else:
            raise NotImplementedError

    return sum([x + 100 * y for y, row in enumerate(grid) for x, c in enumerate(row) if c == "["])


def main():
    test_case_1 = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

    test = False
    day = 15
    if test:
        print("TEST VALUES")
        data = test_case_1.strip().split("\n\n")
    else:
        data = Day.get_data(day).strip().split("\n\n")

    start = perf_counter()
    print(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    print(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    print(f"the whole day {day} took {perf_counter() - start:.4f}s")


main()
