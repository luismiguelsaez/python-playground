from sys import argv
import re

steps = open(argv[1]).readline().rstrip().split(',')

boxes = {}
for i in range(256): boxes[i] = []

total_value = 0
for s in range(len(steps)):
    step_value = 0
    for c in range(len(steps[s])):
        step_value = ( ( step_value + ord(steps[s][c]) ) * 17 ) % 256
    # BEGIN second part
    if re.match('^[a-z]+=[0-9]+$', steps[s]):
        label, value = steps[s].split('=')
        label_value = 0
        for c in range(len(label)):
            label_value = ( ( label_value + ord(steps[s][c]) ) * 17 ) % 256
        # Check if the label is already in the box
        if len([i for i in range(len(boxes[label_value])) if boxes[label_value][i][0] == label]) == 0:
            boxes[label_value].append((label, int(value)))
        else:
            idx = [i for i in range(len(boxes[label_value])) if boxes[label_value][i][0] == label]
            boxes[label_value][idx[0]] = (label, int(value))
    else:
        label = steps[s].split('-')[0]
        label_value = 0
        for c in range(len(label)):
            label_value = ( ( label_value + ord(steps[s][c]) ) * 17 ) % 256
        if len([i for i in range(len(boxes[label_value])) if boxes[label_value][i][0] == label]) == 0:
            pass
        else:
            idx = [i for i in range(len(boxes[label_value])) if boxes[label_value][i][0] == label]
            del boxes[label_value][idx[0]]
    # END second part
    total_value += step_value

print(f"Part one: {total_value}")

total_value = 0
for b in range(len(boxes)):
    if boxes[b] != []:
        box_value = 0
        for l in range(len(boxes[b])):
            box_value += (b + 1 ) * ( l + 1 ) * boxes[b][l][1]
            print(f"- {boxes[b][l][0]}: {b + 1} (box {b}) * {l + 1} * {boxes[b][l][1]} = {(b + 1 ) * ( l + 1 ) * boxes[b][l][1]}")
        total_value += box_value

print(f"Part two: {total_value}")
