from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")
from collections import defaultdict
from statistics import variance


def get_robots(data: list[str]) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    robots = []
    for robot in data:
        pos = int(robot[robot.index("=") + 1 : robot.index(",")]), int(robot[robot.index(",") + 1 : robot.index(" ")])
        vel = int(robot[robot.rindex("=") + 1 : robot.rindex(",")]), int(robot[robot.rindex(",") + 1 :])
        robots.append((pos, vel))
    return robots


def part_one(data: list[str], width: int, height: int, seconds: int = 100) -> Union[str, int]:
    robots = get_robots(data)
    res: dict[tuple[int, int], int] = defaultdict(lambda: 0)
    for pos, vel in robots:
        res[((pos[0] + seconds * vel[0]) % width, (pos[1] + seconds * vel[1]) % height)] += 1

    total = 1
    total *= sum(res[(x, y)] for x in range(width // 2) for y in range(height // 2))
    total *= sum(res[(x, y)] for x in range(width // 2 + 1, width) for y in range(height // 2))
    total *= sum(res[(x, y)] for x in range(width // 2) for y in range(height // 2 + 1, height))
    total *= sum(res[(x, y)] for x in range(width // 2 + 1, width) for y in range(height // 2 + 1, height))
    return total


def draw_room(robots: dict[tuple[int, int], int], width, height, iteration):
    with open(f"day14drawings/{iteration:03}.txt", "w") as f:
        for y in range(height):
            line = ""
            for x in range(width):
                if robots[(x, y)] == 0:
                    line += " "
                else:
                    line += "■"
            f.write(line + "\n")


def old_old_part_two(data: list[str], width: int, height: int) -> Union[str, int]:
    min_sec = 0
    min_safety = float("inf")
    for s in range(width * height + 1):
        safety = part_one(data, width, height, s)
        if safety < min_safety:
            min_sec = s
            min_safety = safety
    return min_safety


def old_part_two(data: list[str], width: int, height: int) -> Union[str, int]:
    robots = get_robots(data)
    # for s in range(height):
    #    res: dict[tuple[int, int], int] = defaultdict(lambda: 0)
    #    for pos, vel in robots:
    #        res[((pos[0] + s * vel[0]) % width, (pos[1] + s * vel[1]) % height)] += 1
    # draw_room(res, width, height, s)
    # draw_room was used to find the magic numbers
    # 22s is width good
    # 98s is height good
    # 101x+22 = y
    # 103x+98 = y
    #
    # 103x+98 = 101x + 22
    # 103x - 101x + 98 - 98 = 101x - 101x + 22 - 98
    # 2x = -76 -> x = -38
    # 101(-38) + 22 = -3816
    # 103(-38) + 98 = -3816
    #
    # modular cycle, si etait il y a 3816 secondes, sera dans -3816 + lcm(101*103) = 6587
    res: dict[tuple[int, int], int] = defaultdict(lambda: 0)
    for pos, vel in robots:
        res[((pos[0] + 6587 * vel[0]) % width, (pos[1] + 6587 * vel[1]) % height)] += 1
    draw_room(res, width, height, 6587)
    return 6587


def part_two(data: list[str], width: int, height: int) -> Union[str, int]:
    robots = get_robots(data)
    min_x_s = 0
    min_x = float("inf")
    min_y_s = 0
    min_y = float("inf")
    for i in range(max(width, height)):
        res: dict[tuple[int, int], int] = defaultdict(lambda: 0)
        for pos, vel in robots:
            res[((pos[0] + i * vel[0]) % width, (pos[1] + i * vel[1]) % height)] += 1
        xs, ys = zip(*[(x, y) for (x, y), amount in res.items() if amount])
        if (x_var := variance(xs)) < min_x:
            min_x, min_x_s = x_var, i
        if (y_var := variance(ys)) < min_y:
            min_y, min_y_s = y_var, i

    # Here t = width * x + min_x_s and t = height * x + min_y_s
    # We can also generalize, because of the wraparound, with modulo arithmetics
    # t = min_x_s % width ->  t = min_x_s + width * k
    #
    # t = min_y_s % height
    # min_x_s + width * k = min_y_s % height
    # width * k = (min_y_s - min_x_s) % height
    # k = inverse(width) * (min_y_s - min_x_s) % height
    # t = min_x_s + (inverse(width) * (min_y_s - min_x_s) % height)*width
    tot = min_x_s + ((pow(width, -1, height) * (min_y_s - min_x_s)) % height) * width
    return tot


def main(test: bool = False):
    test_case_1 = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

    
    day = 14
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n")
        width = 11
        height = 7
    else:
        data = Day.get_data(2024, day).strip().split("\n")
        width = 101
        height = 103

    start = perf_counter()
    logger.info(f"day {day} part 1: {part_one(data, width, height)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"day {day} part 2: {part_two(data,  width, height)} in {perf_counter() - mid:.4f}s")
    logger.info(f"the whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main(True)
