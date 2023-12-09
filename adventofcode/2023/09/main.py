from sys import argv

lines = [l.rstrip() for l in open(argv[1]).readlines()]

def get_elements_diff(elements: list[int])->list[int]:
    diff = [elements[i+1] - elements[i] for i in range(len(elements)) if i < len(elements) - 1]
    return diff

sum_left = 0
sum_right = 0
for l in range(len(lines)):
    line = list(map(lambda x:int(x), lines[l].split(' ')))
    rows = [line]
    while len(list(filter(lambda x:x != 0, line))) > 0:
        line = get_elements_diff(line)
        rows.append(line)
    
    val_right = 0
    val_left = 0
    for i in range(len(rows)-1, -1, -1):
        if i == len(rows)-1:
            rows[i].append(val_right)
            rows[i].insert(0, val_left)
        else:
            val_right = rows[i][-1] + rows[i+1][-1]
            rows[i].append(val_right)
            val_left = rows[i][0] - rows[i+1][0]
            rows[i].insert(0, val_left)

    sum_left += val_left
    sum_right += val_right

print(f"Part one: {sum_right}")
print(f"Part two: {sum_left}")
