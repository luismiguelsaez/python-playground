
floor = 0
for f in [x.strip() for x in open('input.txt').readlines()][0]: floor += 1 if f == '(' else -1

print(f"Part 1: {floor}")
# Result: 74

floor = 0
for c, f in enumerate([x.strip() for x in open('input.txt').readlines()][0]):
  floor += 1 if f == '(' else -1
  if floor == -1:
    print(f"Part 2: {c+1}")
    # Result: 1795
    break
