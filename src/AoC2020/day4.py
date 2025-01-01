from pickletools import stringnl_noescape
from typing import Union
from time import perf_counter
from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")

def is_hex(string: str) -> bool:
    return all(map(lambda x: x.lower() in "abcdef" or x.isnumeric, string))

def is_valid_height(string: str) -> bool:
    if string.endswith("cm"):
        num = int(string[:-2])
        return 150 <= num <= 193
    if string.endswith("in"):
        num = int(string[:-2])
        return 59 <= num <= 76
    return False

def part_one(data: list[str]) -> Union[str, int]:
    tot = 0
    passports = [x.split() for x in data]
    needed_keys = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    for passport in passports:
        keys = {x[:3] for x in passport}
        tot += len(needed_keys.intersection(keys)) == len(needed_keys)
    return tot

def part_two(data: list[str]) -> Union[str, int]:
    tot = 0
    passports = [x.split() for x in data]
    needed_keys = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
    for passport in passports:
        values = dict((x[:3], x[4:]) for x in passport)
        if len(needed_keys.intersection(set(values.keys()))) == len(needed_keys):
            valid = True
            valid &= 1920 <= int(values["byr"]) <= 2002
            valid &= 2010 <= int(values["iyr"]) <= 2020
            valid &= 2020 <= int(values["eyr"]) <= 2030
            valid &= is_valid_height(values["hgt"])
            valid &= values["hcl"][0] == "#" and is_hex(values["hcl"][1:])
            valid &= values["ecl"] in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")
            valid &= values["pid"].isnumeric() and len(values["pid"]) == 9
            tot += valid

    return tot


def main(test: bool = False):
    test_case_1 = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in

pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719

eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""

    
    day = 4
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
    main(True)
