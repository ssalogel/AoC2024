from typing import Union
from time import perf_counter
from src.utils import Day
from collections import defaultdict


def get_connections(data: list[str]) -> dict[str, set[str]]:
    res = defaultdict(lambda: set())
    for conn in data:
        a, b = conn.split("-")
        res[a].add(b)
        res[b].add(a)
    return res


def part_one(data: list[str]) -> Union[str, int]:
    connections = get_connections(data)
    triples = set()
    tested = set()
    for compA, conns in connections.items():
        pot_conns = list(conns.difference(tested))
        for i, compB in enumerate(pot_conns):
            for compC in pot_conns[i + 1 :]:
                if compC in connections[compB]:
                    triple = [compA, compB, compC]
                    triple.sort()
                    triples.add(tuple(triple))
        tested.add(compA)
    starts_with_t = lambda x, y, z: x[0] == "t" or y[0] == "t" or z[0] == "t"
    return sum([starts_with_t(*tri) for tri in triples])


def bron_kerbosh(graph: dict[str, set[str]], r=set(), p=None, x=set()) -> list[set[str]]:
    if p is None:
        p = set(graph.keys())
    if not p and not x:
        yield r
    else:
        u = next(iter(p.union(x)))
        for v in p.difference(graph[u]):
            yield from bron_kerbosh(graph, r=r.union({v}), p=p.intersection(graph[v]), x=x.intersection(graph[v]))
            p.remove(v)
            x.add(v)


def part_two(data: list[str]) -> Union[str, int]:
    connections = get_connections(data)
    cliques = list(bron_kerbosh(connections))
    max_clique = list(max(cliques, key=len))
    max_clique.sort()
    return ",".join(max_clique)


def main():
    test_case_1 = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

    test = False
    day = 23
    if test:
        print("TEST VALUES")
        data = test_case_1.strip().split("\n")
    else:
        data = Day.get_data(2024, day).strip().split("\n")

    start = perf_counter()
    print(f"day {day} part 1: {part_one(data)}  in {perf_counter() - start:.4f}s")
    mid = perf_counter()
    print(f"day {day} part 2: {part_two(data)} in {perf_counter() - mid:.4f}s")
    print(f"the whole day {day} took {perf_counter() - start:.4f}s")


if __name__ == "__main__":
    main()
