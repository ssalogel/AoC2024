from utils import Day
from collections import Counter

test_case_1 = """3   4
4   3
2   5
1   3
3   9
3   3"""

test = False
day = 1
if test:
    data = test_case_1.strip().split("\n")
else:
    data = Day.get_data(day).strip().split("\n")


l1, l2 = [], []
for line in data:
    front, back = line.split("   ", 1)
    l1.append(int(front))
    l2.append(int(back))
l1.sort()
l2.sort()
assert len(l1) == len(l2)
distance = sum(abs(a - b) for a, b in zip(l1, l2))
print(f"day {day} part 1: {distance}")

l1, l2 = [], []
for line in data:
    front, back = line.split("   ", 1)
    l1.append(int(front))
    l2.append(int(back))

right = Counter(l2)
similarity = sum(right[n] * n for n in l1)
print(f"day {day} part 2: {similarity}")
