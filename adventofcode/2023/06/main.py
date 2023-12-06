from sys import argv
import re

lines = [ l.rstrip() for l in open(argv[1], 'r').readlines() ]

vals = []
for time, distance in zip(re.findall('\\s+([0-9]+)', lines[0].split(':')[1]), re.findall('\\s+([0-9]+)', lines[1].split(':')[1])):
    vals.append(len(list(map(lambda x: [ i for i in range(0, int(x[0])+1) if (int(x[0]) - i) * i > int(x[1])] , [(time, distance)]))[0]))

total = 0
for i in range(len(vals)-1):
    if i == 0:
        total = vals[i] * vals[i+1]
    else:
        total = total * vals[i+1]

print(f"Part one: {total}")


time, distance = ''.join(re.findall('[0-9]', lines[0].split(':')[1])), ''.join(re.findall('[0-9]', lines[1].split(':')[1]))
ways = [ i for i in range(0, int(time)+1) if (int(time) - i) * i > int(distance) ]

print(f"Part two: {len(ways)}")
