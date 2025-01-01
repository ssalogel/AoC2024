from typing import Union
from time import perf_counter

from src.utils import Day
import sys
import logging

logger = logging.getLogger("AoC")


def part_one(data: list[str]) -> Union[str, int]:
    start, conns = data
    wires = []
    values = {}
    for value in start.split("\n"):
        values[value[: value.index(":")]] = int(value[-1])
    conns = conns.split("\n")
    for conn in conns:
        op, out = conn.split(" -> ")
        op1, op2, op3 = op.split()
        wires.append((op1, op2, op3, out))
    while wires:
        for op1, meth, op2, out in iter(wires):
            if op1 in values and op2 in values:
                if meth == "OR":
                    values[out] = values[op1] | values[op2]
                elif meth == "AND":
                    values[out] = values[op1] & values[op2]
                elif meth == "XOR":
                    values[out] = values[op1] ^ values[op2]
                else:
                    raise NotImplementedError
                wires.remove((op1, meth, op2, out))
    out_values = [v for v in values if v.startswith("z")]
    out_values.sort()
    res = 0
    for v in reversed(out_values):
        res = res << 1
        res += values[v]
    return res


def part_two(data: list[str]) -> Union[str, int]:
    _, conns = data
    wires = {}
    for conn in conns.split("\n"):
        op, out = conn.split(" -> ")
        op1, op2, op3 = op.split()
        wires[out] = (op1, op2, op3)

    valid_trees = []

    # pattern
    # zAB where AB > 1
    # ABR1 XOR ABR2 -> zAB
    # XAB XOR YAB -> ABR1
    # ABR3 OR ABP4 -> ABR2
    # AAR1 AND AAR2 -> ABR3
    # XAA AND YAA -> ABR4

    # Z01 R1 and R2
    valid = ("fps", "rfg")
    zaa = "z01"
    for n in range(2, 46):
        zab = f"z{n:02}"
        abr1, op, abr2 = wires[zab]

    pass


def get_parent_rules(rules, target, depth=3):
    if depth == 0:
        return []
    if target.startswith("x") or target.startswith("y"):
        return []
    a, op, b = rules[target]
    out = [f"{a} {op} {b} -> {target}"]
    out += get_parent_rules(rules, a, depth - 1)
    out += get_parent_rules(rules, b, depth - 1)
    return out


def part_two_manual(data):
    _, conns = data
    wires = {}
    for conn in conns.split("\n"):
        op, out = conn.split(" -> ")
        op1, op2, op3 = op.split()
        wires[out] = (op1, op2, op3)

    outputs = []

    for n in range(2, 46):
        wire = f"z{n:02}"
        outputs.append(get_parent_rules(wires, wire))

    with open("../../wiresScrambled.txt", "w") as f:
        for output in outputs:
            f.writelines("\n".join(output))
            f.write("\n\n")


def main(test: bool = False):
    test_case_1 = """

x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""

    
    day = 24
    if test:
        logger.info("TEST VALUES")
        data = test_case_1.strip().split("\n\n")
    else:
        data = Day.get_data(2024, day).strip().split("\n\n")

    start = perf_counter()
    logger.info(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    logger.info(f"day {day} part 2: {part_two_manual(data)} in {perf_counter() - mid:.4f}s")
    logger.info(f"the whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    logging.basicConfig(level=logging.NOTSET, stream=sys.stdout)
    main(True)
