from sys import argv
from itertools import cycle
import re
import math

lines = [l.rstrip() for l in open(argv[1], 'r').readlines()]

steps = cycle(lines[0])
coord_lines = lines[2:]
coords = {}
for c in range(len(coord_lines)):
    match = re.search('^([A-Z]+) = \\(([A-Z]+), ([A-Z]+)\\)', coord_lines[c])
    tag, left, right = match.groups()
    coords[tag] = (left, right)

c = 0
next = 'AAA'
end = 'ZZZ'
for step in steps:
    if next == end:
        break
    left, right = coords[next]
    next = left if step == 'L' else right
    c += 1

print(f"Part one: {c}")


starts = [i for i in coords if re.match('[A-Z][A-Z]A', i)]
multiples = []
for start in starts:
    steps = cycle(lines[0])
    next = start
    c = 0
    print(f"Checking start position {start}")
    for step in steps:
        if re.match('[A-Z][A-Z]Z', next):
            print(f"[{c}] Found position {next} for start {start}")
            multiples.append(c)
            break
        left, right = coords[next]
        next = left if step == 'L' else right
        c += 1

print(f"Part two: {math.lcm(*multiples)}")
