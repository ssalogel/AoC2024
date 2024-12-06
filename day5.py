from typing import Union

from utils import Day

def respect_all_rules(rules, update):
    forbidden = set()
    for num in reversed(update):
        if num in forbidden:
            return False
        for rule in rules:
            if num == rule[0]:
                forbidden.add(rule[1])

    return True

def reorder(rules, update):
    while not respect_all_rules(rules, update):
        moved = False
        for ix in range(len(update)):
            for comp in range(ix+1, len(update)):
                for rule in rules:
                    if update[ix] == rule[1] and update[comp] == rule[0]:
                        update = update[:ix] + update[ix+1:comp+1] + [update[ix]] + update[comp+1:]
                        moved = True
                        break
    return update

def part_one(rules: list[str], updates: list[str]) -> Union[str, int]:
    total = 0
    rules = [(int(rule.split('|')[0]), int(rule.split('|')[1])) for rule in rules.split()]
    updates = [[int(x) for x in update.split(',')] for update in updates.split()]
    for update in updates:
        if respect_all_rules(rules, update):
            total += update[len(update)//2]
    return total


def part_two(rules: list[str], updates: list[str]) -> Union[str, int]:
    total = 0
    rules = [(int(rule.split('|')[0]), int(rule.split('|')[1])) for rule in rules.split()]
    updates = [[int(x) for x in update.split(',')] for update in updates.split()]
    for ix, update in enumerate(updates):
        print(ix, '/', len(updates)-1)
        if not respect_all_rules(rules, update):
            total += reorder(rules, update)[len(update) // 2]
    return total


def main():
    test = False

    test_case_1 = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""

    day = 5
    if test:
        data = test_case_1.strip().split("\n\n")
    else:
        data = Day.get_data(day).strip().split("\n\n")


    print(f"day {day} part 1: {part_one(*data)}")
    print(f"day {day} part 2: {part_two(*data)}")


main()