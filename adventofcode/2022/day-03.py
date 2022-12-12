from requests import get

# Get session cookie after login to adventofcode.com
session = '53616c7465645f5f2596cddc32bc251ebdc3b21070bbf3af3f2bd32ac8054d7793c9a0bf8affc014c500bff2c2e337c5dcc62093649140fb38d28f4a8795f288'
res = get('https://adventofcode.com/2022/day/3/input', cookies={'session': session})
input = res.text

items = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

sum = 0
for rucksack in input.split('\n'):
  if rucksack != '':
    r_len = len(rucksack)
    first = rucksack[0:r_len // 2]
    second = rucksack[r_len // 2:]
    common = [i for i in first if i in second]
    sum += items.index(common[0]) + 1

# First part
print(f"Sum: {sum}")

group = list()
rucksacks = input.split('\n')
sum = 0

for i in range(len(rucksacks)):
  if rucksacks[i] != '':
    group.append(rucksacks[i])
    if len(group) == 3:
      common = set(group[0]) & set(group[1]) & set(group[2])
      print(f"Group: {group} Common item: {common}")
      sum += items.index(list(common)[0]) + 1
      group = list()

# Second part
print(f"Sum: {sum}")
