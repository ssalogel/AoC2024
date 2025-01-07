import re
from functools import cache
from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def parse_rules(inp: list[str]) -> dict[
    int,
    list[
        tuple[int,]
        | tuple[
            int,
            int,
        ]
        | tuple[int, int, int]
    ]
    | str,
]:
    rules = {}
    for line in inp:
        num, options = line.split(": ")
        num = int(num)
        if '"' in options:
            rule = options[1:-1]
        else:
            rule = []
            for option in options.split("|"):
                rule.append(tuple(map(int, option.split())))
        rules[num] = rule
    return rules


def part_one(data: list[str]) -> Union[str, int]:
    rules = parse_rules(data[0].split("\n"))

    # rule default rule is 0 by def, since the question is "which answers fit the rule 0"
    @cache
    def build_regex(rule_num: int = 0):
        rule = rules[rule_num]
        if type(rule) is str:
            return rule
        options = []
        for option in rule:
            r = ""
            for sub_rule in option:
                r += build_regex(sub_rule)
            options.append(r)
        return "(" + "|".join(options) + ")"

    regex = build_regex()
    pattern = re.compile(regex)
    res = [re.fullmatch(pattern, x) is not None for x in data[1].split("\n")]
    return sum(res)


def part_two(data: list[str]) -> Union[str, int]:
    rules = parse_rules(data[0].split("\n"))
    rules[8] = [(42,), (42, 8)]
    rules[11] = [(42, 31), (42, 11, 31)]

    # special rules : top of the tree can be cyclic:
    # 0: 8 11
    # 8: 42 | 42 8
    # 11: 42 31 | 42 11 31
    #
    # 8 and 11 aren't anywhere else in the input
    #
    # pattern is therefore 42 * x + 31 * y where x > y
    @cache
    def match(string: str, rule_num=0, index=0) -> list[int]:
        if index >= len(string):
            return []

        rule = rules[rule_num]
        if type(rule) is str:
            if string[index] == rule:
                return [index + 1]
            return []

        matches = []
        for option in rule:
            sub_match = [index]
            for sub_rule in option:
                new_match = []
                for idx in sub_match:
                    new_match += match(string, sub_rule, idx)
                sub_match = new_match
            matches += sub_match
        return matches

    return sum([len(x) in match(x) for x in data[1].split("\n")])


def main(test: bool = False):
    test_case_1 = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

aaabbbbbbaaaabaababaabababbabaaabbababababaaa
abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""

    day = 19
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n\n")
    else:
        data = Day.get_data(2020, day).strip().split("\n\n")

    start = perf_counter()
    logger.info(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    logger.info(f"the whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main()
