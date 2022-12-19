
floor = 0
for f in [x.strip() for x in open('input.txt').readlines()][0]: floor += 1 if f == '(' else -1

print(f"Part 1: {floor}")
# Result: 74

floor = 0
c = 0
for f in [x.strip() for x in open('input.txt').readlines()][0]:
  c += 1
  floor += 1 if f == '(' else -1
  if floor == -1:
    print(f"Part 2: {c}")
    # Result: 1795
    break
