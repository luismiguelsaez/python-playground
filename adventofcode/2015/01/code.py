
floor = 0
for f in [x.strip() for x in open('input.txt').readlines()][0]: floor += 1 if f == '(' else -1

print(f"Part 1: {floor}")
